#!/usr/bin/env python3
"""
Hexrod Taper to LinuxCNC G-Code Generator
==========================================
Reads station-based taper data from a file and generates a 2-axis
LinuxCNC G-code program for milling bamboo hex rod strips with a
double 60-degree disk cutter.

Axes:
  X = along the strip length
  Z = cut depth  (Z=0 at strip flat face; negative = cutting into strip)

Tool:
  T2 = double 60-degree disk cutter (D=45mm)
  Z cut depth = flat_to_flat / 2  (= strip height for a 60-degree hex strip)

Usage:
  python3 taper_gcode.py myrod.dat
  python3 taper_gcode.py myrod.dat --thou          # dimensions in thou/side
  python3 taper_gcode.py myrod.dat --feed 200 -o myrod.ngc

Data file format (.dat):
  # comment lines start with #
  # station_inches  flat_to_flat_mm
  0     1.52
  5     1.78
  10    2.03
  ...

  With --thou flag:
  # station_inches  thou_per_side
  0     60
  5     70
  10    80
  ...
  (thou_per_side * 2 * 0.0254 = flat_to_flat_mm)
"""

import sys
import argparse

# ─── MACHINE PARAMETERS ───────────────────────────────────────────────────────
FEED_RATE       = 300     # mm/min
Z_RAPID         = 5.0     # safe height above workpiece (mm)
Z_OFFSET        = 0.0     # fine zero-point correction (mm)
EXTRA_LAENGE_MM = 10.0    # overshoot at butt end (mm)

# ─── FUNCTIONS ────────────────────────────────────────────────────────────────

def parse_taper_file(path, thou_mode):
    """
    Read taper data from a text file.
    Returns list of (station_inches, flat_to_flat_mm).
    """
    stations = []
    with open(path) as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) < 2:
                print(f"Warning: line {lineno} skipped (need 2 columns): {line!r}",
                      file=sys.stderr)
                continue
            try:
                station_in = float(parts[0])
                dim        = float(parts[1])
            except ValueError:
                print(f"Warning: line {lineno} skipped (not numeric): {line!r}",
                      file=sys.stderr)
                continue

            if thou_mode:
                # thousandths of an inch per side → flat-to-flat mm
                dim_mm = dim * 2.0 * 0.0254
            else:
                dim_mm = dim

            stations.append((station_in, dim_mm))

    return stations


def dimension_to_z(dim_mm):
    """Convert flat-to-flat dimension (mm) to Z cut depth (mm)."""
    return -(dim_mm / 2.0) + Z_OFFSET


def generate_gcode(taper_data, source_name=""):
    """
    taper_data: list of (station_inches, flat_to_flat_mm)
    Returns G-code string.
    """
    stations = [(s * 25.4, d) for s, d in taper_data]
    tip_dim  = taper_data[0][1]
    butt_dim = taper_data[-1][1]

    lines = []
    lines.append("; Hexrod Taper G-Code for LinuxCNC")
    if source_name:
        lines.append(f"; Source: {source_name}")
    lines.append(f"; Taper: {tip_dim:.3f}mm (tip) -> {butt_dim:.3f}mm (butt) flat-to-flat")
    lines.append(f"; Length: {stations[-1][0]:.1f}mm  Stations: {len(stations)}")
    lines.append("; Tool: T2 — double 60-degree disk cutter")
    lines.append("; Z=0 at strip flat face; Z negative = cutting into strip")
    lines.append("")
    lines.append("T2 M6        ; load double disk cutter")
    lines.append("G43 H2       ; apply tool 2 length offset")
    lines.append("G21          ; metric")
    lines.append("G90          ; absolute coordinates")
    lines.append("G94          ; feed in mm/min")
    lines.append("")
    lines.append(f"G0 Z{Z_RAPID:.3f}   ; rapid to safe height")
    lines.append("G0 X0        ; go to X start")
    lines.append("")

    x0, d0 = stations[0]
    z0 = dimension_to_z(d0)
    lines.append(f"; Tip: X={x0:.3f}mm  dim={d0:.3f}mm  Z={z0:.4f}mm")
    lines.append(f"G0 X{x0:.3f}")
    lines.append(f"G1 Z{z0:.4f} F{FEED_RATE}")
    lines.append("")

    for x, dim in stations[1:]:
        z = dimension_to_z(dim)
        lines.append(f"; Station {x/25.4:.1f}\"  X={x:.1f}mm  dim={dim:.3f}mm  Z={z:.4f}mm")
        lines.append(f"G1 X{x:.3f} Z{z:.4f} F{FEED_RATE}")

    x_end = stations[-1][0] + EXTRA_LAENGE_MM
    z_end = dimension_to_z(stations[-1][1])
    lines.append(f"G1 X{x_end:.3f} Z{z_end:.4f} F{FEED_RATE}  ; overshoot")
    lines.append("")
    lines.append(f"G0 Z{Z_RAPID:.3f}  ; retract")
    lines.append("G0 X0        ; home X")
    lines.append("M2           ; program end")

    return "\n".join(lines)


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Convert taper data file to LinuxCNC G-code for hex rod milling"
    )
    parser.add_argument("taper_file",
        help="Taper data file (station_inches  flat_to_flat_mm per line)")
    parser.add_argument("--thou", action="store_true",
        help="Input dimensions are in thousandths of an inch per side")
    parser.add_argument("--feed", type=float, default=300,
        help="Feed rate in mm/min (default 300)")
    parser.add_argument("--extra", type=float, default=10.0,
        help="Overshoot at butt end in mm (default 10.0)")
    parser.add_argument("-o", "--output",
        help="Output .ngc file (default: input filename with .ngc extension)")
    args = parser.parse_args()

    global FEED_RATE, EXTRA_LAENGE_MM
    FEED_RATE       = args.feed
    EXTRA_LAENGE_MM = args.extra

    taper_data = parse_taper_file(args.taper_file, args.thou)

    if not taper_data:
        print("Error: no valid taper data found in file.", file=sys.stderr)
        sys.exit(1)

    gcode = generate_gcode(taper_data, source_name=args.taper_file)

    if args.output:
        out_path = args.output
    else:
        base = args.taper_file.rsplit('.', 1)[0] if '.' in args.taper_file else args.taper_file
        out_path = base + ".ngc"

    with open(out_path, 'w') as f:
        f.write(gcode)

    print(f"Written:   {out_path}", file=sys.stderr)
    print(f"Stations:  {len(taper_data)}", file=sys.stderr)
    print(f"Length:    {taper_data[-1][0] * 25.4:.1f} mm  ({taper_data[-1][0]:.1f}\")", file=sys.stderr)
    print(f"Tip dim:   {taper_data[0][1]:.3f} mm flat-to-flat", file=sys.stderr)
    print(f"Butt dim:  {taper_data[-1][1]:.3f} mm flat-to-flat", file=sys.stderr)


if __name__ == "__main__":
    main()
