# Machine Description: Hexrod CNC for Bamboo Fly Rod Construction

## Purpose

This machine is purpose-built for manufacturing **split-cane (bamboo) fly fishing rods**
using CNC-controlled milling. It mills individual bamboo strips (6 per rod section) to
precise tapered profiles, optionally hollows them from the pith side, and can mill cork
or wood grips using a rotary dividing head.

---

## Mechanical Setup

### Frame and Motion

- **Structure:** V-slot aluminium extrusion profile, portal (gantry) design
- **X-axis:** Long rails (~1600mm), carries the portal along the full rod length
- **Z-axis:** Moves the spindle carriage forward/backward (horizontal movement)
- **Drive:** Stepper motors on both X and Z axes
- **Controller:** Mesa 7C81 FPGA card (hm2_rpspi driver) on a Raspberry Pi running LinuxCNC

### Spindle Orientation — Critical Detail

The spindle is **horizontal**. Its rotation axis is **perpendicular to X** — it runs
across the machine, not along the rails. This applies to both bamboo strip operations
and grip milling.

Z is the **advance direction**: it moves the spindle carriage toward or away from the
workpiece. The spindle rotation axis is perpendicular to Z as well.

```
Side view (looking along X, from the rod tip end):

   ←──── spindle rotation axis ────►
   ──────────────●──────────────       ← cutter seen end-on
                 │
                 │ Z  (advance toward workpiece)
                 ▼
   ═════════════════════════════       ← workpiece cross-section

Top view (looking down):

   ⊙  ← cutter (spindle axis perpendicular to page)
   │
   Z
   │
   ▼
   ════════════════════════════════    ← workpiece lying along X
   ────────────────────────────────► X (rod / grip length)
   (portal carries the spindle, traverses in X)
```

### Cutting Direction for Grip Milling

For milling rod grips (cork/wood), the spindle cuts **from below** the workpiece.
This is an intentional design decision:

- The dividing head (A-axis) holds the grip blank horizontally, parallel to X
- The spindle approaches the blank from below
- This maximises usable Z travel (no need to traverse the full blank radius from outside)
- Chips fall away from the workpiece by gravity
- Loading/unloading the blank is unobstructed from above

```
Side view (grip milling, looking along X):

   ←──── spindle rotation axis ────►

        ══════╪══════    ← grip blank (rotates: A-axis)
        ──────┼──────    ← grip axis = Z zero point (A-axis centre of rotation)
              │
              │ Z  (spindle advances upward toward grip axis)
              │
   ──────────●──────────    ← cutter seen end-on, approaches from below
```

**Z zero-point for grip milling is always the grip axis (center of rotation),
not the blank surface.**

---

## Coordinate System

| Axis | Direction | Description |
|------|-----------|-------------|
| X | along rails | rod/grip length (0 = tip end) |
| Z | horizontal, toward workpiece | cut depth or radial distance from grip axis |
| A | rotary | dividing head rotation (optional, stepper motor) |

### Z convention by operation:

**Taper milling (bamboo strips):**
- Z=0 is the strip surface (pith side facing spindle)
- Z negative = cutting into the strip
- `Z = -(flat_to_flat_dimension / 2)`

**Hollow milling (pith side of bamboo strips):**
- Same as taper milling
- Z=0 is the pith surface
- Z negative = hollow depth
- `Z = -(strip_height - wall_thickness)`

**Grip milling (cylindrical/conical/polygon):**
- Z=0 is the grip axis (A-axis center of rotation)
- Z positive = away from grip axis, toward spindle
- Cutting position: `Z = target_radius + tool_radius`
- Retract position: `Z = blank_radius + tool_radius + 2mm`

---

## Optional A-Axis (Dividing Head)

- **Type:** Stepper motor driven rotary axis
- **Connected to:** Mesa 7C81, stepgen channel 03
- **Use:** Grip milling only (not used for bamboo strip operations)
- **Modes:**
  - `WRAPPED_ROTARY = 1` — indexing mode for polygon grips (A steps to each face angle, stops, X mills the face)
  - `WRAPPED_ROTARY = 0` — continuous rotation for cylindrical/conical grips (A rotates while X and Z move simultaneously, like a lathe)

