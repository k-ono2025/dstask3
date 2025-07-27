import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from adjustText import adjust_text

matplotlib.rcParams['font.family'] = 'Hiragino Maru Gothic Pro'

# データの読み込み（面積ありモデルの予測値付きCSV）
df = pd.read_csv("rent_oita_with_prediction.csv")

# 欠損除外
df = df.dropna(subset=["log_家賃_per_㎡", "log_家賃_per_㎡_pred"])

# 残差を計算
df["残差"] = df["log_家賃_per_㎡"] - df["log_家賃_per_㎡_pred"]

# 残差の正負に応じて上位5件ずつ抽出
top_pos = df[df["残差"] > 0].sort_values(by="残差", ascending=False).head(5)
top_neg = df[df["残差"] < 0].sort_values(by="残差", ascending=True).head(5)

# 散布図の描画
plt.figure(figsize=(10, 8))
plt.scatter(df["log_家賃_per_㎡_pred"], df["log_家賃_per_㎡"], alpha=0.6, label="データ点")
plt.plot([df["log_家賃_per_㎡"].min(), df["log_家賃_per_㎡"].max()],
         [df["log_家賃_per_㎡"].min(), df["log_家賃_per_㎡"].max()],
         color='red', linestyle='--', label="y=x")

# ラベル付きで上位誤差を表示
texts = []
for _, row in pd.concat([top_pos, top_neg]).iterrows():
    plt.scatter(row["log_家賃_per_㎡_pred"], row["log_家賃_per_㎡"], color='red')
    texts.append(plt.text(row["log_家賃_per_㎡_pred"], row["log_家賃_per_㎡"], row["物件名"], fontsize=9, color='red'))

adjust_text(texts, arrowprops=dict(arrowstyle='-', color='gray'))

plt.xlabel("予測 log(家賃_per_㎡)")
plt.ylabel("実測 log(家賃_per_㎡)")
plt.title("実測 vs 予測の散布図（プラス誤差上位5件、マイナス誤差上位5件）")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 出力：ターミナル表示
print("[INFO] プラス誤差上位5件：")
print(top_pos[
    ["物件名", "所在地", "家賃_num", "面積_num", "築年数_num", "駅名", "徒歩分_num",
     "log_家賃_per_㎡", "log_家賃_per_㎡_pred", "残差"]
])

print("\n[INFO] マイナス誤差上位5件：")
print(top_neg[
    ["物件名", "所在地", "家賃_num", "面積_num", "築年数_num", "駅名", "徒歩分_num",
     "log_家賃_per_㎡", "log_家賃_per_㎡_pred", "残差"]
])

# 出力：テキストファイル
with open("top_pos_neg_outliers.txt", "w", encoding="utf-8") as f:
    f.write("【プラス誤差上位5件】\n")
    f.write(top_pos.to_string(index=False))
    f.write("\n\n【マイナス誤差上位5件】\n")
    f.write(top_neg.to_string(index=False))

# 出力：CSVファイル
top_pos.to_csv("top_pos_outliers.csv", index=False, encoding="utf-8-sig")
top_neg.to_csv("top_neg_outliers.csv", index=False, encoding="utf-8-sig")
