import pandas as pd
import numpy as np

def calculate_trise(file_path, sheet_name, column_name):
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    t = df['Time_ms'].to_numpy()
    y = df[column_name].to_numpy()

    # 1. Giá trị đầu và cuối
    y_init = np.mean(y[:20])
    y_final = np.mean(y[-50:])

    # 2. Ngưỡng 10% và 90%
    delta = y_final - y_init
    y_10 = y_init + 0.1 * delta
    y_90 = y_init + 0.9 * delta

    # 3. Tìm thời điểm đạt ngưỡng
    if delta > 0:
        idx_10 = np.argmax(y >= y_10)
        idx_90 = np.argmax(y >= y_90)
    else:
        idx_10 = np.argmax(y <= y_10)
        idx_90 = np.argmax(y <= y_90)

    t_10 = t[idx_10]
    t_90 = t[idx_90]

    # 4. Tính rise time
    trise = t_90 - t_10
    return trise


file_path = "thong_so_EMA.xlsx"

# Alpha 0.1
trise_01 = calculate_trise(
    file_path,
    sheet_name="Alpha_0.1",
    column_name="EMA_Altitude"
)
print(f"T_rise (ms) cho Alpha 0.1: {trise_01:.2f} ms")

# Alpha 0.3
trise_03 = calculate_trise(
    file_path,
    sheet_name="Alpha_0.3",
    column_name="EMA_Altitude"
)
print(f"T_rise (ms) cho Alpha 0.3: {trise_03:.2f} ms")

# Alpha 0.7
trise_07 = calculate_trise(
    file_path,
    sheet_name="Alpha_0.7",
    column_name="EMA_Altitude"
)
print(f"T_rise (ms) cho Alpha 0.7: {trise_07:.2f} ms")

# Dữ liệu thô (ví dụ nằm ở sheet Alpha_0.3)
trise_raw = calculate_trise(
    file_path,
    sheet_name="Alpha_0.3",
    column_name="Raw_Altitude"
)
print(f"T_rise (ms) dữ liệu thô: {trise_raw:.2f} ms")