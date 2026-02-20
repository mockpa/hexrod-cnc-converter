# hexrod-cnc

G-Code generators for bamboo fly rod construction on a 2/3-axis LinuxCNC machine.

## Machine Setup

- **X-axis** – along the rod/grip length
- **Z-axis** – horizontal spindle, cuts from below
- **A-axis** – rotary dividing head (stepper motor, optional)

## Tools

### 1. `taper_gcode.py` – Taper G-Code Generator

Converts a hexagonal rod taper (flat-to-flat dimensions at stations) into a
LinuxCNC G-Code program for milling bamboo strips.

```
Usage:
  1. Edit taper_data[] with your station/dimension pairs (inches, mm)
  2. Adjust machine parameters at the top of the file
  3. python3 taper_gcode.py > taper.ngc
```

**Parameters:**
| Variable | Description |
|---|---|
| `taper_data` | List of (station_inches, dimension_mm) tuples |
| `FEED_RATE` | Feed rate in mm/min |
| `Z_RAPID` | Rapid height above workpiece |
| `Z_OFFSET` | Zero-point correction |
| `EXTRA_LAENGE_MM` | Overshoot at butt end |

---

### 2. `hollowing.py` – Hollow Milling G-Code Generator

Mills the inner hollow (pith side) of bamboo strips using a flat end mill,
leaving solid glue lands at regular intervals and solid sections at tip and butt.

```
Usage:
  1. Edit taper_data[] and hollowing parameters
  2. python3 hollowing.py > hollowing.ngc
```

**Parameters:**
| Variable | Description |
|---|---|
| `TIP_SOLID_MM` | Length left solid at tip end (mm) |
| `BUTT_SOLID_MM` | Length left solid at butt end (mm) |
| `STEG_ABSTAND_MM` | Distance between glue lands (center to center) |
| `STEG_BREITE_MM` | Width of each glue land (mm) |
| `UEBERGANG_MM` | Sine transition zone length (mm) |
| `WANDSTAERKE_MM` | Remaining wall thickness / power fiber layer (mm) |
| `SCHRITT_MM` | Toolpath resolution (1mm recommended) |

**Glue land profile:**
```
Z=0  ___     ___     ___     ___   ← solid (glue land)
        |   |   |   |   |   |
Z=-d    |___|   |___|   |___|      ← hollow
        Sine transitions in/out
```

---

### 3. `griff_generator.py` – Grip G-Code Generator

Generates G-Code for milling cork or wood grips using a rotary A-axis (dividing
head). Spindle is horizontal, cutting from below the workpiece.

Supports three grip types:

#### Cylindrical / Conical
A-axis rotates continuously while X and Z move simultaneously — effectively
turning on a lathe. Multiple roughing passes followed by a finishing pass.

#### Polygon (e.g. octagon)
A-axis indexes to each face angle, then X mills the full grip length at constant Z.

```
Usage:
  1. Set GRIFFTYP = "zylindrisch" | "konisch" | "polygon"
  2. Set grip dimensions and machine parameters
  3. python3 griff_generator.py > griff.ngc
```

**Parameters:**
| Variable | Description |
|---|---|
| `GRIFFTYP` | `"zylindrisch"`, `"konisch"`, or `"polygon"` |
| `GRIFF_LAENGE_MM` | Total grip length (mm) |
| `ROHLING_RADIUS` | Blank radius before milling (mm) |
| `FRAESER_RADIUS` | End mill radius (mm) |
| `ZIEL_RADIUS` | Target radius for cylindrical grip (mm) |
| `RADIUS_TIP` / `RADIUS_BUTT` | Tip and butt radii for conical grip (mm) |
| `POLYGON_SEITEN` | Number of polygon faces (6, 8, ...) |
| `POLYGON_UMKREIS` | Circumradius of finished polygon (mm) |

**Coordinate system (horizontal spindle, cutting from below):**
```
Z = 0 → grip axis (center of rotation)
Z > 0 → away from grip axis (toward spindle)
Z = target_radius + tool_radius → cutting position
```

**Important:** Set Z zero-point at the grip axis (center of the dividing head),
not at the blank surface.

---

## LinuxCNC Configuration

### A-axis (INI excerpt)

```ini
[TRAJ]
AXES = 4
COORDINATES = X Z A

[AXIS_A]
TYPE = ANGULAR
MAX_VELOCITY = 360
MAX_ACCELERATION = 720
WRAPPED_ROTARY = 1       ; for indexing only
; set WRAPPED_ROTARY = 0 for continuous turning (cylindrical/conical)

[JOINT_3]
TYPE = ANGULAR
HOME = 0.0
MAX_VELOCITY = 360
MAX_ACCELERATION = 720
SCALE = 177.78           ; adjust: (steps * microsteps * ratio) / 360
STEPLEN = 1000
STEPSPACE = 1000
DIRHOLD = 2000
DIRSETUP = 2000
HOME_SEQUENCE = -1
```

**SCALE calculation:**
```
SCALE = (Steps/rev × Microsteps × GearRatio) / 360
Example: 200 × 16 × 2 / 360 = 17.78  (no reduction)
         200 × 16 × 18 / 360 = 160    (18:1 reduction)
```

### HAL (Mesa 7C81, channel 3)

```tcl
setp hm2_rpspi.0.stepgen.03.step_type 0
net a-pos-cmd  joint.3.motor-pos-cmd  => hm2_rpspi.0.stepgen.03.position-cmd
net a-pos-fb   joint.3.motor-pos-fb   <= hm2_rpspi.0.stepgen.03.position-fb
net a-enable   joint.3.amp-enable-out => hm2_rpspi.0.stepgen.03.enable
setp hm2_rpspi.0.stepgen.03.maxvel    360
setp hm2_rpspi.0.stepgen.03.maxaccel  720
```

---

## Workflow

```
1. Measure or enter taper data
        ↓
2. Generate taper G-code (taper_gcode.py)
        ↓
3. Generate hollowing G-code (hollowing.py)
        ↓
4. Dry run both programs (no workpiece, spindle off)
        ↓
5. Test cut on scrap wood/MDF, verify dimensions with calipers
        ↓
6. Mill bamboo strips
        ↓
7. (Optional) Mill cork/wood grip with griff_generator.py + A-axis
```

---

## Requirements

- Python 3.6+
- LinuxCNC 2.8+ with Mesa 7C81 (hm2_rpspi driver)
- No external Python packages required
