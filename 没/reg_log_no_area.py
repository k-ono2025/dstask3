import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

# ----------------------------
# データ読み込み
# ----------------------------
df = pd.read_csv("rent_oita_processed.csv")

# ----------------------------
# 必要な列だけ抽出（面積_num は除外）
# ----------------------------
df_model = df[["log_家賃_per_㎡", "築年数_num", "徒歩分_num", "駅名"]].dropna()

# ダミー変数化（駅名のみ）
X = pd.get_dummies(df_model[["築年数_num", "徒歩分_num", "駅名"]], drop_first=True)

# 目的変数
y = df_model["log_家賃_per_㎡"]

# 定数項追加
X = sm.add_constant(X)

# 型変換（念のため）
X = X.astype(float)
y = y.astype(float)

# ----------------------------
# OLS回帰モデル
# ----------------------------
model = sm.OLS(y, X).fit()

# ----------------------------
# VIFの計算
# ----------------------------
vif_df = pd.DataFrame()
vif_df["変数"] = X.columns
vif_df["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]

# ----------------------------
# 結果出力（テキスト保存）
# ----------------------------
with open("regression_result_no_area.txt", "w", encoding="utf-8") as f:
    f.write(model.summary().as_text())
    f.write("\n\n[ VIF（多重共線性チェック） ]\n")
    f.write(vif_df.to_string(index=False))

# ----------------------------
# 予測値を元データに追加して保存
# ----------------------------
df_pred = df_model.copy()
df_pred["log_家賃_per_㎡_no_area_pred"] = model.predict(X)
df_final = df.copy()
df_final.loc[df_pred.index, "log_家賃_per_㎡_no_area_pred"] = df_pred["log_家賃_per_㎡_no_area_pred"]
df_final.to_csv("rent_oita_with_prediction_no_area.csv", index=False, encoding="utf-8-sig")

print("[INFO] 面積を除いた回帰結果を regression_result_no_area.txt に出力しました。")
print("[INFO] 予測列を含むCSVファイルを rent_oita_with_prediction_no_area.csv に保存しました。")
