import pandas as pd
import numpy as np

file_path = "thong_so_EMA.xlsx"  

xl = pd.ExcelFile(file_path)

print(f"{'Sheet':<15} {'Alpha':>8} {'Delta_t (ms)':>14} {'T_stella (ms)':>15}")
print("-" * 55)

results = []

for sheet in xl.sheet_names:
    df = pd.read_excel(file_path, sheet_name=sheet)

    # Lấy alpha từ tên sheet (vd: Alpha_0.3 -> 0.3)
    alpha = float(sheet.split("_")[1])

    # Tính delta_t từ cột Time_ms
    delta_t = df["Time_ms"].diff().dropna().median()

    # Tính T_stella
    T_stella = delta_t / alpha

    print(f"{sheet:<15} {alpha:>8.1f} {delta_t:>14.2f} {T_stella:>15.4f}")
    results.append({"Sheet": sheet, "Alpha": alpha, "Delta_t_ms": delta_t, "T_stella_ms": T_stella})

result_df = pd.DataFrame(results)
result_df.to_excel("T_stella_results.xlsx", index=False)
print("\nDa luu ket qua vao file: T_stella_results.xlsx")

df = pd.read_excel(file_path, sheet_name="Alpha_0.3")

time = df["Time_ms"].values
raw = df["Raw_Altitude"].values

# 1. Xác định giá trị cuối cùng (trung bình 10 mẫu cuối)
final_value = np.mean(raw[-10:])
print(f"Giá trị cuối cùng: {final_value:.3f}")

# 2. Băng thông ±2%
upper_band = final_value * 1.02
lower_band = final_value * 0.98
print(f"Băng trên: {upper_band:.3f}, Băng dưới: {lower_band:.3f}")

# 3. Tìm T_settle: thời điểm cuối cùng tín hiệu ra ngoài băng
t_settle = 0
inside_band = True

for i in range(len(raw)):
    if raw[i] < lower_band or raw[i] > upper_band:
        inside_band = False
        t_settle = time[i]  # lấy thời điểm cuối cùng nằm ngoài
    else:
        if not inside_band:
            # Lần đầu vào băng
            t_settle = time[i]
            inside_band = True

print(f"T_settle = {t_settle} ms")