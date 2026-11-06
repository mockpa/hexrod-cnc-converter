#!/usr/bin/env python3
# yl42_vfd.py — LinuxCNC HAL userspace component for YL42 VFD via RS-485 Modbus
#
# Register map (discovered empirically):
#   0x2000 write: 1=FWD run, 2=REV run, 5=stop (decel)
#   0x1000 write: frequency setpoint in 0.01 Hz units (e.g. 40000 = 400 Hz)
#   0x1000 read:  output frequency in 0.01 Hz units
#   0x1004 read:  output current (approx 0.01 A units)
#   0x3000 read:  status  1=FWD running, 2=REV running, 3=stopped, 4=fault
#
# VFD one-time setup (written at startup, survives power cycle):
#   P0-02 = 2  (command source = RS-485)
#   P0-03 = 9  (frequency source = RS-485)

import sys
import time
import signal
import hal
import minimalmodbus

# ── Configuration ─────────────────────────────────────────────────────────────
SERIAL_PORT  = '/dev/ttyACM0'
SERIAL_BAUD  = 9600
SLAVE_ADDR   = 1
MAX_FREQ_HZ  = 400.0    # VFD max output frequency
MAX_RPM      = 24000.0  # Spindle max RPM
POLL_HZ      = 10       # HAL update rate
AT_SPEED_TOL = 0.05     # 5 % tolerance for at-speed detection

# ── HAL component ─────────────────────────────────────────────────────────────
h = hal.component('yl42_vfd')
h.newpin('speed-rpm',  hal.HAL_FLOAT, hal.HAL_IN)   # commanded speed (RPM)
h.newpin('run-fwd',    hal.HAL_BIT,   hal.HAL_IN)   # forward run request
h.newpin('run-rev',    hal.HAL_BIT,   hal.HAL_IN)   # reverse run request
h.newpin('at-speed',   hal.HAL_BIT,   hal.HAL_OUT)  # at commanded speed
h.newpin('running',    hal.HAL_BIT,   hal.HAL_OUT)  # VFD running
h.newpin('fault',      hal.HAL_BIT,   hal.HAL_OUT)  # VFD fault
h.newpin('freq-cmd',   hal.HAL_FLOAT, hal.HAL_OUT)  # commanded freq (Hz)
h.newpin('freq-fb',    hal.HAL_FLOAT, hal.HAL_OUT)  # actual output freq (Hz)
h.newpin('current',    hal.HAL_FLOAT, hal.HAL_OUT)  # output current (A)
h.ready()

# ── Modbus setup ──────────────────────────────────────────────────────────────
vfd = minimalmodbus.Instrument(SERIAL_PORT, SLAVE_ADDR)
vfd.serial.baudrate = SERIAL_BAUD
vfd.serial.bytesize = 8
vfd.serial.parity   = 'N'
vfd.serial.stopbits = 1
vfd.serial.timeout  = 0.5

def vfd_init():
    vfd.write_register(0x0002, 2, functioncode=6)  # P0-02 = comms command
    vfd.write_register(0x0003, 9, functioncode=6)  # P0-03 = comms frequency
    vfd.write_register(0x2000, 5, functioncode=6)  # ensure stopped

def vfd_stop():
    try:
        vfd.write_register(0x2000, 5, functioncode=6)
    except Exception:
        pass

def rpm_to_reg(rpm):
    hz = abs(rpm) / MAX_RPM * MAX_FREQ_HZ
    hz = min(hz, MAX_FREQ_HZ)
    return int(hz * 100)   # 0.01 Hz units, e.g. 40000 = 400.00 Hz

# ── Graceful shutdown ─────────────────────────────────────────────────────────
def shutdown(sig, frame):
    vfd_stop()
    sys.exit(0)

signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT,  shutdown)

# ── Startup ───────────────────────────────────────────────────────────────────
try:
    vfd_init()
except Exception as e:
    sys.stderr.write(f"yl42_vfd: init failed: {e}\n")
    sys.exit(1)

prev_cmd  = 5    # last command sent (5 = stop)
error_count = 0

# ── Main loop ─────────────────────────────────────────────────────────────────
while True:
    try:
        rpm  = h['speed-rpm']
        fwd  = h['run-fwd']
        rev  = h['run-rev']

        # Determine run command
        if fwd and rpm > 1.0:
            cmd = 1
        elif rev and rpm > 1.0:
            cmd = 2
        else:
            cmd = 5

        freq_reg = rpm_to_reg(rpm)

        # Write frequency setpoint every cycle
        vfd.write_register(0x1000, freq_reg, functioncode=6)

        # Write run command only on change
        if cmd != prev_cmd:
            vfd.write_register(0x2000, cmd, functioncode=6)
            prev_cmd = cmd

        # Read back status and frequency
        status   = vfd.read_register(0x3000, functioncode=3)
        freq_out = vfd.read_register(0x1000, functioncode=3) * 0.01  # Hz
        current  = vfd.read_register(0x1004, functioncode=3) * 0.01  # A (approx)

        running = status in (1, 2)
        fault   = (status == 4)

        # At-speed: running and actual freq within tolerance of commanded
        cmd_hz   = freq_reg * 0.01
        tol_hz   = max(cmd_hz * AT_SPEED_TOL, 1.0)
        at_speed = running and cmd != 5 and (abs(freq_out - cmd_hz) <= tol_hz)

        h['running']   = running
        h['fault']     = fault
        h['freq-cmd']  = cmd_hz
        h['freq-fb']   = freq_out
        h['current']   = current
        h['at-speed']  = at_speed

        error_count = 0

    except Exception as e:
        error_count += 1
        h['running']  = False
        h['at-speed'] = False
        if error_count <= 3:
            sys.stderr.write(f"yl42_vfd: comms error: {e}\n")
        # After 5 consecutive errors try to re-init
        if error_count == 5:
            sys.stderr.write("yl42_vfd: re-initialising...\n")
            try:
                vfd_init()
                prev_cmd = 5
            except Exception:
                pass

    time.sleep(1.0 / POLL_HZ)
