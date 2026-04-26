import serial
import struct
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.animation as animation
from collections import deque
import sys

COM_PORT = 'COM8'
BAUD_RATE = 115200
DISPLAY_WINDOW = 1000

try:
    ser = serial.Serial(COM_PORT, BAUD_RATE)
except Exception:
    sys.exit()

y_data = deque([2048]*DISPLAY_WINDOW, maxlen=DISPLAY_WINDOW)
y_pa8 = deque([0]*DISPLAY_WINDOW, maxlen=DISPLAY_WINDOW)
y_pa9 = deque([0]*DISPLAY_WINDOW, maxlen=DISPLAY_WINDOW)

fig = plt.figure(figsize=(12, 6))
fig.canvas.manager.set_window_title("ECG & Leads Monitor")

gs = gridspec.GridSpec(2, 3, figure=fig)

ax_pa0 = fig.add_subplot(gs[:, 0:2])
line_pa0, = ax_pa0.plot(y_data, color='red')
ax_pa0.set_ylim(0, 4096)
ax_pa0.set_ylabel("ADC Value")
ax_pa0.set_title("PA0 (ECG Signal)", fontweight='bold')
ax_pa0.grid(True, linestyle='--', alpha=0.6)

ax_pa8 = fig.add_subplot(gs[0, 2])
line_pa8, = ax_pa8.plot(y_pa8, color='blue')
ax_pa8.set_ylim(-0.5, 1.5)
ax_pa8.set_yticks([0, 1])
ax_pa8.set_title("PA8 (LOD+)", fontweight='bold')
ax_pa8.grid(True, linestyle='--', alpha=0.6)

ax_pa9 = fig.add_subplot(gs[1, 2])
line_pa9, = ax_pa9.plot(y_pa9, color='green')
ax_pa9.set_ylim(-0.5, 1.5)
ax_pa9.set_yticks([0, 1])
ax_pa9.set_title("PA9 (LOD-)", fontweight='bold')
ax_pa9.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()

def read_ecg_packet():
    while True:
        if ser.read(1) == b'\xF1':
            if ser.read(1) == b'\xF1':
                header_rest = ser.read(4) 
                num_samples = header_rest[0] | (header_rest[1] << 8)
                pa8_state = header_rest[2]
                pa9_state = header_rest[3]
                
                payload = ser.read(num_samples * 2)
                if len(payload) == num_samples * 2:
                    data = struct.unpack(f'<{num_samples}H', payload)
                    return data, pa8_state, pa9_state

def update_plot(frame):
    new_data, pa8_state, pa9_state = read_ecg_packet()
    
    y_data.extend(new_data)
    y_pa8.extend([pa8_state] * len(new_data))
    y_pa9.extend([pa9_state] * len(new_data))
    
    line_pa0.set_ydata(y_data)
    line_pa8.set_ydata(y_pa8)
    line_pa9.set_ydata(y_pa9)

    return line_pa0, line_pa8, line_pa9

ani = animation.FuncAnimation(fig, update_plot, interval=10, blit=True, cache_frame_data=False)

try:
    plt.show()
except KeyboardInterrupt:
    pass
finally:
    ser.close()