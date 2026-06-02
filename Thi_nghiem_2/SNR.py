import pandas as pd
import numpy as np

file = "thong_so_EMA.xlsx"
sheets = ["Alpha_0.1", "Alpha_0.3", "Alpha_0.7"]

configs = sheets + ["Raw"]

results = []

for sheet in configs:
    df = pd.read_excel(file, sheet_name=sheets[0]) 
    
    if sheet == "Raw": #Dữ liệu Thô
        data = df["Raw_Altitude"].tail(100) 
        label = "Thô (Raw)"
    else:
        #Đã có bộ lọc EMA
        df = pd.read_excel(file, sheet_name=sheet)
        data = df["EMA_Altitude"].tail(100) 
        label = sheet

    amplitude = data.max() - data.min()
    snr = np.mean(data) / np.std(data)

    results.append([label, amplitude, snr])

results_df = pd.DataFrame(results, columns=["Hệ số", "Biên độ (m)", "SNR"])
print(results_df)