import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# データの読み込み
df = pd.read_csv("rent_oita_processed.csv")

# 対数変換
df["log_家賃_per_㎡"] = np.log(df["家賃_per_㎡"])

# ヒストグラム表示
plt.hist(df["log_家賃_per_㎡"].dropna(), bins=30)
plt.title("坪単価（対数変換）の分布")
plt.xlabel("log(家賃_per_㎡)")
plt.ylabel("件数")
plt.show()
