# Đồ thị đặc tuyến tính : h_{meas}vsh_{ref}– gồm điểm đo và đường hồi quy

import numpy as np
import matplotlib.pyplot as plt


h_ref = np.array([0.0, 3.5, 7.0, 10.5, 14.0])
h_meas = np.array([29.35, 32.94, 36.45, 40.69, 43.70])

# Hồi quy tuyến tính
a, b = np.polyfit(h_ref, h_meas, 1)

x_fit = np.linspace(min(h_ref), max(h_ref), 100)
y_fit = a * x_fit + b

print(f"Phương trình hồi quy:")
print(f"h_meas = {a} * h_ref + {b}")

# Vẽ đồ thị
plt.figure(figsize=(8,6))

plt.plot(h_ref, h_meas, 'o', markersize=8, label='Điểm đo')

plt.plot(x_fit, y_fit, '-', linewidth=2, label=f'Đường hồi quy: y = {a}x + {b}')

# Gắn nhãn
plt.xlabel(r'$h_{ref}$')
plt.ylabel(r'$h_{meas}$')
plt.title(r'Đồ thị đặc tuyến tính: $h_{meas}$ vs $h_{ref}$')

plt.grid(True)
plt.legend()

plt.show()  