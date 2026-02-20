# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a G-code generation toolkit for bamboo fly rod manufacturing on a CNC mill running LinuxCNC with a Mesa 7C81 FPGA card on a Raspberry Pi.

## Running the Scripts

All three generators are pure Python 3 (no external dependencies). Edit parameters directly in the script, then run and redirect output:

```bash
python3 taper_gcode.py > taper.ngc
python3 hollowing.py > hollowing.ngc
python3 griff_generator.py > griff.ngc
```

Generated `.ngc` files are git-ignored. All scripts use LF line endings (enforced by `.gitattributes`).

## Architecture

Three standalone G-code generators, each parameterized at the top of the file:

### taper_gcode.py
Converts a `taper_data[]` list of `(station_inches, dimension_mm)` tuples into Z-depth cuts along the X-axis via linear interpolation. Produces the hexagonal rod taper profile.

### hollowing.py
Mills the pith-side hollow while preserving solid tip/butt sections and periodic glue lands. Uses sine-curve transitions between hollow and solid sections. Wall thickness tracks the taper automatically (references same `taper_data[]` format).

Key parameters: `TIP_SOLID_MM`, `BUTT_SOLID_MM`, `STEG_ABSTAND_MM` (glue land spacing), `STEG_BREITE_MM` (glue land width), `UEBERGANG_MM` (transition zone), `WANDSTAERKE_MM` (wall thickness), `SCHRITT_MM` (step resolution).

### griff_generator.py
Mills cork/wood grips using a horizontal spindle cutting from below. Controlled by `GRIFFTYP`:
- `zylindrisch` — constant radius, continuous A-axis rotation
- `konisch` — linear radius tip-to-butt, continuous rotation
- `polygon` — regular polygon faces (e.g. 6 or 8-sided), indexed A-axis positioning

Performs roughing passes then a finishing pass.

## Machine Coordinate System

- **X-axis**: Rod/grip length
- **Z-axis**: Cut depth (negative = cutting into material)
- **A-axis**: Rotary dividing head (stepper, 0–360°), used for grip milling

## LinuxCNC Configuration

`linuxcnc/hexrod.ini` — Machine configuration (3-axis: X, Z, optional A).
`linuxcnc/hexrod.hal` — HAL wiring connecting LinuxCNC motion controller to Mesa 7C81 stepgen channels and GPIO home switches via `hm2_rpspi` driver.

## Mesa 7C81 Firmware Flash

```bash
sudo mesaflash --device 7C81 --spi --addr /dev/spidev0.0 \
  --write 7c81/configs/hostmot2/7c81_5abobx2d.bit
sudo mesaflash --device 7C81 --spi --addr /dev/spidev0.0 \
  --verify 7c81/configs/hostmot2/7c81_5abobx2d.bit
```

Hardware pin mapping details are in `../7c81_2x_mach3bob_plan.md`.
