#!/usr/bin/env python3
"""
Hexrod Hollow Milling G-Code Generator for LinuxCNC
====================================================
Reads the same taper data file used by taper_gcode.py and generates a
G-code program for milling the inner hollow (pith side) of bamboo strips.

Features:
  - Solid tip and butt sections (no hollowing near the ends)
  - Glue lands at regular intervals
  - Smooth sine-curve transitions in/out of all solid sections
  - Wall thickness follows the taper automatically

Axes:
  X = along the strip length
  Z = cut depth  (Z=0 at strip surface, negative = cutting into strip)

Tool:
  T1 = 12mm flat end mill

Usage:
  python3 hollowing.py myrod.dat
  python3 hollowing.py myrod.dat --thou --wall 0.5 --feed 150
  python3 hollowing.py myrod.dat -o myrod_hollow.ngc

Data file format: same as taper_gcode.py (station_inches  flat_to_flat_mm)
"""

import math
import sys
import argparse

# ─── HOLLOWING PARAMETERS (defaults, overridable via CLI) ─────────────────────
TIP_SOLID_MM    =  80.0   # solid length at tip (mm)
BUTT_SOLID_MM   =  60.0   # solid length at butt (mm)
STEG_ABSTAND_MM = 150.0   # glue land spacing, center-to-center (mm)
STEG_BREITE_MM  =  12.0   # glue land width (mm)
UEBERGANG_MM    =   8.0   # sine transition zone length (mm)
WANDSTAERKE_MM  =   0.4   # wall thickness / power fiber layer (mm)

# ─── MACHINE PARAMETERS ───────────────────────────────────────────────────────
FEED_RATE  = 200     # mm/min
Z_RAPID    = 3.0     # safe height above workpiece (mm)
SCHRITT_MM = 1.0     # toolpath resolution (mm)

# ─── FUNCTIONS ────────────────────────────────────────────────────────────────

def parse_taper_file(path, thou_mode):
    stations = []
    with open(path) as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            try:
                station_in = float(parts[0])
                dim        = float(parts[1])
            except ValueError:
                continue
            dim_mm = dim * 2.0 * 0.0254 if thou_mode else dim
            stations.append((station_in, dim_mm))
    return stations


def interpolate_dimension(x_mm, stations_mm):
    for i in range(len(stations_mm) - 1):
        x0, d0 = stations_mm[i]
        x1, d1 = stations_mm[i + 1]
        if x0 <= x_mm <= x1:
            t = (x_mm - x0) / (x1 - x0)
            return d0 + t * (d1 - d0)
    return None


def sine_transition(t):
    return 0.5 * (1 - math.cos(math.pi * t))


def compute_factor(x_mm, x_total, steg_positions):
    """
    Returns 0.0 (solid/land) to 1.0 (full hollow depth).
    Transitions use smooth sine curves.
    """
    if x_mm < TIP_SOLID_MM:
        if x_mm < TIP_SOLID_MM - UEBERGANG_MM:
            return 0.0
        t = (x_mm - (TIP_SOLID_MM - UEBERGANG_MM)) / UEBERGANG_MM
        return sine_transition(t)

    butt_start = x_total - BUTT_SOLID_MM
    if x_mm > butt_start:
        if x_mm > butt_start + UEBERGANG_MM:
            return 0.0
        t = (x_mm - butt_start) / UEBERGANG_MM
        return 1.0 - sine_transition(t)

    for steg_center in steg_positions:
        steg_l  = steg_center - STEG_BREITE_MM / 2.0
        steg_r  = steg_center + STEG_BREITE_MM / 2.0
        entry_l = steg_l - UEBERGANG_MM
        exit_r  = steg_r + UEBERGANG_MM

        if steg_l <= x_mm <= steg_r:
            return 0.0
        elif entry_l <= x_mm < steg_l:
            t = (x_mm - entry_l) / UEBERGANG_MM
            return 1.0 - sine_transition(t)
        elif steg_r < x_mm <= exit_r:
            t = (x_mm - steg_r) / UEBERGANG_MM
            return sine_transition(t)

    return 1.0


def compute_steg_positions(x_total):
    hohl_start = TIP_SOLID_MM
    hohl_end   = x_total - BUTT_SOLID_MM
    stege = []
    x = hohl_start + STEG_ABSTAND_MM
    while x < hohl_end:
        stege.append(x)
        x += STEG_ABSTAND_MM
    return stege


