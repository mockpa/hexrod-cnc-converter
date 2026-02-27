# YL42 High Performance Universal Frequency Converter — Product Manual

---

## Contents

1. [Chapter 1: Product Information](#chapter-1-product-information)
2. [Chapter 2: Electrical Installation](#chapter-2-electrical-installation)
3. [Chapter 3: Operation Display](#chapter-3-operation-display)
4. [Chapter 4: Function Parameter Table](#chapter-4-function-parameter-table)
5. [Chapter 5: Fault Diagnosis and Countermeasures](#chapter-5-fault-diagnosis-and-countermeasures)

---

## Chapter 1: Product Information

### 1.1 Safety Information and Precautions

Safety precautions are divided into two categories:
- **Danger**: Failure to operate as required may cause serious injury or death.
- **Note**: Failure to operate as required may result in moderate or minor injury and equipment damage.

Read this chapter carefully when installing, debugging, and servicing. Any injuries and losses caused by illegal operations are not the company's responsibility.

---

### 1.2 Naming Rules

```
YL42  [voltage]  [power kW]  [motor type]  [brake]
```

| Field | Mark | Meaning |
|-------|------|---------|
| Series | YL42 | YL42 Inverter series |
| Voltage | S | Single-phase 220V |
| | -2T | Three-phase 220V |
| | T | Three-phase 380V |
| | -5T | Three-phase 480V |
| | -7T | Three-phase 690V |
| Power (kW) | — | 0.4 / 0.75 / 1.5 / 2.2 / 3.7 / 5.5 / 7.5 |
| Motor type | G | Universal type |
| | P | Fan/pump type |
| Brake unit | blank | No brake unit |
| | B | Brake unit included |

**Example**: `YL42 T 0.75 G B` = Three-phase 380V, 0.75kW, universal type, with brake unit.

**Nameplate example**:
```
MODEL:  YL42 T 0.75 G B   CE
INPUT:  3PH AC380-440V 3.4A 50/60HZ
OUTPUT: 3PHAC0-440V 2.4A 0-3.2KHZ
S/N:    XXXXXXXXXXXXXXXXXXXXXX
```

---

### 1.4 YL Inverter Series Index

#### Single-phase 220V, 50/60Hz

| Model | KVA | Input A | Output A | kW | HP |
|-------|-----|---------|----------|----|----|
| YL42-2T0.7GB | 1.5 | 8.2 | 4.0 | 0.75 | 1 |
| YL42-2T1.5GB | 3.0 | 14.0 | 7.0 | 1.5 | 2 |
| YL42-2T2.2GB | 4.0 | 23.0 | 9.6 | 2.2 | 3 |
| YL42-2T3.7GB | 5.5 | 31.0 | 17 | 3.7 | 4 |
| YL42-2T5.5GB | 8.9 | 26.0 | 25 | 5.5 | 5 |
| YL42-2T7.5GB | 21 | 35 | 32 | 7.5 | 10 |
| YL42-2T11GB | 30 | 46.5 | 45 | 11 | 15 |

#### Three-phase 380V, 50/60Hz

| Model | KVA | Input A | Output A | kW | HP |
|-------|-----|---------|----------|----|----|
| YL42-T0.7GB | 1.5 | 3.4 | 2.1 | 0.75 | 1 |
| YL42-T1.5GB | 3.0 | 5.0 | 3.8 | 1.5 | 2 |
| YL42-T2.2GB | 4.0 | 5.4 | 5.1 | 2.2 | 3 |
| YL42-T3.0GB | 5.0 | 8.5 | 7.0 | 3.0 | 4 |
| YL42-T3.7GB | 5.9 | 10.5 | 9.0 | 3.7 | 5 |
| YL42-T5.5GB | 8.9 | 14.6 | 13.0 | 5.5 | 7.5 |
| YL42-T7.5GB | 11.0 | 20.5 | 17.0 | 7.5 | 10 |
| YL42-T11GB | 17.0 | 26.0 | 25.0 | 11.0 | 15 |
| YL42-T15GB | 21.0 | 35.0 | 32.0 | 15.0 | 20 |
| YL42-T18.5GB | 24.0 | 38.5 | 37.0 | 18.5 | 25 |
| YL42-T22GB | 30.0 | 46.5 | 45.0 | 22 | 30 |
| YL42-T30GB | 40.0 | 62.0 | 60.0 | 30 | 40 |
| YL42-T37G | 57.0 | 76.0 | 75.0 | 37 | 50 |
| YL42-T45G | 69.0 | 92.0 | 91.0 | 45 | 60 |

---

### 1.5 Product Appearance, Installation Hole Size

Plastic structure (small units): ~85mm W × 116/135mm H × 75/136mm D (varies by power rating). Refer to Figure 1-2 in the original manual for exact dimensions.

---

### 1.6 Warranty Instructions

- Free warranty: 12 months from date of manufacture/delivery (barcode on fuselage).
- Maintenance fee charged after 12 months or for:
  1. Damage caused by not following manual regulations.
  2. Damage from fire, flood, abnormal voltage, etc.
  3. Damage from abnormal use.
  4. Service fee per manufacturer's unified standard; contract terms take priority.

---

## Chapter 2: Electrical Installation

### 2.1.1 Main Circuit Terminals and Wiring

| Terminal | Name | Description |
|----------|------|-------------|
| R, S, T | Power input | Single/three-phase AC power connection |
| P, PB | Braking resistor | Connect braking resistor |
| U, V, W | Inverter output | Connected to three-phase motor |
| ⏚ | Ground | Grounding connection |

---

### 2.1.2 Wiring Mode of Inverter Control Circuit

Key points from the wiring diagram:
- **Three-phase power input**: R, S, T → through circuit breaker → inverter
- **Motor output**: U, V, W → three-phase induction motor
- **Braking resistor**: connected between P and PB terminals
- **+10V**: reference supply for external potentiometer (1kΩ–5kΩ)
- **AI1, AI2**: analog inputs, DC 0–10V or 0/4–20mA
- **X1–X7**: multifunction digital inputs
- **X5 (HDI)**: high-speed pulse input (up to 50kHz)
- **Y1**: open-collector output
- **HDO**: high-speed pulse output (up to 50kHz)
- **AO1, AO2**: analog outputs (0–10V)
- **TA1/TA2, TB1/TB2, TC1/TC2**: Relay R1 and R2 outputs
- **485+, 485–**: RS-485 communication

> **Note**: The X terminal of YL42 mainboard can be X5 at most. AO2 has voltage output only (no current). Terminal shared with Y1 is switched by J1.

---

### 2.1.3 Control Terminal Layout

Two versions:
- **Non-isolated**: COM terminal is actually connected to GND.
- **Isolated**: optical coupling isolation; supports NPN/PNP input switching; J4 jumper selects isolation mode.

Terminal row (top): `A+ B- GND AI1 AI2 10V AO1 Y1 K1A K1B K1C`
Terminal row (bottom): `+24V-COM X1 X2 X3 X4 HDI HDO K2A K2B K2C`

---

### 2.1.4 Function Description of Control Terminals

| Type | Terminal | Name | Function |
|------|----------|------|----------|
| Power | +10V–GND | +10V supply | +10V for external potentiometer (1kΩ–5kΩ), max 150mA |
| Power | +24V–COM | +24V supply | Supply for DI/DO and sensors, max 200mA |
| Analog | AI1–GND | Analog input 1 | DC 0–10V / 0–20mA (P4-37); 22kΩ voltage / 500Ω current impedance |
| Analog | AI2–GND | Analog input 2 | Same as AI1 |
| Analog | AO1–GND | Analog output 1 | 0–10V / 0–20mA (4–20mA optional via PS-23) |
| Analog | AO2–GND | Analog output 2 | 0–10V only (no current output on YL42) |
| Digital | X1–COM | Digital input 1 | Multifunction input |
| Digital | X2–COM | Digital input 2 | Multifunction input |
| Digital | X3–COM | Digital input 3 | Multifunction input |
| Digital | X4–COM | Digital input 4 | Multifunction input |
| Digital | HDI–COM (X5) | Digital input 5 / High-speed pulse | Same as X1–X4 plus high-speed pulse up to 50kHz; impedance 1kΩ; 5–30V |
| Comm | A+, B– | RS-485 | A+ differential positive, B– differential negative |
| Digital out | Y1–COM | Open-collector output | J1 jumper selects Y1 or AO2 on isolated board |
| Digital out | HDO–COM | High-speed pulse output | Up to 50kHz; or open-collector like Y1 (set by P5-00) |
| Relay | K1A–K1B–K1C | Relay 1 | A=common, B=NC, C=NO; AC250V 3A cosφ=0.4; DC30V 1A |
| Relay | K2A–K2B–K2C | Relay 2 | Same ratings as Relay 1 |

---

### 2.1.5 Wiring Instructions for Signal Input Terminals

- Analog signals are susceptible to interference — use shielded cable, max 20m.
- If severely disturbed, add a filter capacitor or ferrite magnet at the signal source.

---

## Chapter 3: Operation Display

### 3.1 Operation Panel Layout

```
┌─────────────────────────────┐
│  RUN ● [8.8.8.8.8] Hz  A   │  ← Upper display (5-digit LED)
│  L/R ●  FWD ●  TUNE ●      │
│  [8.8.8.8.8]               │  ← Lower display (monitoring)
│                    [knob]   │
│ [PRG] [▲] [▼] [▶] [MFK] [ENTER] │
│              [RUN] [STOP/RST]   │
└─────────────────────────────┘
```

#### Status Indicator LEDs

| LED | Off | On | Flashing |
|-----|-----|----|---------|
| RUN | Stopped | Running | — |
| LOCAL/REMOTE | Panel control | Terminal control | Communication control |
| FWD/REV | — | Forward rotation | — |
| TUNE/TC | — | Torque control mode | Slow=harmonic; Fast=fault |

#### Unit Indicators

| Display | Unit |
|---------|------|
| Hz | Frequency |
| A | Current |
| V | Voltage |
| RPM/Hz·A | Speed |
| % (A·V) | Percentage |

#### Keyboard Function Table

| Key | Name | Function |
|-----|------|----------|
| PRG | Programming | Enter/exit first-level menu |
| ENTER | Confirm | Enter menu level / confirm parameter |
| ▲ | Increment | Increment data or function code |
| ▼ | Decrement | Decrement data or function code |
| ▶ | Shift | Select displayed parameter (STOP/RUN); select digit to modify |
| RUN | Run | Start in keyboard operation mode |
| STOP/RES | Stop/Reset | Stop running; reset in FAULT state (can be restricted by P7-02) |
| MFK | Multifunction | Function switchover as defined by P7-01 |

---

## Chapter 4: Function Parameter Table

**Attribute symbols**:
- ☆ = Can be changed in stop or running state
- ★ = Cannot be changed while running
- • = Actual test record value, cannot be changed

---

### P0 Group: Basic Parameters

| Code | Name | Setting Range | Default | Attr |
|------|------|--------------|---------|------|
| P0-00 | G/P model | 1: G model; 2: P model | 1 | ★ |
| P0-01 | Motor control mode | 0: Vector (no sensor); 2: V/F control | 2 | ★ |
| P0-02 | Command source | 0: Panel (LED off); 1: Terminal (LED on); 2: Communication (LED flash) | 0 | ☆ |
| P0-03 | Main frequency source X | 0: Digital (P0-08, non-retentive); 1: Digital (P0-08, retentive); 2: AI1; 3: AI2; 4: AI3 (keyboard pot); 5: HDI pulse; 6: Multi-segment; 7: Simple PLC; 8: PID; 9: Communication | 4 | ★ |
| P0-04 | Auxiliary frequency source Y | Same as P0-03 | 0 | ★ |
| P0-05 | Frequency Y range reference | 0: Relative to max frequency; 1: Relative to frequency source X | 0 | ☆ |
| P0-06 | Frequency Y range % | 0%–150% | 100% | ☆ |
| P0-07 | Frequency source superposition mode | Ones: 0=X only; 1=X+Y; 2=Switch X/Y; 3=Switch X/X+Y; 4=Switch Y/X+Y. Tens: 0=Main+aux; 1=Main−aux; 2=Max; 3=Min; 4=Main×aux; 5=Main+aux | 00 | ☆ |
| P0-08 | Preset frequency | 0.00Hz – max frequency (P0-10) | 50.00Hz | ☆ |
| P0-09 | Running direction | 0: Same; 1: Reverse | 0 | ☆ |
| P0-10 | Maximum frequency | 50.00–3200.00Hz (P0-22=2); 50.00–3200.00Hz (P0-22=1) | 50.00Hz | ★ |
| P0-11 | Upper limit frequency source | 0: P0-12; 1: AI1; 2: AI2; 3: AI3 pot; 4: HDI; 5: Communication | 0 | ★ |
| P0-12 | Upper limit frequency | Lower limit (P0-14) – max (P0-10) | 50.00Hz | ☆ |
| P0-13 | Upper limit frequency offset | 0.00Hz – max (P0-10) | 0.00Hz | ☆ |
| P0-14 | Lower limit frequency | 0.00Hz – upper limit (P0-12) | 0.00Hz | ☆ |
| P0-15 | Carrier frequency | 0.5kHz – 16.0kHz | Model dependent | ☆ |
| P0-16 | Carrier freq adjusts with temperature | 0: No; 1: Yes | 1 | ☆ |
| P0-17 | Acceleration time 1 | 0s – 65000s (P0-19=0) | Model dependent | ☆ |
| P0-18 | Deceleration time 1 | 0.0s – 6500.0s (P0-19=1); 0.00s – 650.00s (P0-19=2) | Model dependent | ☆ |
| P0-19 | Accel/decel time unit | 0: 1s; 1: 0.1s; 2: 0.01s | 1 | ★ |
| P0-21 | Aux freq offset when superimposing | 0.00Hz – max (P0-10) | 0.00Hz | ☆ |
| P0-22 | Frequency instruction resolution | 1: 0.1Hz; 2: 0.01Hz (note: set to 1 for high-frequency output) | 2 | ★ |
| P0-23 | Digital frequency shutdown memory | 0: No memory; 1: Memory | 1 | ☆ |
| P0-25 | Base frequency for accel/decel | 0: Max frequency (P0-10); 1: Set frequency | 0 | ★ |
| P0-26 | Freq UP/DOWN reference during run | 0: Operating frequency; 1: Set frequency | 0 | ★ |
| P0-27 | Command source binding frequency source | Ones: panel binding; Tens: terminal binding; Hundreds: communication binding; Thousands: auto binding (0–9 same options as P0-03) | 0000 | ☆ |
| P0-29 | Industry Application Macro | 0: Factory default (P0-29=10000 to restore factory params); 1: Constant pressure water supply (one pump); 2: One-drag-three constant pressure water supply; 3: One-drag-five constant pressure water supply; 7: Fire water supply inspection cabinet; 11: CNC 100Hz macro 1; 12: CNC 100Hz macro 2; 17: Spindle 300Hz macro 1; 18: Spindle 300Hz macro 2; 21: Linear multi-stage speed / engraving machine 400Hz macro (P7-16=0.15 or above) | 0 | ☆ |

---

### P1 Group: Motor Parameters

| Code | Name | Setting Range | Default | Attr |
|------|------|--------------|---------|------|
| P1-00 | Motor type | 0: Ordinary async; 1: Variable freq async; 2: PMSM (separate manual) | 0 | ★ |
| P1-01 | Motor rated power | 0.1–1000kW | Model | ★ |
| P1-02 | Motor rated voltage | 1–380V | Model | ★ |
| P1-03 | Motor rated current | 0.01–100.00A | Model | ★ |
| P1-04 | Motor rated frequency | 0.01Hz – max frequency | Model | ★ |
| P1-05 | Motor rated speed | 1–65535 rpm | Model | ★ |
| P1-10 | Async motor no-load current | 0.01–P1-03 | Tuning params | ★ |
| P1-37 | Tuning options | 0: None; 1: Static tuning; 2: Complete tuning; 3: Static tuning 2 | 0 | ★ |

---

### P2 Group: Vector Parameters

| Code | Name | Setting Range | Default | Attr |
|------|------|--------------|---------|------|
| P2-00 | Speed loop proportional gain 1 | 1–100 | 30 | ☆ |
| P2-01 | Speed loop integral time 1 | 0.01–10.0s | 0.50s | ☆ |
| P2-02 | Switching frequency 1 | 0.00–P2-05 | 3.00Hz | ☆ |
| P2-03 | Speed loop proportional gain 2 | 1–100 | 20 | ☆ |
| P2-04 | Speed loop integral time 2 | 0.01s–10.00s | 1.00s | ☆ |
| P2-05 | Switching frequency 2 | P2-02 – max frequency | 10.00Hz | ☆ |
| P2-06 | Vector control slip gain | 50–200% | 150% | ☆ |
| P2-07 | Speed loop filter time | 0.000–0.100s | 0.000s | ☆ |
| P2-08 | Vector control overexcitation gain | 0–200 | 64 | ☆ |
| P2-09 | Torque upper limit source (speed ctrl) | 0: P2-10; 1: AI1; 2: AI2; 3: Keyboard pot; 4: PULSE; 5: Communication; 6: MIN(AI1,AI2); 7: MAX(AI1,AI2) | 0 | ☆ |
| P2-10 | Torque upper limit (speed ctrl) | 0.0%–200.0% | 150.0% | ☆ |
| P2-13 | Excitation adjustment proportional gain | 0–60000 | 2000 | ☆ |
| P2-14 | Excitation adjustment integral gain | 0–60000 | 1300 | ☆ |
| P2-15 | Torque adjustment proportional gain | 0–60000 | 2000 | ☆ |
| P2-16 | Torque adjustment integral gain | 0–60000 | 1300 | ☆ |
| P2-17 | Speed loop integral properties | Ones: 0=integral separation invalid; 1=effective | 0 | ☆ |

---

### P3 Group: V/F Control Parameters

| Code | Name | Setting Range | Default | Attr |
|------|------|--------------|---------|------|
| P3-00 | VF curve | 0: Linear; 1: Multipoint; 2: Square; 3: 1.2 power; 4: 1.4 power; 6: 1.6 power; 8: 1.8 power; 10: Fully separated; 11: Semi-separated | 0 | ★ |
| P3-01 | Torque boost | 0.0% (auto); 0.1–30.0% | Model | ☆ |
| P3-02 | Torque boost cut-off frequency | 0.00Hz – max frequency | 50.00Hz | ★ |
| P3-03 | Multipoint VF frequency point 1 | 0.00Hz – P3-05 | 0.00Hz | ★ |
| P3-04 | Multipoint VF voltage point 1 | 0.0%–100.0% | 0.0% | ★ |
| P3-05 | Multipoint VF frequency point 2 | P3-03 – P3-07 | 0.00Hz | ★ |
| P3-06 | Multipoint VF voltage point 2 | 0.0%–100.0% | 0.0% | ★ |
| P3-07 | Multipoint VF frequency point 3 | P3-05 – motor rated freq (P1-04) | 0.00Hz | ★ |
| P3-08 | Multipoint VF voltage point 3 | 0.0%–100.0% | 0.0% | ★ |
| P3-09 | VF slip compensation gain | 0.0%–200.0% | 0.0% | ☆ |
| P3-10 | VF overexcitation gain | 0–200 | 64 | ☆ |
| P3-11 | VF oscillation suppression gain | 0–100 | Model | ☆ |

---

### P4 Group: Input Terminal Parameters

| Code | Name | Setting Range | Default | Attr |
|------|------|--------------|---------|------|
| P4-00 | X1 terminal function | 0: No function; 1: FWD; 2: REV; 3: Three-wire; 4: FJOG; 5: RJOG; 6: Terminal UP; 7: Terminal DOWN; 8: Free stop; 9: Fault reset; 10: Running pause; 11: External fault NO; 12–15: Multi-segment cmd 1–4; 16: Accel/decel time sel 1; 17: Accel/decel time sel 2; 18: Freq source switch; 19: UP/DOWN clear; 20: Run cmd switch terminal 1; 21: Accel/decel prohibited; 22: PID pause; 23: PLC state reset; 24: Swing freq pause; 25: Counter input; 26: Counter reset; 27: Length counting; 28: Length reset; 29: Torque control prohibited; 30: HDI pulse freq input (DI5); 31: Reserved; 32: Immediate DC braking; 33: External fault NC; 34: Freq modification enable; 35: PID direction reverse; 36: External stop terminal 1; 37: Run cmd switch terminal 2; 38: PID integral pause; 39: Freq source X and preset switch; 40: Freq source Y and preset switch; 41–54: see manual | 1 | ★ |
| P4-01 | X2 terminal function | Same options as P4-00 | 2 | ★ |
| P4-02 | X3 terminal function | Same options as P4-00 | 4 | ★ |
| P4-03 | X4 terminal function | Same options as P4-00 | 6 | ★ |
| P4-04 | X5 (HDI) terminal function | Same options + 47: Emergency stop; 48: External stop 2; 49: Deceleration DC braking; 50: Clear running time; 51: Two/three wire switch; 52: Reverse prohibited; 53: Single terminal UP/DOWN; 54: Terminal activated UP only | 12 | ★ |
| P4-05 | X6 terminal function | Same options | 00 | ★ |
| P4-06 | X7 terminal function | Same options | 00 | ★ |
| P4-10 | X terminal filtering time | 0.000s–1.000s | 0.010s | ☆ |
| P4-11 | Terminal command mode | 0: Two-wire 1; 1: Two-wire 2; 2: Three-wire 1; 3: Three-wire 2 | 0 | ★ |
| P4-12 | Terminal UP/DOWN change rate | 0.001Hz/s–65.535Hz/s | 1.00Hz/s | ☆ |
| P4-13 | AI1 curve 1 minimum input | 0.00V–P4-15 | 0.00V | ☆ |
| P4-14 | AI1 curve 1 min input setting | -100.0%–100.0% | 0.0% | ☆ |
| P4-15 | AI1 curve 1 maximum input | P4-13–10.00V | 10.00V | ☆ |
| P4-16 | AI1 curve 1 max input setting | -100.0%–100.0% | 100.0% | ☆ |
| P4-17 | AI1 filter time | 0.00s–10.0s | 0.10s | ☆ |
| P4-18 | AI2 curve 2 minimum input | 0.00V–P4-20 | 0.00V | ☆ |
| P4-19 | AI2 curve 2 min input setting | -100.0%–100.0% | 0.0% | ☆ |
| P4-20 | AI2 curve 2 maximum input | P4-18–10.00V | 10.00V | ☆ |
| P4-21 | AI2 curve 2 max input setting | -100.0%–100.0% | 100.0% | ☆ |
| P4-22 | AI2 filter time | 0.00s–10.00s | 0.10s | ☆ |
| P4-23 | AI1 curve minimum input corresponding | -100.0%–100.0% | -100.0% | ☆ |
| P4-25 | AI curve selection | Ones: AI1 curve (1=curve1, 2=curve2, 3=curve3); Tens: AI2 curve; Hundreds: AI3 | 321 | ☆ |
| P4-30 | AI lower than minimum handling | 000: Ones=AI1 (0=min setting, 1=0.0%); Tens=AI2; Hundreds=AI3 | 000 | ☆ |
| P4-35 | X terminal effective mode | Ones: X1 high=valid; Tens: X2; Hundreds: X3; Thousands: X4; Ten-thousands: X5; Hundred-thousands: X6; (0=high active, 1=low active, voltage input) | 10 | ★ |
| P4-37 | All input voltage/current mode selection | Ones: AI1; Tens: AI2; Hundreds: AI3 (0=voltage, 1=current) | — | ★ |
| P4-40–P4-50 | X1–X7 on/off delay times | 0.0s–655.3s | 0.0s | ★ |

---

### P5 Group: Output Terminal Parameters

| Code | Name | Setting Range | Default | Attr |
|------|------|--------------|---------|------|
| P5-00 | HDO terminal output mode | 0: High-speed pulse output (HDO); 1: Open-collector output (like Y1) | 0 | ★ |
| P5-01 | Relay RY1 function (K1A-K1B-K1C) | 0: No output; 1: In operation; 2: Freq reached; 3: Zero speed (no output at stop); 4: Freq reached (output at stop); 5: Overload pre-alarm; 6: Motor overload pre-alarm; 7: Inverter overload pre-alarm; 8: Set count value reached; 9: Defined count reached; 10: Running pause; 11: PLC cycle complete; 12: Freq limiting; 13: Torque limiting; 14: Accumulated runtime reached; 15: Lower limit freq reached (at stop); 16: Ready to run; 17: AI1–AI2; 18: Communication; 19: Zero speed running; 20: Zero speed operation 2 (also output at stop); 21–41: see manual | 1 | ☆ |
| P5-02 | Relay RY2 function (K2A-K2B-K2C) | Same options as P5-01 | 4 | ☆ |
| P5-03 | Y terminal output function | Same options | — | ☆ |
| P5-04 | Y2 output function | Same options | — | ☆ |
| P5-06 | AO1 output function | 0: Operating freq; 1: Setting freq; 2: Output current; 3: Torque; 4: Output power; 5: HDI pulse input; 6: AI1; 7: AI2; 8: AI3; 9: AO1; 10: AO2 = 100%; 11: Motor speed; 12: Communication; 13: Motor speed; 14: Output torque; 15: Output voltage (100%=1000V); 16: Reserved; 17: Inverter output torque | 0 | ☆ |
| P5-07 | AO2 output function | Same options | 0 | ☆ |
| P5-08 | HDO output function | Same as AO1 options | 0 | ☆ |
| P5-09 | HDO output maximum frequency | 0.01kHz–50.0kHz | 50.0kHz | ☆ |
| P5-10 | AO1 zero bias factor | -100.0%–100.0% | 0.0% | ☆ |
| P5-11 | AO1 gain | -10.00–10.00 | 1.00 | ☆ |
| P5-12 | AO2 zero bias factor | -100.0%–100.0% | 0.0% | ☆ |
| P5-13 | AO2 gain | -10.00–10.00 | 1.00 | ☆ |
| P5-17 | FMR delayed closing time | 0.0s–655.3s | 0.0s | ☆ |
| P5-18 | RY1 delayed closing time | 0.0s–655.3s | 0.0s | ☆ |
| P5-19 | RY2 delayed closing time | 0.0s–655.3s | 0.0s | ☆ |
| P5-20 | RY2 delayed opening time | 0.0s–655.3s | 0.0s | ☆ |
| P5-22 | Y terminal output valid status | Ones: Y1 (0=positive, 1=negative logic); Tens: HDO; Hundreds: RY1; Thousands: RY2 | 0000 | ☆ |

---

### P6 Group: Start and Stop Control

| Code | Name | Setting Range | Default | Attr |
|------|------|--------------|---------|------|
| P6-00 | Start method | 0: Direct start; 1: Speed tracking restart; 2: Pre-excitation start (AC async) | 0 | ★ |
| P6-01 | Speed tracking method | 0: Start from stop freq; 1: Start from zero speed; 2: Start from max frequency | 0 | ★ |
| P6-02 | Speed tracking speed | 1–100 | 20 | ☆ |
| P6-03 | Start frequency | 0.00–10.00Hz | 0.00Hz | ☆ |
| P6-04 | Start frequency hold time | 0.0s–100.0s | 0.0s | ☆ |
| P6-05 | Start DC braking / pre-excitation current | 0%–100% | 0% | ★ |
| P6-06 | Start DC braking / pre-excitation time | 0.0s–100.0s | 0.0s | ★ |
| P6-07 | Acceleration and deceleration method | 0: Linear; 1: S-curve accel/decel A; 2: S-curve accel/decel B | 0 | ★ |
| P6-08 | S-curve start time ratio | 0.0%–(100.0%-P6-09) | 30.0% | ★ |
| P6-09 | S-curve end time ratio | 0.0%–(100.0%-P6-08) | 30.0% | ★ |
| P6-10 | Stop mode | 0: Decelerate to stop; 1: Free stop | 0 | ☆ |
| P6-11 | Stop DC braking start frequency | 0.00Hz – max frequency | 0.00Hz | ☆ |
| P6-12 | Stop DC braking wait time | 0.0s–100.0s | 0.0s | ☆ |
| P6-13 | Stop DC braking current | 0%–100% | 0% | ☆ |
| P6-14 | Stop DC braking time | 0.0s–100.0s | 0.0s | ☆ |
| P6-15 | Stop DC brake usage rate | 0%–100% | 100% | ☆ |
| P6-40 | Display function selection 1 | — | — | ☆ |
| P6-41 | MF key function selection | 0: No function; 1: Input AI/bus voltage display; 2: Fwd/rev switch (comm channel); 3: Fwd/rev switching | 0 | ☆ |

---

### P7 Group: Keyboard and Display

| Code | Name | Setting Range | Default | Attr |
|------|------|--------------|---------|------|
| P7-02 | STOP/RESET key function | 0: Only in keyboard operation mode, the stop function is valid; 1: In any operation mode, the stop function is valid | — | ☆ |
| P7-03 | LED running display parameter 1 | Bit00: Operating freq (Hz); Bit01: Set freq (Hz); Bit02: Bus voltage (V); Bit03: Output voltage (V); Bit04: Output current (A); Bit05: Output power (kW); Bit06: Output torque (%); Bit07: DI input status; Bit08: DO output status; Bit09: AI1 voltage (V); Bit10: AI2 voltage (V); Bit11: AI3 pot voltage (V); Bit12: Count value; Bit13: Length; Bit14: Load speed; Bit15: PID setting | 001F | ☆ |
| P7-04 | LED stop display parameter | Bit00: Set freq (Hz); Bit01: Bus voltage (V); Bit02: DI input status; Bit03: DO output; Bit04: AI1 voltage; Bit05: AI2 voltage; Bit06: AI3 pot; Bit07: Communication setting; Bit08: Output power; Bit09: AI2 auxiliary motor pump; Bit10: Linkage X1 terminal output; Bit11: Linkage X2 terminal output; Bit12: Linkage X3 terminal output; Bit13: Linkage X4 terminal; Bit14: Linkage X5 terminal; Bit15: Set freq (Hz) for reference | 001F | ☆ |
| P7-40 | LED running display parameter 2 | Bit00: AI3; Bit01: AI2; Bit02: AI1; Bit03: Setting freq (Y); Bit04: Setting freq (X); Bit05: Main/aux freq display (Hz, Hi14); Bit06: Comms setting value (Hi13); Bit07: Current power-on time; Bit08: Current running time; Bit09: HDI input pulse freq; Bit10: Comms settings; Bit11: Main freq X display (Hz); Bit12: Motor MQ display; Bit13: Torque control setting value; Bit14: Load speed; Bit15: PID feedback value | 0000 | ☆ |
| P7-45 | LED stop display parameter 2 | Setting freq (Y/A); AI1; AI2; AI3; Setting freq (Y); Freq (X); Bus voltage; Length value; Count value; Output freq; etc. | 0FFF | ☆ |

---

### P8 Group: Auxiliary Functions

| Code | Name | Setting Range | Default | Attr |
|------|------|--------------|---------|------|
| P8-00 | Jog operating frequency | 0.00Hz – max frequency | 6.00Hz | ☆ |
| P8-01 | Jog acceleration time | 0.0s–6500.0s | Model | ☆ |
| P8-02 | Jog deceleration time | 0.0s–6500.0s | Model | ☆ |
| P8-03 | Acceleration time 2 | 0.0s–6500.0s | Model | ☆ |
| P8-04 | Deceleration time 2 | 0.0s–6500.0s | Model | ☆ |
| P8-05 | Acceleration time 3 | 0.0s–6500.0s | Model | ☆ |
| P8-06 | Deceleration time 3 | 0.0s–6500.0s | Model | ☆ |
| P8-07 | Acceleration time 4 | 0.0s–6500.0s | Model | ☆ |
| P8-08 | Deceleration time 4 | 0.0s–6500.0s | Model | ☆ |
| P8-09 | Hopping frequency 1 | 0.00Hz – max frequency | 0.00Hz | ☆ |
| P8-10 | Hopping frequency 2 | 0.00Hz – max frequency | 0.00Hz | ☆ |
| P8-11 | Hopping frequency width | 0.00Hz – max frequency | 0.00Hz | ☆ |
| P8-14 | Below lower-limit frequency action | 0: Run at lower limit freq; 1: Stop; 2: Run at zero speed | 0 | ☆ |
| P8-17 | Accumulation running time arrival | 0–65000h | — | ☆ |
| P8-18 | Startup protection | 0: Disable; 1: Allow | 1 | ☆ |
| P8-19 | Stop display parameter 1 | 00–96 (corresponding to U0 group parameter numbers) | 04 | ☆ |
| P8-20 | Stop display parameter 2 | 00–96 | 02 | ☆ |
| P8-22 | Cumulative power-on time | — | — | • |
| P8-23 | Load speed display coefficient | 0.001–65.535 | 1.000 | ☆ |
| P8-24 | Load speed display decimal places | 0: 0 places; 1: 1 place; 2: 2 places; 3: 3 places | 1 | ☆ |
| P8-26 | Inverter module temperature | — | — | • |
| P8-28 | Cumulative power consumption | 0–65535kWh | — | • |

---

### P9 Group: Fault and Protection

> Fault type codes embedded in P9-14/P9-15/P9-16: 1=Accel overcurrent; 2=Decel overcurrent; 3=Constant speed overcurrent; 4=Accel overvoltage; 5=Decel overvoltage; 6=Constant speed overvoltage; 7=Undervoltage; 8=Buffer resistor overload; 9=Inverter overload; 10=Motor overload; 11=Input phase loss; 12=Input phase loss; 13=Output phase loss; 14=Module OT; 15=External fault; 16=Communication abnormality; 17=Contactor abnormality; 18=Current detection abnormality; 19=Motor tuning abnormality; 20=Reserved; 21=Parameter reading/writing abnormality; 22=Inverter hardware abnormality; 23=Motor ground short circuit; 24=Reserved; 25=Reserved; 27=User-defined fault 1; 28=User-defined fault 2; 29=Power-on time reaches; 30=Load loss; 31=Run-time PID feedback loss; 40=Fast current limit timeout; 41=Switch motor during operation; 42=Speed deviation; 43=Motor overspeed; 45=Reserved; 51=Reserved; 70=Water shortage pressure fault; 71=Excessive water pressure fault

| Code | Name | Setting Range | Default | Attr |
|------|------|--------------|---------|------|
| P9-00 | Motor overload protection | 0: Disable; 1: Allow | 1 | ☆ |
| P9-01 | Motor overload protection gain | 0.20–10.00 | 1.00 | ☆ |
| P9-02 | Motor overload warning coefficient | 50%–100% | 80% | ☆ |
| P9-03 | Overvoltage stall gain | 0–100 | 0 | ☆ |
| P9-04 | Overvoltage stall protection voltage | 200.0–2000.0V | 220V:380V / 380V:760V | ☆ |
| P9-05 | Overvoltage stall current limit gain | 0–100 | 20 | ☆ |
| P9-06 | Over-current stall protection current | 100%–200% | 150% | ☆ |
| P9-07 | Power on to ground short-circuit protection | 0: Invalid; 1: Valid | 1 | ☆ |
| P9-08 | Dynamic braking action threshold voltage | 200.0–2000.0V | 220V:360V / 380V:700V | ☆ |
| P9-09 | Automatic fault reset times | 0–20 | 0 | ☆ |
| P9-10 | Action selection of fault DO during auto reset | 0: No action; 1: Action | 0 | ☆ |
| P9-11 | Automatic fault reset interval | 0.1–100.0s | 1.0s | ☆ |
| P9-12 | Input phase loss protection | 0: Disable; 1: Allow | 0 | ☆ |
| P9-13 | Output phase loss protection option | 0: Disable; 1: Allow | 1 | ☆ |
| P9-14 | Type of first failure | (read-only, see code list above) | — | • |
| P9-15 | Type of second failure | (read-only) | — | • |
| P9-16 | Type of third (latest) failure | (read-only) | — | • |
| P9-17 | Frequency of third (latest) failure | — | — | • |
| P9-18 | Current at third failure | — | — | • |
| P9-19 | Bus voltage at third failure | — | — | • |
| P9-20 | Input terminal status at third failure | — | — | • |
| P9-21 | Output terminal status at third failure | — | — | • |
| P9-22 | Inverter status at third failure | — | — | • |
| P9-23 | Power-on time at third failure | — | — | • |
| P9-24 | Running time at third failure | — | — | • |
| P9-27 | Frequency at second failure | — | — | • |
| P9-28 | Current at second failure | — | — | • |
| P9-29 | Bus voltage at second failure | — | — | • |
| P9-30 | Input terminal status at second failure | — | — | • |
| P9-31 | Output terminal status at second failure | — | — | • |
| P9-32 | Inverter status at second failure | — | — | • |
| P9-33 | Power-on time at second failure | — | — | • |
| P9-34 | Running time at second failure | — | — | • |
| P9-37 | Frequency at first failure | — | — | • |
| P9-38 | Current at first failure | — | — | • |
| P9-39 | Bus voltage at first failure | — | — | • |
| P9-40 | Input terminal status at first failure | — | — | • |
| P9-41 | Output terminal status at first failure | — | — | • |
| P9-42 | Inverter status at first failure | — | — | • |
| P9-43 | Power-on time at first failure | — | — | • |
| P9-44 | Running time at first failure | — | — | • |
| P9-47 | Fault protection action selection 1 | Ones: Motor overload (11) 0=free stop, 1=stop by mode, 2=continue; Tens: Input phase loss (12); Hundreds: Output phase loss (13); Thousands: External fault (15); Ten-thousands: Communication (16) | 00000 | ☆ |
| P9-50 | Motor overheat protection | 0%: no motor overheat; others: PT100 thermistor | — | ☆ |
| P9-54 | Continue to run frequency selection in case of failure | 0: Current operating freq; 1: Set freq; 2: Upper limit freq; 3: Lower limit freq; 4: Abnormal standby freq | 0 | ☆ |
| P9-55 | Abnormal backup frequency | 60.0%–100.0% (100.0% corresponds to maximum frequency P0-10) | 100.0% | ☆ |
| P9-59 | Instantaneous power failure action selection | 0: Invalid; 1: Decelerate; 2: Decelerate to stop | 0 | ☆ |
| P9-60 | Momentary stop action pause judgment voltage | P9-62–100.0% | 100.0% | ☆ |
| P9-61 | Instantaneous power failure voltage recovery judgment time | 0.0s–100.0s | 0.50s | ☆ |
| P9-62 | Instantaneous power failure action judgment voltage | 60.0%–100.0% | 80.0% | ☆ |
| P9-63 | Offload protection options | 0: Invalid; 1: Valid | 0 | ☆ |
| P9-64 | Offload detection level | 0.0%–100.0% | 10.0% | ☆ |
| P9-65 | Offload detection time | 0.0s–60.0s | 1.0s | ☆ |

---

### PA Group: PID Function

| Code | Name | Setting Range | Default | Attr |
|------|------|--------------|---------|------|
| PA-00 | PID given source | 0: PA-01; 1: AI1; 2: AI2; 3: AI3 keyboard pot; 4: HDI pulse (X5); 5: Communication; 6: Multi-segment command; 7: Water supply group b0-01 | 0 | ☆ |
| PA-01 | PID given value | 0.0%–100.0% | 50.0% | ☆ |
| PA-02 | PID feedback source | 0: AI1; 1: AI2; 2: AI3 keyboard pot; 3: AI1–AI2; 4: HDI pulse (X5); 5: Communication; 6: AI1+AI2; 7: MAX(\|AI1\|,\|AI2\|); 8: MIN(\|AI1\|,\|AI2\|) | 0 | ☆ |
| PA-03 | PID action direction | 0: Positive effect; 1: Negative effect | 0 | ☆ |
| PA-04 | PID feedback range | 0–65535 | 1000 | ☆ |
| PA-05 | Proportional gain Kp1 | 0.0–100.0 | 20.0 | ☆ |
| PA-06 | Integration time Ti1 | 0.01s–10.00s | 2.00s | ☆ |
| PA-07 | Differential time Td1 | 0.000s–10.000s | 0.000s | ☆ |
| PA-08 | PID reverse cutoff frequency | 0.00Hz – max frequency | 2.00Hz | ☆ |
| PA-09 | PID deviation limit | 0.0%–100.0% | 0.0% | ☆ |
| PA-10 | PID differential limit | 0.00%–100.00% | 0.10% | ☆ |
| PA-11 | PID given change time | 0.00s–650.00s | 0.00s | ☆ |
| PA-12 | PID feedback filter time | 0.00s–60.00s | 0.00s | ☆ |
| PA-13 | PID output filter time | 0.00s–60.00s | 0.00s | ☆ |
| PA-15 | Proportional gain Kp2 | 0.0–100.0 | 20.0 | ☆ |
| PA-16 | Integration time Ti2 | 0.01s–10.00s | 2.00s | ☆ |
| PA-17 | Differential time Td2 | 0.000s–10.000s | 0.000s | ☆ |
| PA-18 | PID parameters switching condition | 0: No switching; 1: Switch via DI terminal; 2: Automatically switch based on deviation | 0 | ☆ |
| PA-19 | PID parameters switching deviation 1 | 0.0%–PA-20 | 20.0% | ☆ |
| PA-20 | PID parameters switching deviation 2 | PA-19–100.0% | 80.0% | ☆ |
| PA-21 | PID initial value | 0.0%–100.0% | 0.0% | ☆ |
| PA-22 | PID initial value holding time | 0.00s–650.00s | 0.00s | ☆ |
| PA-23 | Max positive output deviation | 0.00%–100.00% | 1.00% | ☆ |
| PA-24 | Max negative output deviation | 0.00%–100.00% | 1.00% | ☆ |
| PA-25 | PID integral properties | Ones: Integral separation 0=invalid, 1=effective; Tens: Stop integration at output limit 0=continue, 1=stop | 0 | ☆ |
| PA-26 | PID feedback loss detection value | 0.0%: No detection; 0.1%–100.0% | 0.0% | ☆ |
| PA-27 | PID feedback loss detection time | 0.0s–20.0s | 0.0s | ☆ |
| PA-28 | PID shutdown calculation | 0: No operation at shutdown; 1: Operation at shutdown | 1 | ☆ |

---

### Pb Group: Swing Frequency / Fixed Length / Count

| Code | Name | Setting Range | Default | Attr |
|------|------|--------------|---------|------|
| Pb-00 | Swing frequency setting method | 0: Relative to center frequency; 1: Relative to max frequency | 0 | ☆ |
| Pb-01 | Swing frequency amplitude | 0.0%–100.0% | 0.0% | ☆ |
| Pb-02 | Sudden jump frequency amplitude | 0.0%–50.0% | 0.0% | ☆ |
| Pb-03 | Swing frequency cycle | 0.1s–3000.0s | 10.0s | ☆ |
| Pb-04 | Triangular wave rise time | 0.1%–100.0% | 50.0% | ☆ |
| Pb-05 | Set length | 0–65535m | 1000m | ☆ |
| Pb-06 | Actual length | 0–65535m | 0m | ☆ |
| Pb-07 | Number of pulses per meter | 1–65535 | 100.0 | ☆ |
| Pb-08 | Set count value | 1–65535 | 1000 | ☆ |
| Pb-09 | Specified count value | 1–65535 | 1000 | ☆ |

---

### PC Group: Multi-segment Instructions and Simple PLC

| Code | Name | Setting Range | Default | Attr |
|------|------|--------------|---------|------|
| PC-00–PC-15 | Multi-segment instruction 0–15 | -100.0%–100.0% | 0.0% | ☆ |
| PC-16 | Simple PLC operation mode | 0: Stop after single cycle; 1: Keep final value at end of single cycle; 2: Cycle; 3: Keep final value at end of a single cycle (power-down memory) | 0 | ☆ |
| PC-17 | Simple PLC power-down memory | 0: Power down without memory; 1: Power down with memory | 0 | ☆ |
| PC-40–PC-47 | Segment P1–P8 timing (0.0s–6553.5s) | — | 0.0s(0) | ☆ |
| PC-41 | Simple PLC step timer selection | — | — | ☆ |

---

### Pd Group: Communication Parameters

| Code | Name | Setting Range | Default | Attr |
|------|------|--------------|---------|------|
| Pd-00 | Communication baud rate | 0: 600BPS; 1: 1200BPS; 2: 2400BPS; 3: 4800BPS; 4: 9600BPS; 5: 19200BPS; 6: 38400BPS; 7: 57600BPS | 4 | ☆ |
| Pd-01 | Data format | 0: No parity (8-N-2); 1: Even parity (8-E-1); 2: Odd parity (8-O-1); 3: No parity (8-N-1) | 3 | ☆ |
| Pd-02 | Local address | 1–247 | 1 | ☆ |
| Pd-03 | Communication response delay | 0–20ms | 2 | ☆ |
| Pd-04 | Communication timeout | 0.0 (invalid); 0.1s–60.0s | 0.0 | ☆ |
| Pd-05 | Data transfer format | 1: Standard MODBUS protocol | 1 | ☆ |
| Pd-06 | Communication reading current resolution | 0: 0.01A; 1: 0.1A | 0 | ☆ |
| Pd-07 | Reserve | — | — | — |

### PP Group: Parameter Management

| Code | Name | Setting Range | Default | Attr |
|------|------|--------------|---------|------|
| PP-00 | User password | 0–65535 | 0 | ☆ |
| PP-01 | Parameter initialization | 0: No operation; 1: Restore factory params (excl. motor); 2: Clear incl. motor; 3: Restore incl. motor; 4: Backup params; 10: Restore backup | 0 | ★ |
| PP-02 | Function parameter group display selection | Ones: U group; Tens: A group; Hundreds: b group (0=hide, 1=show) | 111 | ★ |
| PP-04 | Function code modification attribute | 0: Can be modified; 1: Cannot be modified | 0 | ★ |

---

### A0 Group: Torque Control Parameters

| Code | Name | Notes |
|------|------|-------|
| A0-00 | Speed/torque control | 0: Speed control; 1: Torque control (select via terminal or A0-00) |
| A0-01 | Torque setting source | 0: A0-03 digital setting; 1: AI1; 2: AI2; 3: AI3 keyboard pot; 4: HDI pulse; 5: Communication; 6: MIN(AI1,AI2); 7: MAX(AI1,AI2) |
| A0-02 | Reserved | — |
| A0-03 | Torque digital setting | -200.0%–200.0%; default 150.0% |
| A0-04 | Reserved | — |
| A0-05 | Maximum torque frequency | 0.00Hz–max frequency; default 30.00Hz |

---

### A1 Group: Control Optimization Parameters

| Code | Name | Setting Range | Default | Attr |
|------|------|--------------|---------|------|
| A1-00 | Zero compensation upper limit | 0–15kHz | 13.0kHz | ☆ |
| A1-01 | PWM modulation method | 0: Asynchronous modulation; 1: Synchronous modulation; 2: Compensation mode 1; 3: Compensation mode 2; 4: No compensation | — | ☆ |
| A1-02 | PWM modulation mode | — | — | ☆ |
| A1-03 | Random PWM depth | 0–10 | 0 | ☆ |
| A1-04 | Dead zone compensation enable | 0: Disabled; 1: Enable | 1 | ☆ |
| A1-05 | SVC optimization mode | 0: No optimization; 1: Optimization mode 1; 2: Optimization mode 2 | 1 | ☆ |
| A1-06 | Current detection compensation | 0–100 | 5 | ☆ |
| A1-07 | Fast current limit enable | 0: Disabled; 1: Enable | 1 | ☆ |
| A1-08 | Undershoot point setting | 1000–3000V | — | ☆ |
| A1-09 | Dead time adjustment | 200/2500V | — | ☆ |
| A1-10 | Undershoot frequency adjustment | 100–200% | 150% | ☆ |
| A1-17 | Y terminal output valid status | — | 0d/0h | ☆ |
| A1-18–A1-22 | Wake-up / sleep freq, fan control | — | — | ☆ |

---

### bH Group: Water Supply Application (Pressure Supply Macros)

See P0-29 macro selection for water supply application macros (1-tow-3, 1-tow-5, fire inspection, etc.).

Key parameters for constant pressure water supply:
- **Pb-15** (= PA-00): PID given source
- **PA-05**: Proportional gain Kp
- **PA-06**: Integration time Ti
- **PA-07**: Differential time Td
- Use multi-speed terminals (X terminals) to select pump combinations

---

## Chapter 5: Fault Diagnosis and Countermeasures

### 5.1 Fault Alarm and Countermeasures

> The frequency converter has fault/warning protection. When a fault occurs, the TUNE/TC indicator flashes quickly and a fault code is shown. Fault information is recorded in P9-14, P9-15, P9-16 for up to 3 faults.

| Fault Code | Fault Name | Possible Causes | Countermeasures |
|-----------|-----------|----------------|-----------------|
| Er01 | Inverter unit protect (overcurrent) | Short circuit in output; module overheated; wiring loose; drive board fault; inverter module damaged | Eliminate peripheral faults; check wiring; check air duct; clean filter; seek technical support |
| Er02 | Accelerating overcurrent | Short circuit in output; too short accel time; grid voltage too low; motor params incorrect; drive board abnormal | Eliminate peripheral faults; increase acceleration time; check voltage; perform motor parameter identification |
| Er03 | Decelerating overcurrent | Short circuit; too short decel time; decel load too large | Increase decel time; add braking resistor; seek support |
| Er04 | Constant speed overcurrent | Short circuit; too large sudden load change; grid voltage too low; motor params abnormal | Eliminate faults; check voltage; seek support |
| Er05 | Accelerating overvoltage | Grid voltage too high; energy feedback during accel | Adjust input voltage; seek support |
| Er06 | Decelerating overvoltage | Grid voltage too high; too short decel time; braking unit/resistor abnormal | Adjust voltage; increase decel time; install braking device |
| Er07 | Constant speed overvoltage | Grid voltage too high; sudden large load change | Adjust grid voltage; cancel external force driving motor |
| Er08 | Instantaneous power overvoltage | Grid voltage too high; abnormal voltage at startup | Adjust voltage; seek support |
| Er09 | Undervoltage | Grid voltage too low; abnormal bus voltage detection | Check grid voltage; seek support |
| Er10 | Inverter overload | Accel too short; grid voltage too low; motor load too large | Increase accel time; adjust voltage; reduce load; choose larger inverter |
| Er11 | Motor overload | Motor protection gain P9-01 not appropriate; motor stalled or overloaded | Adjust P9-01; reduce load; seek support |
| Er12 | Input phase loss | Input phase loss; drive board abnormal | Eliminate input phase loss |
| Er13 | Output phase loss | Output wiring disconnected; motor internal disconnection; drive board abnormal | Check output wiring; seek support |
| Er14 | Module OT | Air duct blocked; fan damaged; ambient temperature too high; module damaged | Clean air duct; check/replace fan; reduce ambient temperature |
| Er15 | External device fault | External fault input (X terminal DI function 11=normally open or 33=normally closed) triggered | Check external device |
| Er16 | Communication abnormality | RS-485 communication lost or timeout (see Pd-04 timeout setting) | Check wiring; check Pd-04 timeout; check master device |
| Er17 | Contactor failure | Drive board and power board contactor abnormal | Replace contactor; seek support |
| Er18 | Current detection fault | Hall device abnormal; drive board and power board abnormal | Replace Hall device/board; seek support |
| Er19 | Motor tuning fault | Motor parameters set incorrectly; motor parameter identification failed | Check motor params; seek support |
| Er21 | Parameter read/write fault | EEPROM chip damaged or parameter read/write error | Seek support |
| Er22 | Inverter hardware fault | — | Power off/on again; seek support |
| Er23 | Motor ground short circuit | Motor or cable short to ground | Check motor; eliminate short circuit |
| Er26 | Running time reaches | Running time has reached the set value | Use parameter initialization to clear record |
| Er30 | Load loss | Motor lost load (belt break, etc.) | Check mechanical load coupling |
| Er31 | Run-time PID feedback loss | PID feedback signal lost during operation | Check PID feedback wiring; check PA-26/PA-27 |
| Er27 | User-defined fault 1 | Multi-function terminal DI function 44 triggered | Check external trigger condition |
| Er28 | User-defined fault 2 | Multi-function terminal DI function 45 triggered | Check external trigger condition |
| Er29 | Power-on time reaches | Accumulated power-on time has reached set value | Use initialization to clear |
| Er40 | Fast current limit timeout | — | Reduce load; choose higher-power inverter |
| Er41 | Motor switch during operation fault | Motor was switched while running | Stop before switching motor |
| Er42 | Speed deviation too large | Speed tracking deviation exceeds set value | Check motor coupling; adjust parameters |
| Er43 | Motor overspeed | Motor speed exceeds upper limit | Check mechanical conditions; verify max frequency settings |
| Er46 | PID feedback and current fault | PID feedback is smaller than PA-26 value | Check PID feedback input; check PA-26 |
| Er50 | Accumulation fault | Accumulated power-on times exceed set value | Use parameter initialization to clear |
| Er60 | Offload (underload) protection | Load is below the offload detection level (P9-64) for longer than P9-65 | Check mechanical coupling; check P9-64/P9-65 settings |
| Er65 | Motor overheat | Temperature sensor wiring wrong; motor temperature too high | Check sensor wiring; reduce frequency; take heat-dissipating measures |
| Er67 | Motor overheat | Temperature too high | Check and reduce load; improve cooling |
| Er70 | Water shortage pressure fault | Water supply pressure lower than protection value | Check water supply; check sensor |
| Er71 | Excessive water pressure fault | Water pressure exceeds limit | Check water supply; check sensor |

---

### 5.2 Common Faults and Solutions

| Symptom | Possible Causes | Solutions |
|---------|----------------|-----------|
| No display after power-on | Input phase loss; rectifier bridge damaged; buffer circuit fault; power board abnormal; display board fault | Check input power; check peripheral faults; seek technical support |
| Display normal but no output after RUN | Control mode wrong; command source wrong; freq command not given; motor/drive fault | Check P0-02 command source; check P0-03 freq source; verify motor wiring |
| Motor rotation direction wrong | Phase sequence wrong; direction control incorrect | Swap any two output phases (U/V/W); or set P0-09 reverse direction |
| Motor speed not reaching set value | Freq upper limit too low; insufficient torque; overload | Check P0-12 upper limit; check load; check V/F parameters |
| Motor vibrates or unstable speed | Motor parameter identification needed; V/F curve wrong | Perform motor auto-tuning (P1-37); adjust V/F curve |
| Overcurrent on start | Accel time too short; motor cable short | Increase P0-17 accel time; check wiring |
| Overvoltage on deceleration | Decel time too short; no braking resistor | Increase P0-18 decel time; install braking resistor on P/PB terminals |

---

*Document converted from: "handbook ufc.pdf" — YL42 High Performance Universal Frequency Converter Product Manual*
