import pandas as pd
import numpy as np

file   = "thong_so_EMA.xlsx"
sheets = ["Alpha_0.1", "Alpha_0.3", "Alpha_0.7"]

results = []

for sheet in sheets:
    df   = pd.read_excel(file, sheet_name=sheet)
    data = df["EMA_Altitude"].tail(100)

    amplitude = data.max() - data.min()
    snr       = np.mean(data) / np.std(data)
    results.append([sheet, amplitude, round(snr, 4)])

for sheet in sheets:
    df   = pd.read_excel(file, sheet_name=sheet)
    data = df["Raw_Altitude"].tail(100)

    amplitude = data.max() - data.min()
    snr       = np.mean(data) / np.std(data)
    results.append([f"Raw ({sheet})", round(amplitude, 4), round(snr, 4)])

results_df = pd.DataFrame(results, columns=["Hệ số", "Biên độ (m)", "SNR"])
print(results_df)

# Lưu ra Excel
results_df.to_excel("SNR_results.xlsx", index=False)
print("\nDa luu ket qua vao: SNR_results.xlsx")

import pandas as pd
import numpy as np

FILE_PATH   = "thong_so_EMA.xlsx"   # Đặt file cùng thư mục script
SHEET_NAME  = 0                      
COL_TIME    = "Time_ms"             
COL_RAW     = "Raw_Altitude"         
ALPHA_LIST  = [0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9]  
OUTPUT_FILE = "EMA_T_stella_compare.xlsx"
# ============================================================

df = pd.read_excel(FILE_PATH, sheet_name=SHEET_NAME)

# Tính delta_t
delta_t = df[COL_TIME].diff().dropna().median()

print(f"Delta_t = {delta_t:.2f} ms")
print(f"\n{'Alpha':>8} | {'T_stella (ms)':>14} | {'EMA Mean':>10} | {'EMA Std':>9} | {'RMSE vs Raw':>12}")
print("-" * 65)

results = []
ema_columns = {}

for alpha in ALPHA_LIST:
    # Tính EMA
    ema = df[COL_RAW].ewm(alpha=alpha, adjust=False).mean()

    # Tính T_stella
    T_stella = delta_t / alpha

    # Thống kê
    ema_mean = ema.mean()
    ema_std  = ema.std()
    rmse     = np.sqrt(((df[COL_RAW] - ema) ** 2).mean())

    print(f"{alpha:>8.2f} | {T_stella:>14.4f} | {ema_mean:>10.4f} | {ema_std:>9.4f} | {rmse:>12.4f}")

    results.append({
        "Alpha":        alpha,
        "T_stella_ms":  round(T_stella, 4),
        "EMA_Mean":     round(ema_mean, 4),
        "EMA_Std":      round(ema_std, 4),
        "RMSE_vs_Raw":  round(rmse, 4),
    })
    ema_columns[f"EMA_alpha_{alpha}"] = ema.values

summary_df = pd.DataFrame(results)

detail_df = df[[COL_TIME, COL_RAW]].copy()
for col_name, values in ema_columns.items():
    detail_df[col_name] = values

with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
    summary_df.to_excel(writer, sheet_name="So_sanh_T_stella", index=False)
    detail_df.to_excel(writer, sheet_name="Chi_tiet_EMA", index=False)

print(f"\nDa luu ket qua vao: {OUTPUT_FILE}")
print(f"  - Sheet 'So_sanh_T_stella': bang so sanh cac alpha")
print(f"  - Sheet 'Chi_tiet_EMA'    : Raw + EMA cua tung alpha theo thoi gian")