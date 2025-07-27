import pandas as pd
import numpy as np
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error

# ----------------------------
# データ読み込み & 欠損除去
# ----------------------------
df = pd.read_csv("rent_oita_processed.csv")
df_model = df[["log_家賃_per_㎡", "築年数_num", "徒歩分_num", "面積_num", "駅名"]].dropna()

# 説明変数のダミー化
X = pd.get_dummies(df_model[["築年数_num", "徒歩分_num", "面積_num", "駅名"]], drop_first=True)
y = df_model["log_家賃_per_㎡"]

# スケーリング（Lassoは標準化が必要）
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ----------------------------
# Lasso回帰（交差検証でα選択）
# ----------------------------
lasso = LassoCV(cv=5, random_state=0)
lasso.fit(X_scaled, y)

# ----------------------------
# 係数の抽出
# ----------------------------
coef_df = pd.DataFrame({
    "変数名": X.columns,
    "係数": lasso.coef_
}).sort_values(by="係数", key=abs, ascending=False)

# ----------------------------
# 結果をテキストファイルに保存
# ----------------------------
with open("lasso_result.txt", "w", encoding="utf-8") as f:
    f.write(f"[INFO] 最適な α（正則化強度）: {lasso.alpha_:.5f}\n")
    f.write(f"[INFO] 決定係数 R²: {lasso.score(X_scaled, y):.4f}\n\n")
    f.write("[INFO] 非ゼロ係数の変数一覧:\n")
    f.write(coef_df[coef_df["係数"] != 0].to_string(index=False))

# ----------------------------
# 予測値を元のデータに追加し保存
# ----------------------------
y_pred = lasso.predict(X_scaled)
df_pred = df_model.copy()
df_pred["log_家賃_per_㎡_lasso_pred"] = y_pred
df_final = df.copy()
df_final.loc[df_pred.index, "log_家賃_per_㎡_lasso_pred"] = y_pred
df_final.to_csv("rent_oita_with_lasso_prediction.csv", index=False, encoding="utf-8-sig")

print("[INFO] Lasso回帰の結果を lasso_result.txt に出力しました。")
print("[INFO] 予測列を含むCSVファイルを rent_oita_with_lasso_prediction.csv に保存しました。")
