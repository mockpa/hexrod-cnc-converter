# Mesa 7C81 + 2x Mach3 5-Axis Breakout Board - Connection Plan

## Overview

Connect a Mesa 7C81 FPGA card (on Raspberry Pi) to two Vallder-style
Mach3 5-Axis Breakout Boards using the **5ABOBX2** firmware configuration.

This gives:
- 8 step/dir axes (4 per BOB)
- 2 PWM spindle outputs (0-10V analog)
- 2 encoder inputs
- SSerial expansion on RS-422 (P5/P6)
- 17 GPIO pins on P7

---

## Firmware

- **Bitfile:** `7c81_5abobx2d.bit` (from `7c81.zip`)
- **Pinfile:** `7c81_5abobx2d.pin`

**Official description (from Mesa manual):**
> The 5ABOBX2 configuration is a 8 axis (4 per connector) configuration
> for 2 of the common 5 Axis "Mach 3" BOBs. Both RS-422/RS-485 serial
> ports are used as Sserial I/O expansion. Encoders are available on
> both BOB connectors as are PWM generators for the BOBs analog spindle
> speed interface. The last parallel expansion connector may be used
> for GPIO.

---

## Physical Connections

```
7C81 P1 ---[26-pin IDC to DB25 cable]---> Mach3 BOB #1
7C81 P2 ---[26-pin IDC to DB25 cable]---> Mach3 BOB #2
7C81 P7 --- available for GPIO / future expansion
```

**Cable type:** 26-pin IDC header to DB25 ribbon cable (parallel port style)

---

## Jumper Settings on 7C81

All defaults -- no changes needed for Mach3 BOBs.

| Jumper | Position | Reason |
|--------|----------|--------|
| W1 | UP | 5V tolerance enabled for P1 (default) - BOBs use 5V signals |
| W2 | UP | Pull-up mode for P1 (default) - works with opto-isolated inputs |
| W3 | DOWN | Breakout 5V power DISABLED for P1 (default) - BOB has own PSU |
| W4 | UP | 5V tolerance enabled for P2 (default) |
| W5 | UP | Pull-up mode for P2 (default) |
| W6 | DOWN | Breakout 5V power DISABLED for P2 (default) - BOB has own PSU |
| W11 | UP | Breakout 5V power DISABLED for P7 (default) |
| W12 | DOWN | Pull-up mode for P7 (default) |
| W13 | DOWN | 5V tolerance enabled for P7 (default) |

> **WARNING:** Do NOT enable W3/W6 breakout power. The Mach3 BOBs are NOT
> designed to receive 5V on DB25 pins 22-25. They have their own 12-24V power input.

---

## Pin Mapping - BOB #1 on P1 (StepGen channels 0-3)

| DB25 Pin | 7C81 I/O | Function |
|----------|----------|----------|
| 1 | IO0 | PWM 0 (spindle speed 0-10V analog) |
| 2 | IO2 | StepGen 0 - Step (Axis X) |
| 3 | IO4 | StepGen 0 - Dir (Axis X) |
| 4 | IO6 | StepGen 1 - Step (Axis Y) |
| 5 | IO8 | StepGen 1 - Dir (Axis Y) |
| 6 | IO9 | StepGen 2 - Step (Axis Z) |
| 7 | IO10 | StepGen 2 - Dir (Axis Z) |
| 8 | IO11 | StepGen 3 - Step (Axis A) |
| 9 | IO12 | StepGen 3 - Dir (Axis A) |
| 10 | IO13 | GPIO (input - e.g. limit/home) |
| 11 | IO14 | Encoder 0 - Quad-A |
| 12 | IO15 | Encoder 0 - Quad-B |
| 13 | IO16 | Encoder 0 - Quad-IDX |
| 14 | IO1 | GPIO |
| 15 | IO3 | GPIO |
| 16 | IO5 | GPIO |
| 17 | IO7 | GPIO |
| 18-21 | | GND |
| 22-25 | | GND (do NOT jumper for 5V) |

