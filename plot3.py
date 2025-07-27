import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from adjustText import adjust_text

# Set font family for Japanese characters
matplotlib.rcParams['font.family'] = 'Hiragino Maru Gothic Pro'

# データの読み込み（Lassoモデルの予測値付きCSV）
# Load data (CSV with predicted values from Lasso model)
df = pd.read_csv("rent_oita_with_lasso_prediction.csv")

# 欠損除外
# Exclude rows with missing values in relevant columns
df = df.dropna(subset=["log_家賃_per_㎡", "log_家賃_per_㎡_lasso_pred"])

# 残差を計算 (予測値の列名を lasso_pred に変更)
# Calculate residuals (changed prediction column name to lasso_pred)
df["残差"] = df["log_家賃_per_㎡"] - df["log_家賃_per_㎡_lasso_pred"]

# 残差の正負に応じて上位3件ずつ抽出
# Extract top 3 positive and top 3 negative residuals
top_pos = df[df["残差"] > 0].sort_values(by="残差", ascending=False).head(3)
top_neg = df[df["残差"] < 0].sort_values(by="残差", ascending=True).head(3)

# 散布図の描画
# Create the scatter plot
plt.figure(figsize=(10, 8))
# 予測値の列名を lasso_pred に変更
plt.scatter(df["log_家賃_per_㎡_lasso_pred"], df["log_家賃_per_㎡"], alpha=0.6, label="データ点")
plt.plot([df["log_家賃_per_㎡"].min(), df["log_家賃_per_㎡"].max()],
         [df["log_家賃_per_㎡"].min(), df["log_家賃_per_㎡"].max()],
         color='red', linestyle='--', label="y=x")

# ラベル付きで上位誤差を表示
# Display top error points with labels
texts = []
for _, row in pd.concat([top_pos, top_neg]).iterrows():
    # 予測値の列名を lasso_pred に変更
    plt.scatter(row["log_家賃_per_㎡_lasso_pred"], row["log_家賃_per_㎡"], color='red')
    texts.append(plt.text(row["log_家賃_per_㎡_lasso_pred"], row["log_家賃_per_㎡"], row["物件名"], fontsize=9, color='red'))

# Adjust text labels to prevent overlap
adjust_text(texts, arrowprops=dict(arrowstyle='-', color='gray'))

# 軸ラベルとタイトルの更新
plt.xlabel("予測 log(家賃_per_㎡)")
plt.ylabel("実測 log(家賃_per_㎡)")
plt.title("実測 vs 予測の散布図（プラス誤差上位3件、マイナス誤差上位3件）")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 出力：ターミナル表示
print("[INFO] プラス誤差上位3件：")
print(top_pos[
    ["物件名", "所在地", "家賃_num", "面積_num", "築年数_num", "駅名", "徒歩分_num",
     "log_家賃_per_㎡", "log_家賃_per_㎡_lasso_pred", "残差"] # 列名を lasso_pred に変更
])

print("\n[INFO] マイナス誤差上位3件：")
print(top_neg[
    ["物件名", "所在地", "家賃_num", "面積_num", "築年数_num", "駅名", "徒歩分_num",
     "log_家賃_per_㎡", "log_家賃_per_㎡_lasso_pred", "残差"] # 列名を lasso_pred に変更
])

# 出力：テキストファイル
with open("top_pos_neg_outliers.txt", "w", encoding="utf-8") as f:
    f.write("【プラス誤差上位3件】\n")
    f.write(top_pos.to_string(index=False))
    f.write("\n\n【マイナス誤差上位3件】\n")
    f.write(top_neg.to_string(index=False))

# 出力：CSVファイル
top_pos.to_csv("top_pos_outliers.csv", index=False, encoding="utf-8-sig")
top_neg.to_csv("top_neg_outliers.csv", index=False, encoding="utf-8-sig")
