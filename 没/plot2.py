import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.family'] = 'AppleGothic'
# データの読み込み（面積ありモデルの予測値付きCSV）
df = pd.read_csv("rent_oita_with_prediction.csv")

# 欠損除外（必要なら）
df = df.dropna(subset=["log_家賃_per_㎡", "log_家賃_per_㎡_pred"])

# 残差を計算
df["残差"] = df["log_家賃_per_㎡"] - df["log_家賃_per_㎡_pred"]

# 散布図の描画
plt.figure(figsize=(8, 6))
plt.scatter(df["log_家賃_per_㎡_pred"], df["log_家賃_per_㎡"], alpha=0.6)
plt.plot([df["log_家賃_per_㎡"].min(), df["log_家賃_per_㎡"].max()],
         [df["log_家賃_per_㎡"].min(), df["log_家賃_per_㎡"].max()],
         color='red', linestyle='--')
plt.xlabel("予測 log(家賃_per_㎡)")
plt.ylabel("実測 log(家賃_per_㎡)")
plt.title("実測 vs 予測の散布図")
plt.grid(True)
plt.tight_layout()
plt.show()
# 残差の絶対値を使って誤差の大きい上位5件を表示
df["abs_残差"] = df["残差"].abs()
top_outliers = df.sort_values(by="abs_残差", ascending=False).head(5)

# 出力
print("[INFO] 誤差が大きい上位5物件：")
print(top_outliers[
    ["物件名", "所在地", "家賃_num", "面積_num", "築年数_num", "駅名", "徒歩分_num",
     "log_家賃_per_㎡", "log_家賃_per_㎡_pred", "残差"]
])