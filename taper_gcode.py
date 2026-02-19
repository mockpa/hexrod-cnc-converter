#!/usr/bin/env python3
"""
Hexrod Taper to LinuxCNC G-Code Generator
==========================================
Converts flat-to-flat taper dimensions (at 5-inch stations) into a
2-axis LinuxCNC G-Code program for milling bamboo hex rod strips.

Axes:
  X = along the strip length
  Z = cut depth (horizontal spindle)

Usage:
  Edit taper_data and machine parameters below, then run:
    python3 taper_gcode.py > taper.ngc
"""

# ─── TAPER DATA ───────────────────────────────────────────────────────────────
# Format: (station_inches, flat_to_flat_dimension_mm)
# Start at 0 (tip), end at full length (butt)
taper_data = [
    (0,   1.52),
    (5,   1.78),
    (10,  2.03),
    (15,  2.29),
    (20,  2.54),
    (25,  2.79),
    (30,  3.05),
    (35,  3.30),
    (40,  3.56),
    (45,  3.81),
    (50,  4.06),
    (55,  4.32),
    (60,  4.57),
]

# ─── MACHINE PARAMETERS ───────────────────────────────────────────────────────
ZOLL_ZU_MM       = 25.4
FEED_RATE        = 300      # mm/min
Z_RAPID          = 5.0      # rapid height above workpiece (mm)
Z_OFFSET         = 0.0      # zero-point correction (mm)
EXTRA_LAENGE_MM  = 10.0     # overshoot at butt end (mm)

# ─── FUNCTIONS ────────────────────────────────────────────────────────────────

def dimension_to_z(dim_mm):
    """Convert flat-to-flat dimension to Z cut depth (strip height = dim/2)."""
    return -(dim_mm / 2.0) + Z_OFFSET

# ─── MAIN ─────────────────────────────────────────────────────────────────────

stations = [(s * ZOLL_ZU_MM, d) for s, d in taper_data]

lines = []
lines.append("; Hexrod Taper G-Code for LinuxCNC")
lines.append(f"; Taper: {taper_data[0][1]:.2f}mm (Tip) -> {taper_data[-1][1]:.2f}mm (Butt)")
lines.append("; Axes: X=length, Z=depth")
lines.append("")
lines.append("G21          ; metric")
lines.append("G90          ; absolute coordinates")
lines.append("G94          ; feed in mm/min")
lines.append("")
lines.append("; === START ===")
lines.append("G0 Z{:.3f}  ; rapid to safe height".format(Z_RAPID))
lines.append("G0 X0        ; home X")
lines.append("")

x0, d0 = stations[0]
z0 = dimension_to_z(d0)
lines.append(f"; Tip: X={x0:.3f} Dim={d0:.3f}mm Z={z0:.4f}mm")
lines.append(f"G0 X{x0:.3f}")
lines.append(f"G1 Z{z0:.4f} F{FEED_RATE}")
lines.append("")

for x, dim in stations[1:]:
    z = dimension_to_z(dim)
    lines.append(f"; Station X={x:.1f}mm, Dim={dim:.3f}mm -> Z={z:.4f}mm")
    lines.append(f"G1 X{x:.3f} Z{z:.4f} F{FEED_RATE}")

x_end = stations[-1][0] + EXTRA_LAENGE_MM
z_end = dimension_to_z(stations[-1][1])
lines.append(f"G1 X{x_end:.3f} Z{z_end:.4f} F{FEED_RATE}  ; overshoot")
lines.append("")
lines.append("; === END ===")
lines.append(f"G0 Z{Z_RAPID:.3f}")
lines.append("G0 X0")
lines.append("M2  ; program end")

gcode = "\n".join(lines)
print(gcode)

with open("taper.ngc", "w") as f:
    f.write(gcode)

import sys
print("\n; -> Saved as taper.ngc", file=sys.stderr)