**SCALE formula:**
```
SCALE = (motor_steps × microsteps × gear_ratio) / 360
```

---

## Workpiece: Bamboo Strips

A hexagonal bamboo fly rod section is built from **6 identical triangular strips**
glued together. Each strip is:

- A 60° triangular cross-section
- Power fibers (hard outer skin) at the apex, pith (soft inner core) at the base
- Milled to a precise taper along its length

**Taper data format:**
- Stations every 5 inches along the rod
- Dimension given as flat-to-flat (across the finished hex rod at that station)
- Strip height at each station = `dimension / 2`
- This is the Z cut depth for that station

**Hollowing:**
- Some rod designs hollow the pith side to reduce weight
- A flat end mill removes material from the pith face
- Wall thickness (power fiber layer) is preserved: typically 0.4–0.5mm
- Glue lands (solid sections) are left at regular intervals (~150mm) for gluing
- Tip and butt ends are left solid (configurable length)
- All transitions (into/out of hollow sections and glue lands) use sine curves
  to avoid stress concentration points

---

## Software: hexrod-cnc

Repository contains three Python G-Code generators:

### `taper_gcode.py`
Converts taper station data into a LinuxCNC `.ngc` file for milling strip profiles.
Input: list of `(station_inches, flat_to_flat_mm)` tuples.
Output: G1 moves along X with simultaneous Z following the taper.

### `hollowing.py`
Generates hollow milling G-Code with:
- Configurable solid tip/butt lengths (`TIP_SOLID_MM`, `BUTT_SOLID_MM`)
- Regular glue lands (`STEG_ABSTAND_MM`, `STEG_BREITE_MM`)
- Sine-curve transitions (`UEBERGANG_MM`)
- 1mm toolpath resolution

### `griff_generator.py`
Generates grip milling G-Code for three grip types:
- `"zylindrisch"` — cylindrical, constant radius, continuous A rotation
- `"konisch"` — conical, linearly varying radius tip to butt, continuous A rotation
- `"polygon"` — regular polygon (any number of faces), A indexes to each face

All grip operations assume **horizontal spindle cutting from below**,
with Z=0 at the grip axis.

---

## LinuxCNC Configuration Files

### `linuxcnc/` — Bamboo strip operations (taper + hollowing)

`linuxcnc/hexrod.ini` — machine configuration:
- 2 axes: X, Z
- Mesa 7C81 via hm2_rpspi on Raspberry Pi

`linuxcnc/hexrod.hal` — HAL wiring:
- X: joint 0, stepgen 00
- Z: joint 1, stepgen 02

Launch: `linuxcnc linuxcnc/hexrod.ini`

### `linuxcnc-grip/` — Grip and reel seat milling

`linuxcnc-grip/grip.ini` — machine configuration:
- 3 axes: X, Z, A
- A-axis: direct-drive stepper, SCALE = 8.889 steps/deg (3200 steps/rev ÷ 360°)
- WRAPPED_ROTARY = 0 (continuous rotation, works for all grip types)
- Mesa 7C81 via hm2_rpspi on Raspberry Pi

`linuxcnc-grip/grip.hal` — HAL wiring:
- X: joint 0, stepgen 00
- Z: joint 1, stepgen 02
- A: joint 2, stepgen 03 (BOB P1 DB25 pins 8/9)

Launch: `linuxcnc linuxcnc-grip/grip.ini`

---

## Key Design Decisions Summary

1. **Horizontal spindle** — dictates all Z coordinate conventions
2. **From below** — for grip milling, maximises Z travel and simplifies workholding
3. **Z=0 at strip surface** — for bamboo strip operations
4. **Z=0 at grip axis** — for all grip milling operations (different zero-point!)
5. **Sine transitions** — all hollow/solid boundaries use cosine interpolation to
   avoid sharp steps that could cause bamboo to split
6. **Glue lands** — solid sections left in hollow strips so the 6 strips can be
   glued together reliably along the full length
7. **LinuxCNC + Mesa 7C81** — hardware step generation on FPGA for reliable timing,
   running on Raspberry Pi
