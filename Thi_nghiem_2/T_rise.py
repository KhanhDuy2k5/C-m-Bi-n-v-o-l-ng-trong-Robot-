import pandas as pd
import numpy as np

def calculate_trise(file_path, sheet_name, column_name):
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    t = df["Time_ms"].to_numpy()
    y = df[column_name].to_numpy()

    y_init  = np.mean(y[:20])
    y_final = np.mean(y[-50:])
    delta   = y_final - y_init

    if abs(delta) < 1e-6:
        print(f"  [{sheet_name}/{column_name}] delta ≈ 0 — tín hiệu không có bước nhảy rõ ràng.")
        return None

    # 2. Ngưỡng 10% và 90%
    y_10 = y_init + 0.1 * delta
    y_90 = y_init + 0.9 * delta

    # 3. Tìm chỉ số vượt ngưỡng
    if delta > 0:
        idx_10_arr = np.where(y >= y_10)[0]
        idx_90_arr = np.where(y >= y_90)[0]
    else:
        idx_10_arr = np.where(y <= y_10)[0]
        idx_90_arr = np.where(y <= y_90)[0]


    t_10 = t[idx_10_arr[0]]
    t_90 = t[idx_90_arr[0]]

    # 4. Tính T_rise
    trise = t_90 - t_10
    return trise


file_path = "thong_so_EMA.xlsx"

cases = [
    ("Alpha_0.1", "EMA_Altitude",  "Alpha 0.1"),
    ("Alpha_0.3", "EMA_Altitude",  "Alpha 0.3"),
    ("Alpha_0.7", "EMA_Altitude",  "Alpha 0.7"),
    ("Alpha_0.3", "Raw_Altitude",  "Dữ liệu thô"),
]

results = []
print(f"{'Trường hợp':<20} {'T_rise (ms)':>12}")
print("-" * 35)

for sheet, col, label in cases:
    trise = calculate_trise(file_path, sheet, col)
    if trise is not None:
        print(f"{label:<20} {trise:>12.2f}")
        results.append([label, sheet, col, round(trise, 2)])
    else:
        print(f"{label:<20} {'N/A':>12}")
        results.append([label, sheet, col, None])

# Lưu ra Excel
results_df = pd.DataFrame(results, columns=["Trường hợp", "Sheet", "Cột", "T_rise_ms"])
results_df.to_excel("T_rise_results.xlsx", index=False)
print("\nDa luu ket qua vao: T_rise_results.xlsx")