## Pin Mapping - BOB #2 on P2 (StepGen channels 4-7)

| DB25 Pin | 7C81 I/O | Function |
|----------|----------|----------|
| 1 | IO19 | PWM 1 (spindle speed 0-10V analog) |
| 2 | IO21 | StepGen 4 - Step (Axis X) |
| 3 | IO23 | StepGen 4 - Dir (Axis X) |
| 4 | IO25 | StepGen 5 - Step (Axis Y) |
| 5 | IO27 | StepGen 5 - Dir (Axis Y) |
| 6 | IO28 | StepGen 6 - Step (Axis Z) |
| 7 | IO29 | StepGen 6 - Dir (Axis Z) |
| 8 | IO30 | StepGen 7 - Step (Axis A) |
| 9 | IO31 | StepGen 7 - Dir (Axis A) |
| 10 | IO32 | GPIO (input - e.g. limit/home) |
| 11 | IO33 | Encoder 1 - Quad-A |
| 12 | IO34 | Encoder 1 - Quad-B |
| 13 | IO35 | Encoder 1 - Quad-IDX |
| 14 | IO20 | GPIO |
| 15 | IO22 | GPIO |
| 16 | IO24 | GPIO |
| 17 | IO26 | GPIO |
| 18-21 | | GND |
| 22-25 | | GND (do NOT jumper for 5V) |

---

## Power Supply

| Device | Voltage | Connection |
|--------|---------|------------|
| 7C81 | 5V DC | TB1 screw terminal (pin 1 = +5V, pin 2 = GND) |
| BOB #1 | 12-24V DC | BOB's own power input terminal |
| BOB #2 | 12-24V DC | BOB's own power input terminal |
| Raspberry Pi | 5V | Through 7C81 P4 header (or its own USB-C) |

All power supplies can share a common ground.

---

## Flash Firmware

```bash
# 1. Extract bitfile
cd /home/lurr/Downloads
unzip 7c81.zip 7c81/configs/hostmot2/7c81_5abobx2d.bit

# 2. Flash to 7C81
sudo mesaflash --device 7C81 --spi --addr /dev/spidev0.0 \
  --write 7c81/configs/hostmot2/7c81_5abobx2d.bit

# 3. Verify
sudo mesaflash --device 7C81 --spi --addr /dev/spidev0.0 \
  --verify 7c81/configs/hostmot2/7c81_5abobx2d.bit

# 4. Power cycle the 7C81 / Raspberry Pi after flashing
```

---

## LinuxCNC Driver

- **Driver:** `hm2_rpspi`
- **Load with:** `loadrt hm2_rpspi`
- The driver auto-detects the 5ABOBX2 config and creates HAL pins for all stepgens, encoders, PWM outputs, and GPIO.

---

## Mach3 BOB Stepper Driver Connections

On each Mach3 BOB, connect stepper motor drivers to the axis terminals:
- **PUL+/PUL-** (step signal)
- **DIR+/DIR-** (direction signal)
- Common anode or common cathode depending on driver wiring

BOB input terminals (pins 10-13 on DB25) connect to:
- Limit switches
- Home switches
- E-stop
- Probe / tool setter

BOB relay output can control spindle on/off.
BOB 0-10V analog output (from PWM) controls spindle speed via VFD.

---

## Checklist

- [ ] Extract and flash `7c81_5abobx2d.bit` firmware
- [ ] Build or purchase 2x IDC-26 to DB25 cables
- [ ] Verify jumper settings on 7C81 (all defaults for this setup)
- [ ] Wire BOB #1 to P1, BOB #2 to P2
- [ ] Wire stepper drivers to each BOB
- [ ] Wire limit switches, e-stop, home switches to BOB inputs
- [ ] Wire spindle VFD to BOB analog output
- [ ] Power up and test with `mesaflash --readhmid` to confirm detection
- [ ] Create LinuxCNC HAL and INI configuration
- [ ] Test each axis individually with `halrun`
- [ ] Full system test
