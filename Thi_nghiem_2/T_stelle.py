import pandas as pd
import numpy as np

def calculate_settle_time(
    file_path,
    sheet_name,
    column_name,
    abs_tolerance=0.1,   # SỬ DỤNG SAI SỐ TUYỆT ĐỐI (VD: 0.1 mét = 10 cm)
    stable_samples=20,
    verbose=True
):
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    df.columns = df.columns.str.strip()

    # Ép cột thời gian về số
    df['Time_ms'] = pd.to_numeric(df['Time_ms'], errors='coerce')
    df[column_name] = pd.to_numeric(df[column_name], errors='coerce')

    # Xóa NaN
    df = df.dropna(subset=['Time_ms', column_name])

    t = df['Time_ms'].to_numpy()
    y = df[column_name].to_numpy()

    # Giá trị đầu và cuối
    y_init = np.mean(y[:min(50, len(y))])
    y_final = np.mean(y[-min(50, len(y)):])

    delta = abs(y_final - y_init)
    
    # THAY ĐỔI Ở ĐÂY: Dùng band cố định thay vì dựa vào delta
    band = abs_tolerance 

    lower = y_final - band
    upper = y_final + band

    if verbose:
        print(f"\n--- {sheet_name} / {column_name} ---")
        print(f"  y_init (avg first 50): {y_init:.4f}")
        print(f"  y_final (avg last 50): {y_final:.4f}")
        print(f"  delta = {delta:.4f}")
        print(f"  band (absolute ±) = {band:.4f}")
        print(f"  stable band: [{lower:.4f}, {upper:.4f}]")

    inside = (y >= lower) & (y <= upper)

    count = 0
    for i in range(len(inside)):
        if inside[i]:
            count += 1
        else:
            count = 0

        if count >= stable_samples:
            settle_idx = i - stable_samples + 1
            settle_time = t[settle_idx]
            if verbose:
                print(f"  -> Settle time found at t = {settle_time:.2f} ms (index {settle_idx})")
            return settle_time

    if verbose:
        print(f"  WARNING: Never reached {stable_samples} stable consecutive samples within band.")
        print(f"  Returning last time = {t[-1]:.2f} ms")
    return t[-1]

file_path = "thong_so_EMA.xlsx"

# Alpha 0.1
tsettle_01 = calculate_settle_time(file_path, "Alpha_0.1", "EMA_Altitude")
print(f"Tsettle Alpha 0.1: {tsettle_01:.2f} ms")

# Alpha 0.3
tsettle_03 = calculate_settle_time(file_path, "Alpha_0.3", "EMA_Altitude")
print(f"Tsettle Alpha 0.3: {tsettle_03:.2f} ms")

# Alpha 0.7
tsettle_07 = calculate_settle_time(file_path, "Alpha_0.7", "EMA_Altitude")
print(f"Tsettle Alpha 0.7: {tsettle_07:.2f} ms")

# Raw (lấy từ Alpha_0.3 sheet)
tsettle_raw = calculate_settle_time(file_path, "Alpha_0.3", "Raw_Altitude")
print(f"Tsettle Raw: {tsettle_raw:.2f} ms")