import pandas as pd
import re

# CSV読み込み
df = pd.read_csv("rent_oita_full.csv")

# ----------------------------
# 築年数：「新築」→0、「築10年」→10
# ----------------------------
def parse_age(x):
    if pd.isna(x):
        return None
    if "新築" in x:
        return 0
    match = re.search(r"築\s*(\d+)", x)
    return int(match.group(1)) if match else None

df["築年数_num"] = df["築年数"].apply(parse_age)

# ----------------------------
# 面積：「40.5㎡」→ 40.5（float）
# ----------------------------
def parse_area(x):
    if pd.isna(x):
        return None
    match = re.search(r"([\d\.]+)", x)
    return float(match.group(1)) if match else None

df["面積_num"] = df["面積"].apply(parse_area)

# ----------------------------
# 家賃：「6.8万円」→ 6.8
# ----------------------------
def parse_rent(x):
    if pd.isna(x):
        return None
    match = re.search(r"([\d\.]+)", x)
    return float(match.group(1)) if match else None

df["家賃_num"] = df["家賃"].apply(parse_rent)

# ----------------------------
# 徒歩分数：「○○駅 歩7分」→ 7
# ----------------------------
def parse_walk_minutes(x):
    if pd.isna(x):
        return None
    match = re.search(r"歩\s*(\d+)分", x)
    return int(match.group(1)) if match else None

df["徒歩分_num"] = df["徒歩分"].apply(parse_walk_minutes)

# ----------------------------
# 駅名の抽出（形式1：/大分駅 歩10分）
# ----------------------------
def extract_station(x):
    if pd.isna(x):
        return None
    match = re.search(r"/([^/ ]+?駅)", x)
    return match.group(1) if match else None

df["駅名"] = df["徒歩分"].apply(extract_station)

# ----------------------------
# 駅名が欠損している行を、「○○駅 歩X分」形式から補完
# ----------------------------
def fallback_station_name(x):
    if pd.isna(x):
        return None
    match = re.search(r"([^\s/]+駅)", x)
    return match.group(1) if match else None

df["駅名"] = df["駅名"].combine_first(df["徒歩分"].apply(fallback_station_name))
def fallback_station_name(x):
    if pd.isna(x):
        return None
    match = re.search(r"([^\s/]+駅)", x)
    return match.group(1) if match else None

df["駅名"] = df["駅名"].combine_first(df["徒歩分"].apply(fallback_station_name))

# ----------------------------
# 家賃／面積（万円/㎡）の計算
# ----------------------------
df["家賃_per_㎡"] = df["家賃_num"] / df["面積_num"]
# ----------------------------

# 家賃_per_㎡の対数値を追加
# ----------------------------
import numpy as np
df["log_家賃_per_㎡"] = np.log(df["家賃_per_㎡"])

# ----------------------------
# 保存
# ----------------------------
df.to_csv("rent_oita_processed.csv", index=False, encoding="utf-8-sig")
print("[INFO] 前処理完了。保存ファイル: rent_oita_processed.csv")