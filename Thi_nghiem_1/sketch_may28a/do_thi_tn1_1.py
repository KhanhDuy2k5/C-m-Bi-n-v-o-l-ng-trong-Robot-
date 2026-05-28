# Thí nghiệm 1 
# Đồ thị h_means và h_ref cùng với đường thẳng lý tưởng y = x
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

h_ref = np.array([0.0, 3.5, 7.0, 10.5, 14.0])
h_meas = np.array([29.35, 32.94, 36.45, 40.69, 43.70])

df = pd.DataFrame({
    'h_ref': h_ref,
    'h_meas': h_meas
})


# Vẽ đồ thị
plt.figure(figsize=(8, 6))

plt.plot(h_ref, h_meas, 'o-', label='h_meas vs h_ref')

# Đường lý tưởng y = x
x_line = np.linspace(min(h_ref), max(h_ref), 100)
plt.plot(x_line, x_line, '--', label='Đường thẳng lý tưởng (y=x)')

# Gắn nhãn
plt.xlabel('h_ref')
plt.ylabel('h_meas')
plt.title('Đồ thị h_meas vs h_ref cùng với đường thẳng lý tưởng (y=x)')
plt.legend()
plt.grid(True)

plt.show()
