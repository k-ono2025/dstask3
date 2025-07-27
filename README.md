# データサイエンス特論第一第3回課題
## 概要
このプロジェクトは、大分市内の賃貸物件データを用いて、家賃に影響を与える要因をLasso回帰によって分析するものです。<br>
面積・築年数・駅距離・間取り・最寄駅などの特徴量が、家賃にどのような影響を与えるかを可視化・定量化します。<br>

- SUUMOサイトからの物件データ収集（スクレイピング）<br>
- データの前処理<br>
- Lasso回帰分析の実施<br>
- 分析結果の可視化と出力<br>

---

## ファイル構成

task2/<br>
├── suumo_scraper_oita_full.py            # SUUMOから物件データを収集するスクレイピングスクリプト<br>
├── rent_oita_full.csv                    # 収集した生データ<br>
├── normalization.py                      # 前処理・正規化用スクリプト<br>
├── rent_oita_processed.csv              # 正規化・ダミー変数化後のデータ<br>
├── lasso_reg.py                          # Lasso回帰のメインスクリプト<br>
├── lasso_result.txt                      # 回帰結果（係数・R²など）のログ出力<br>
├── rent_oita_with_lasso_prediction.csv  # Lasso回帰による予測値付きデータ<br>
├── plot3.py                              # プロットスクリプト（誤差・残差の可視化）<br>
├── top_pos_neg_outliers.txt             # プラス/マイナス誤差の大きい物件リスト<br>
├── top_neg_outliers.csv                 # 負の誤差が大きい物件の詳細リスト<br>
