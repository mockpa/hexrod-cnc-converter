#!/usr/bin/env python3
"""
Hexrod Hollow Milling G-Code Generator for LinuxCNC
====================================================
Mills the inner hollow (pith side) of bamboo strips using a flat end mill.

Features:
  - Solid tip and butt sections (configurable length)
  - Glue lands at regular intervals
  - Smooth sine-curve transitions in/out of all solid sections
  - Wall thickness follows the taper automatically

Axes:
  X = along the strip length
  Z = cut depth (horizontal spindle, Z=0 is the strip surface)

Usage:
  Edit taper_data, hollowing parameters and machine parameters below, then:
    python3 hollowing.py > hollowing.ngc
"""
import math
import sys

# ─── TAPER DATA ───────────────────────────────────────────────────────────────
# Format: (station_inches, flat_to_flat_dimension_mm)
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

# ─── HOLLOWING PARAMETERS ─────────────────────────────────────────────────────
TIP_SOLID_MM    =  80.0   # solid length at tip (mm)
BUTT_SOLID_MM   =  60.0   # solid length at butt (mm)

STEG_ABSTAND_MM = 150.0   # glue land spacing, center-to-center (mm)
STEG_BREITE_MM  =  12.0   # glue land width (mm)
UEBERGANG_MM    =   8.0   # sine transition zone length (mm)

WANDSTAERKE_MM  =   0.4   # remaining wall thickness / power fiber layer (mm)

# ─── MACHINE PARAMETERS ───────────────────────────────────────────────────────
ZOLL_ZU_MM  = 25.4
FEED_RATE   = 200     # mm/min
Z_RAPID     = 3.0     # safe height above workpiece (mm)
SCHRITT_MM  = 1.0     # toolpath resolution (mm) — 1mm recommended

# ─── FUNCTIONS ────────────────────────────────────────────────────────────────

def interpolate_dimension(x_mm, stations):
    """Linear interpolation of dimension at any X position."""
    for i in range(len(stations) - 1):
        x0, d0 = stations[i]
        x1, d1 = stations[i + 1]
        if x0 <= x_mm <= x1:
            t = (x_mm - x0) / (x1 - x0)
            return d0 + t * (d1 - d0)
    return None

def sine_transition(t):
    """Smooth sine transition, t in [0,1] -> [0,1]."""
    return 0.5 * (1 - math.cos(math.pi * t))

def compute_factor(x_mm, x_total, steg_positions):
    """
    Returns a factor 0.0 to 1.0:
      0.0 = do not mill (solid section or glue land)
      1.0 = full hollow depth
    Transitions are smooth sine curves.
    """
    # Tip solid section
    if x_mm < TIP_SOLID_MM:
        if x_mm < TIP_SOLID_MM - UEBERGANG_MM:
            return 0.0
        t = (x_mm - (TIP_SOLID_MM - UEBERGANG_MM)) / UEBERGANG_MM
        return sine_transition(t)

    # Butt solid section
    butt_start = x_total - BUTT_SOLID_MM
    if x_mm > butt_start:
        if x_mm > butt_start + UEBERGANG_MM:
            return 0.0
        t = (x_mm - butt_start) / UEBERGANG_MM
        return 1.0 - sine_transition(t)

    # Glue lands
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

    return 1.0  # full hollow depth

def compute_steg_positions(x_total):
    """Distribute glue lands evenly in the hollow section."""
    hohl_start  = TIP_SOLID_MM
    hohl_end    = x_total - BUTT_SOLID_MM
    stege = []
    x = hohl_start + STEG_ABSTAND_MM
    while x < hohl_end:
        stege.append(x)
        x += STEG_ABSTAND_MM
    return stege

# ─── MAIN ─────────────────────────────────────────────────────────────────────

stations_mm = [(s * ZOLL_ZU_MM, d) for s, d in taper_data]
x_total     = stations_mm[-1][0]

steg_positions = compute_steg_positions(x_total)

# Print info header to stderr
print(f"; ============================================", file=sys.stderr)
print(f";  Hexrod Hollowing G-Code - LinuxCNC",         file=sys.stderr)
print(f"; ============================================", file=sys.stderr)
print(f"; Total length:    {x_total:.1f} mm",            file=sys.stderr)
print(f"; Tip solid:       {TIP_SOLID_MM:.1f} mm",       file=sys.stderr)
print(f"; Butt solid:      {BUTT_SOLID_MM:.1f} mm",      file=sys.stderr)
print(f"; Hollow range:    {TIP_SOLID_MM:.1f} - {x_total - BUTT_SOLID_MM:.1f} mm", file=sys.stderr)
print(f"; Glue lands at:   {', '.join(f'{s:.1f}mm' for s in steg_positions)}", file=sys.stderr)
print(f"; Land width:      {STEG_BREITE_MM:.1f} mm",     file=sys.stderr)
print(f"; Transition:      {UEBERGANG_MM:.1f} mm",        file=sys.stderr)
print(f"; Wall thickness:  {WANDSTAERKE_MM:.2f} mm",      file=sys.stderr)
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
    factor = compute_factor(x, x_total, steg_positions)
    z = -max_depth * factor
    path.append((x, z))
    if x >= x_total:
        break
    x += SCHRITT_MM

# Generate G-Code
lines = []
lines.append("; Hexrod Hollowing G-Code for LinuxCNC")
lines.append(f"; Tip solid: {TIP_SOLID_MM}mm | Butt solid: {BUTT_SOLID_MM}mm")
lines.append(f"; Glue lands: {', '.join(f'{s:.1f}mm' for s in steg_positions)}")
lines.append(f"; Wall thickness: {WANDSTAERKE_MM}mm | Transition: {UEBERGANG_MM}mm")
lines.append("")
lines.append("G21  ; metric")
lines.append("G90  ; absolute")
lines.append("G94  ; feed in mm/min")
lines.append("")
lines.append(f"G0 Z{Z_RAPID:.3f}")
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
lines.append("G0 X0             ; home")
lines.append("M2                ; end")

gcode = "\n".join(lines)
print(gcode)

with open("hollowing.ngc", "w") as f:
    f.write(gcode)
print("\n; -> Saved as hollowing.ngc", file=sys.stderr)
