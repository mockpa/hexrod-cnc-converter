#!/usr/bin/env python3
"""
Fly Rod Grip G-Code Generator for LinuxCNC
==========================================
Generates G-Code for milling cork or wood grips using a rotary A-axis
(stepper-driven dividing head).

Machine geometry:
  - Horizontal spindle, cutting from BELOW the workpiece
  - X = along the grip length
  - Z = distance from grip axis to tool center (Z=0 at grip axis)
  - A = workpiece rotation (dividing head)

Z zero-point: Set at the grip axis (center of rotation of the dividing head),
NOT at the blank surface.

Grip types:
  "zylindrisch" – cylindrical, constant radius
  "konisch"     – conical, linear radius change tip to butt
  "polygon"     – regular polygon (hexagon, octagon, etc.) with indexed A-axis

Usage:
  1. Set GRIFFTYP and parameters below
  2. python3 griff_generator.py > griff.ngc

LinuxCNC A-axis config (INI):
  WRAPPED_ROTARY = 0   for cylindrical/conical (continuous turning)
  WRAPPED_ROTARY = 1   for polygon (indexing only)
"""
import math
import sys

# ─── GRIP TYPE ────────────────────────────────────────────────────────────────
GRIFFTYP = "polygon"   # "zylindrisch" | "konisch" | "polygon"

# ─── GRIP DIMENSIONS ─────────────────────────────────────────────────────────
GRIFF_LAENGE_MM = 200.0   # total grip length (mm)
X_START_MM      =   0.0   # X start position

ROHLING_RADIUS  =  15.0   # blank radius before milling (mm)
FRAESER_RADIUS  =   3.0   # end mill radius (mm)

# Cylindrical:
ZIEL_RADIUS     =  10.0   # finished grip radius (mm)

# Conical:
RADIUS_TIP      =   8.0   # radius at narrow (tip) end (mm)
RADIUS_BUTT     =  13.0   # radius at wide (butt) end (mm)

# Polygon:
POLYGON_SEITEN  =   8     # number of faces (6=hex, 8=oct, ...)
POLYGON_UMKREIS =  11.0   # circumradius of finished polygon (mm)

# ─── MACHINE PARAMETERS ───────────────────────────────────────────────────────
FEED_CUT    = 150     # mm/min cutting feed
SCHRITT_MM  =   1.0   # X-axis resolution (mm)

# Safe Z: above blank surface seen from below
# = blank radius + tool radius + 2mm clearance
Z_FREIFAHRT = ROHLING_RADIUS + FRAESER_RADIUS + 2.0

# ─── COORDINATE SYSTEM (horizontal spindle, from below) ──────────────────────

def z_for_radius(target_r):
    """
    Z = distance from grip axis to tool center.
    Cutting position for target radius:
      Z = target_radius + tool_radius
    Z=0 is the grip axis (A-axis center of rotation).
    """
    return target_r + FRAESER_RADIUS

def conical_radius(x_mm):
    """Linearly interpolated radius for conical grip."""
    t = (x_mm - X_START_MM) / GRIFF_LAENGE_MM
    return RADIUS_TIP + t * (RADIUS_BUTT - RADIUS_TIP)

# ─── CYLINDRICAL / CONICAL ───────────────────────────────────────────────────

