import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# データの読み込み（ファイル名を正確に）
df = pd.read_csv("rent_oita_processed.csv")

# ヒストグラムの描画
plt.hist(df["家賃_per_㎡"].dropna(), bins=30)
plt.title("坪単価の分布")
plt.xlabel("家賃_per_㎡")
plt.ylabel("件数")
plt.show()
