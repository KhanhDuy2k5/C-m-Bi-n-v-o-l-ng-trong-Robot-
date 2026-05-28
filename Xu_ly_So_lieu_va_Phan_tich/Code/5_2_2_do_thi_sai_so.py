import numpy as np
import matplotlib.pyplot as plt

h_ref = np.array([0.0, 3.5, 7.0, 10.5, 14.0])
h_meas = np.array([29.35, 32.94, 36.45, 40.69, 43.70])

e_h = h_meas - h_ref

print("Sai số e_h:")
print(e_h)

plt.figure(figsize=(8,6))

plt.plot(h_ref, e_h, 'o-', linewidth=2, markersize=8, label=r'$e_h = h_{meas} - h_{ref}$')

plt.axhline(y=0, linestyle='--', linewidth=1.5, label='e_h = 0')

# Gắn nhãn
plt.xlabel(r'$h_{ref}$')
plt.ylabel(r'$e_h$')
plt.title(r'Đồ thị sai số: $e_h$ vs $h_{ref}$')

plt.grid(True)
plt.legend()

# Hiển thị
plt.show()