def generate_turning():
    """
    Lathe-style turning: A rotates continuously, Z follows the radius profile,
    X advances simultaneously. Multiple roughing passes + one finishing pass.
    """
    lines = []
    lines.append(f"; === {GRIFFTYP.upper()} GRIP – horizontal spindle, cutting from below ===")
    lines.append(f"; Length: {GRIFF_LAENGE_MM}mm")
    if GRIFFTYP == "zylindrisch":
        lines.append(f"; Radius: {ZIEL_RADIUS}mm")
    else:
        lines.append(f"; Radius: {RADIUS_TIP}mm (tip) -> {RADIUS_BUTT}mm (butt)")
    lines.append(f"; Z=0 at grip axis")
    lines.append("")
    lines.append("G21 G90 G94")
    lines.append(f"G0 Z{Z_FREIFAHRT:.3f}  ; clear of blank")
    lines.append("G0 X0 A0")
    lines.append("")

    # Build roughing passes from blank down to target
    if GRIFFTYP == "zylindrisch":
        target_r = ZIEL_RADIUS
    else:
        target_r = min(RADIUS_TIP, RADIUS_BUTT)

    roughing_steps = []
    r = ROHLING_RADIUS - 1.0
    while r >= target_r + 0.5:
        roughing_steps.append(("roughing", r))
        r -= 1.0
    roughing_steps.append(("finishing", None))  # None = follow contour

    rotations_per_mm = 3   # overlapping passes for good surface
    a_total = 0.0

    for pass_type, fixed_r in roughing_steps:
        label = f"roughing r={fixed_r:.1f}mm" if fixed_r else "finishing (contour)"
        lines.append(f"; --- {label} ---")
        lines.append(f"G0 Z{Z_FREIFAHRT:.3f}")
        lines.append(f"G0 X{X_START_MM:.3f}")

        x = X_START_MM
        while True:
            x = min(x, X_START_MM + GRIFF_LAENGE_MM)

            if fixed_r is not None:
                r = fixed_r
            else:
                r = conical_radius(x) if GRIFFTYP == "konisch" else ZIEL_RADIUS

            z = z_for_radius(r)
            a_total += 360.0 * rotations_per_mm * SCHRITT_MM
            lines.append(f"G1 X{x:.3f} Z{z:.4f} A{a_total:.1f} F{FEED_CUT}")

            if x >= X_START_MM + GRIFF_LAENGE_MM:
                break
            x += SCHRITT_MM

        lines.append(f"G0 Z{Z_FREIFAHRT:.3f}")
        lines.append(f"G0 X{X_START_MM:.3f}")
        lines.append("")

    lines.append(f"G0 Z{Z_FREIFAHRT:.3f}")
    lines.append("G0 X0")
    lines.append("M2")
    return lines

# ─── POLYGON ─────────────────────────────────────────────────────────────────

def generate_polygon():
    """
    Polygon milling with horizontal spindle from below:
    - A indexes to face center angle (face perpendicular to tool)
    - Z advances to inradius + tool radius (flat cut)
    - X mills full grip length
    - Between faces: Z retracts, A indexes to next face
    """
    sektor   = 360.0 / POLYGON_SEITEN
    inkreis  = POLYGON_UMKREIS * math.cos(math.pi / POLYGON_SEITEN)
    z_cut    = z_for_radius(inkreis)
    z_entry  = z_for_radius(ROHLING_RADIUS)  # tangent at blank surface

    lines = []
    lines.append(f"; === POLYGON GRIP ({POLYGON_SEITEN}-sided) – horizontal spindle, from below ===")
    lines.append(f"; Length: {GRIFF_LAENGE_MM}mm")
    lines.append(f"; Circumradius: {POLYGON_UMKREIS:.2f}mm  Inradius: {inkreis:.3f}mm")
    lines.append(f"; Z cut position: {z_cut:.4f}mm from axis")
    lines.append(f"; {POLYGON_SEITEN} faces, {sektor:.1f}° apart")
    lines.append(f"; Z=0 at grip axis")
    lines.append("")
    lines.append("G21 G90 G94")
    lines.append(f"G0 Z{Z_FREIFAHRT:.3f}")
    lines.append("G0 X0 A0")
    lines.append("")

    for face in range(POLYGON_SEITEN):
        a_angle = face * sektor
        lines.append(f"; --- Face {face+1}/{POLYGON_SEITEN}  A={a_angle:.1f}° ---")
        lines.append(f"G0 Z{Z_FREIFAHRT:.3f}              ; retract")
        lines.append(f"G0 A{a_angle:.2f}                 ; index: face perpendicular to tool")
        lines.append(f"G0 X{X_START_MM:.3f}               ; start position")
        lines.append(f"G1 Z{z_entry:.4f} F{FEED_CUT // 2}  ; approach blank surface")
        lines.append(f"G1 Z{z_cut:.4f}  F{FEED_CUT // 3}  ; plunge to cut depth")
        lines.append(f"G1 X{X_START_MM + GRIFF_LAENGE_MM:.3f} F{FEED_CUT}  ; mill face")
        lines.append("")

    lines.append(f"G0 Z{Z_FREIFAHRT:.3f}")
    lines.append("G0 X0 A0")
    lines.append("M2")
    return lines

# ─── MAIN ─────────────────────────────────────────────────────────────────────

if GRIFFTYP in ("zylindrisch", "konisch"):
    gcode_lines = generate_turning()
elif GRIFFTYP == "polygon":
    gcode_lines = generate_polygon()
else:
    print(f"Unknown GRIFFTYP: {GRIFFTYP}", file=sys.stderr)
    sys.exit(1)

gcode = "\n".join(gcode_lines)
print(gcode)

filename = f"griff_{GRIFFTYP}.ngc"
with open(filename, "w") as f:
    f.write(gcode)
print(f"\n; -> Saved as {filename}", file=sys.stderr)
