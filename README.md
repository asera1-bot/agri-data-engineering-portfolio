# Agricultural Data Engineering Portfolio

## Overview
目的：
収穫データには表記ゆれ、欠損、重複、不正値などが含まれることを想定して、
そのままDBへ登録をしないようにETLパイプラインを構築しました。

処理：
Extract　→　Transform　→　Validate　の順に処理を行い、
検証結果を　OK　/　WARNING　/　ERROR　に分類しました。

保存：
OK・WARNING　→　fact_harvest
ERROR　→　quarantine_harvest

活用：
PostgreSQLに蓄積したデータをSQLで集計し、
Streamlitで可視化する。

デプロイ：
AWS　EC2上に環境構築をおこない、ブラウザからStreamlitへアクセスできるようにしました。

## Architecture
```text
Sample CSV
    ↓
Extract
    ↓
Transform
    ↓
Validate
    ├── OK ──────────→ fact_harvest
    ├── WARNING ─────→ fact_harvest + reason
    └── ERROR ───────→ quarantine_harvest
                            ↓
                       PostgreSQL
                            ↓
                         SQL Analysis
                            ↓
                        Streamlit
                            ↓
                         AWS EC2
```

## Directory Structure
```text
src/
├── extract/
├── transform/
├── validate/
├── load/
└── pipeline.py

sql/
├── schema.sql
└── analysis/

sample_data/

docker-compose.yml
requirements.txt
```

・extract：データの読み込み
・transform：データの加工、編集
・validate：データの検証
・load：データのDBへの蓄積
・pipeline：extract,transform,validate,loadの実行を一つのコマンドで行うため作成
・schema.sql：PostgreSQLのテーブル構造・制約をコードとして管理し、同じDB構造を別環境でも再現できるようにする

## Data Quality Rules
| Status | Rule | 処理 |
|---|---|---|
| OK | 正常なデータ | fact_harvestへ保存 |
| WARNING | possible_duplicate | fact_harvestへ保存し、reasonを保持 |
| WARNING | unusual_quantity | fact_harvestへ保存し、reasonを保持 |
| ERROR | duplicate_harvest_id | quarantine_harvestへ隔離 |
| ERROR | unknown_crop | quarantine_harvestへ隔離 |
| ERROR | unknown_farm | quarantine_harvestへ隔離 |
| ERROR | unknown_client | quarantine_harvestへ隔離 |
| ERROR | invalid_date | quarantine_harvestへ隔離 |
| ERROR | future_date | quarantine_harvestへ隔離 |
| ERROR | invalid_quantity | quarantine_harvestへ隔離 |

possible_duplicateがWARNINGである理由は、現実に同じ農園、日付、作物、収量の収穫はありえるため。
そのため、機械的に排除せずに、人間の目で確認できるようにfactに残しています。

## Database Design
fact_harvest
    正常データ + 要確認データ
    OK / WARNING

quarantine_harvest
    DB本体へ入れられないデータ
    ERROR

ERRORデータは削除せず隔離することで、エラー件数・原因・対象レコードを追跡可能にしています。
元データを確認・修正した後、再度パイプラインを実行することで正常データとして取り込める設計としています。

## How to Run
git clone https://github.com/asera1-bot/agri-data-engineering-portfolio.git
cd agri-data-engineering-portfolio

cp .env.example .env

.env の PostgreSQL 接続情報を環境に合わせて設定

docker compose up -d

PostgreSQLテーブルの作成
psql -h localhost -p 5433 \
  -U portfolio \
  -d agri_data \
  -f sql/schema.sql

Python環境を作成し、依存ライブラリをインストール
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python -m src.pipeline

Streamlitを起動
streamlit run app/app.py