def generate_gcode(taper_data, source_name=""):
    stations_mm = [(s * 25.4, d) for s, d in taper_data]
    x_total     = stations_mm[-1][0]
    steg_positions = compute_steg_positions(x_total)

    print(f"; ============================================", file=sys.stderr)
    print(f";  Hexrod Hollowing G-Code - LinuxCNC",         file=sys.stderr)
    print(f"; ============================================", file=sys.stderr)
    print(f"; Source:       {source_name}",                 file=sys.stderr)
    print(f"; Total length: {x_total:.1f} mm",              file=sys.stderr)
    print(f"; Tip solid:    {TIP_SOLID_MM:.1f} mm",         file=sys.stderr)
    print(f"; Butt solid:   {BUTT_SOLID_MM:.1f} mm",        file=sys.stderr)
    print(f"; Hollow range: {TIP_SOLID_MM:.1f} - {x_total - BUTT_SOLID_MM:.1f} mm", file=sys.stderr)
    print(f"; Glue lands:   {', '.join(f'{s:.1f}mm' for s in steg_positions)}", file=sys.stderr)
    print(f"; Land width:   {STEG_BREITE_MM:.1f} mm",       file=sys.stderr)
    print(f"; Wall thick:   {WANDSTAERKE_MM:.2f} mm",        file=sys.stderr)
    print(f"; ============================================", file=sys.stderr)

    # Build toolpath
    path = []
    x = 0.0
    while True:
        x = min(x, x_total)
        dim = interpolate_dimension(x, stations_mm)
        if dim is None:
            break
        max_depth = max(0.0, (dim / 2.0) - WANDSTAERKE_MM)
        factor    = compute_factor(x, x_total, steg_positions)
        z = -max_depth * factor
        path.append((x, z))
        if x >= x_total:
            break
        x += SCHRITT_MM

    lines = []
    lines.append("; Hexrod Hollowing G-Code for LinuxCNC")
    if source_name:
        lines.append(f"; Source: {source_name}")
    lines.append(f"; Tip solid: {TIP_SOLID_MM}mm | Butt solid: {BUTT_SOLID_MM}mm")
    lines.append(f"; Glue lands: {', '.join(f'{s:.1f}mm' for s in steg_positions)}")
    lines.append(f"; Wall: {WANDSTAERKE_MM}mm | Transition: {UEBERGANG_MM}mm")
    lines.append("; Tool: T1 — 12mm flat end mill")
    lines.append("")
    lines.append("T1 M6        ; load 12mm end mill")
    lines.append("G43 H1       ; apply tool 1 length offset")
    lines.append("G21          ; metric")
    lines.append("G90          ; absolute")
    lines.append("G94          ; feed in mm/min")
    lines.append("")
    lines.append(f"G0 Z{Z_RAPID:.3f}   ; safe height")
    lines.append("G0 X0")
    lines.append("")
    lines.append("; === Hollow milling pass ===")
    lines.append("")

    cutting = False
    for x, z in path:
        if z < -0.01:
            if not cutting:
                lines.append(f"G0 X{x:.3f}")
                lines.append(f"G1 Z{z:.4f} F{FEED_RATE}")
                cutting = True
            else:
                lines.append(f"G1 X{x:.3f} Z{z:.4f} F{FEED_RATE}")
        else:
            if cutting:
                lines.append(f"G1 X{x:.3f} Z{z:.4f} F{FEED_RATE}  ; -> land/end")
                cutting = False

    lines.append("")
    lines.append(f"G0 Z{Z_RAPID:.3f}  ; retract")
    lines.append("G0 X0          ; home")
    lines.append("M2             ; end")

    return "\n".join(lines)


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Generate hollowing G-code from taper data file"
    )
    parser.add_argument("taper_file",
        help="Taper data file (same format as taper_gcode.py)")
    parser.add_argument("--thou", action="store_true",
        help="Input dimensions are in thousandths of an inch per side")
    parser.add_argument("--feed", type=float, default=FEED_RATE,
        help=f"Feed rate mm/min (default {FEED_RATE})")
    parser.add_argument("--wall", type=float, default=WANDSTAERKE_MM,
        help=f"Wall thickness mm (default {WANDSTAERKE_MM})")
    parser.add_argument("--tip-solid", type=float, default=TIP_SOLID_MM,
        help=f"Solid tip length mm (default {TIP_SOLID_MM})")
    parser.add_argument("--butt-solid", type=float, default=BUTT_SOLID_MM,
        help=f"Solid butt length mm (default {BUTT_SOLID_MM})")
    parser.add_argument("--land-spacing", type=float, default=STEG_ABSTAND_MM,
        help=f"Glue land spacing mm (default {STEG_ABSTAND_MM})")
    parser.add_argument("-o", "--output",
        help="Output .ngc file (default: input name + _hollow.ngc)")
    args = parser.parse_args()

    global FEED_RATE, WANDSTAERKE_MM, TIP_SOLID_MM, BUTT_SOLID_MM, STEG_ABSTAND_MM
    FEED_RATE       = args.feed
    WANDSTAERKE_MM  = args.wall
    TIP_SOLID_MM    = args.tip_solid
    BUTT_SOLID_MM   = args.butt_solid
    STEG_ABSTAND_MM = args.land_spacing

    taper_data = parse_taper_file(args.taper_file, args.thou)

    if not taper_data:
        print("Error: no valid taper data found in file.", file=sys.stderr)
        sys.exit(1)

    gcode = generate_gcode(taper_data, source_name=args.taper_file)

    if args.output:
        out_path = args.output
    else:
        base = args.taper_file.rsplit('.', 1)[0] if '.' in args.taper_file else args.taper_file
        out_path = base + "_hollow.ngc"

    with open(out_path, 'w') as f:
        f.write(gcode)

    print(f"Written: {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
