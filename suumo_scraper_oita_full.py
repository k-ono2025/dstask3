from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import re

# -------------------------
# 補助関数
# -------------------------

def extract_floor(floor_text):
    match = re.search(r'(\d+階)', floor_text)
    return match.group(1) if match else ""

def extract_station_name(text):
    match = re.search(r'/([^/ ]+?)駅', text)
    return match.group(1) + "駅" if match else ""

def safe_find_text(element, by, selector):
    try:
        return element.find_element(by, selector).text.strip()
    except:
        return ""

def safe_find_href(prop):
    try:
        a_tag = prop.find_element(By.CSS_SELECTOR, ".js-cassette_link_href")
        href = a_tag.get_attribute("href")
        # すでに https で始まっていればそのまま、そうでなければ補完
        if href.startswith("http"):
            return href
        else:
            return "https://suumo.jp" + href
    except Exception as e:
        print(f"[DEBUG] リンク取得失敗: {e}")
        return ""

# -------------------------
# Chrome起動オプション（ヘッドレス）
# -------------------------

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

base_url = "https://suumo.jp/chintai/oita/sc_oita/?page={}"
all_data = []

# -------------------------
# メイン処理：ページごとに取得
# -------------------------

for page in range(1, 21):  # ← ここで取得ページ数を調整（20ページ ≒ 約400件）
    print(f"[INFO] Fetching page {page}")
    driver.get(base_url.format(page))

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cassetteitem"))
        )
    except:
        print(f"[WARN] ページ {page} 読み込み失敗")
        continue

    properties = driver.find_elements(By.CLASS_NAME, "cassetteitem")
    print(f"[INFO] {len(properties)} 件の物件を検出")

    for prop in properties:
        try:
            name = safe_find_text(prop, By.CLASS_NAME, "cassetteitem_content-title")
            address = safe_find_text(prop, By.CLASS_NAME, "cassetteitem_detail-col1")
            station_text = safe_find_text(prop, By.CLASS_NAME, "cassetteitem_detail-col2")
            age_floor_text = safe_find_text(prop, By.CLASS_NAME, "cassetteitem_detail-col3")

            station = extract_station_name(station_text)
            floor = extract_floor(age_floor_text)
            age = age_floor_text.split()[0] if "築" in age_floor_text else ""

            # ✅ URLを取得（セレクタ修正済み）
            link = safe_find_href(prop)
            print("[DEBUG] URL取得:", link)

            rows = prop.find_elements(By.CLASS_NAME, "cassetteitem_other")
            for row in rows:
                floor_plan = safe_find_text(row, By.CLASS_NAME, "cassetteitem_madori")
                area = safe_find_text(row, By.CLASS_NAME, "cassetteitem_menseki")
                rent = safe_find_text(row, By.CLASS_NAME, "cassetteitem_price--rent")

                all_data.append({
                    "物件名": name,
                    "所在地": address,
                    "最寄り駅": station,
                    "徒歩分": station_text,
                    "築年数": age,
                    "階数": floor,
                    "間取り": floor_plan,
                    "面積": area,
                    "家賃": rent,
                    "URL": link
                })

        except Exception as e:
            print(f"[ERROR] 物件情報取得エラー: {e}")
            continue

driver.quit()

# -------------------------
# CSVに保存
# -------------------------

df = pd.DataFrame(all_data)
df.to_csv("rent_oita_full.csv", index=False, encoding="utf-8-sig")
print(f"[INFO] 保存完了。件数: {len(df)}")
