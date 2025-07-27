import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

# ----------------------------
# データ読み込み
# ----------------------------
df = pd.read_csv("rent_oita_processed.csv")

# ----------------------------
# 欠損除去 & 対象列の抽出
# ----------------------------
df_model = df[["log_家賃_per_㎡", "築年数_num", "徒歩分_num", "面積_num", "駅名"]].dropna()

# ----------------------------
# 説明変数のダミー変数化
# ----------------------------
X = pd.get_dummies(df_model[["築年数_num", "徒歩分_num", "面積_num", "駅名"]], drop_first=True)

# 目的変数
y = df_model["log_家賃_per_㎡"]

# 定数項追加
X = sm.add_constant(X)

# データ型をfloatに明示
X = X.astype(float)
y = y.astype(float)

# ----------------------------
# 回帰モデル構築
# ----------------------------
model = sm.OLS(y, X).fit()

# ----------------------------
# VIF（多重共線性）の確認
# ----------------------------
vif_df = pd.DataFrame()
vif_df["変数"] = X.columns
vif_df["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]

# ----------------------------
# 回帰結果をテキストファイルに保存
# ----------------------------
with open("regression_result.txt", "w", encoding="utf-8") as f:
    f.write(model.summary().as_text())
    f.write("\n\n[ VIF（多重共線性チェック） ]\n")
    f.write(vif_df.to_string(index=False))

# ----------------------------
# 予測値を元のデータに追加し保存
# ----------------------------

# 元の df に対応する予測値を追加（欠損を除いた行のみ）
df_pred = df_model.copy()
df_pred["log_家賃_per_㎡_pred"] = model.predict(X)

# 元の df に予測列をマージ（indexベースで）
df_final = df.copy()
df_final.loc[df_pred.index, "log_家賃_per_㎡_pred"] = df_pred["log_家賃_per_㎡_pred"]

# 保存
df_final.to_csv("rent_oita_with_prediction.csv", index=False, encoding="utf-8-sig")

print("[INFO] 回帰結果を regression_result.txt に出力しました。")
print("[INFO] 予測列を含むCSVファイルを rent_oita_with_prediction.csv に保存しました。")
