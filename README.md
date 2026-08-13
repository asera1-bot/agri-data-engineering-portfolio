# agri-data-engineering-portfolio
Portfolio project for agricultural data engineering with Python, PostgreSQL, SQL, Docker and Streamlit.


### 開発Tips: tmuxでの画面スクロールとクリップボード共有（Linux向け）

本プロジェクトのターミナル環境で tmux を使用する際、タッチパッドによるスクロール範囲選択やブラウザへの直接コピー（Ctrl + C）を可能にするための設定と操作手順です。 

### 1. 事前準備（初回のみ）

Ubuntu環境にクリップボード共有ツールをインストールし、設定ファイルを配置します。 

bash

# クリップボードツールのインストール
sudo apt update && sudo apt install -y xsel

# tmux設定ファイルの作成・上書き
cat << 'EOF' > ~/.tmux.conf
# マウス機能を有効化
set -g mouse on

# コピーモードの操作を vi スタイルにする
set-window-option -g mode-keys vi

# 選択開始を「v」にする
bind-key -T copy-mode-vi v send-keys -X begin-selection

# コピー確定（確定と同時にブラウザへ共有）を「Enter」にする
bind-key -T copy-mode-vi Enter send-keys -X copy-pipe-and-cancel "xsel -bi"
EOF

# 反映のためにtmuxを一度再起動
tmux kill-server
tmux

コードは注意してご使用ください。

### 2. キーボードでのコピー＆ペースト手順

マウスやタッチパッドは使わず、以下のキーボード操作でページを跨いだ広範囲のコピーが可能です。 

1. **コピーモードに入る**: Ctrl + b を押した後に [ を押す（画面右上に [0/0] と表示される）
2. **移動**: 矢印キー または PageUp / PageDown でコピーしたい先頭位置へ移動する
3. **選択開始**: v キーを1回押す
4. **範囲指定**: 矢印キー または PageUp / PageDown で範囲を広げる（選択された部分が反転します）
5. **コピー確定**: Enter キーを押す（画面が自動で閉じ、クリップボードに保存される）
6. **貼り付け**: 

  * **ブラウザなど外部アプリ**: 通常通り Ctrl + v
  * **ターミナル（tmux内）**: Ctrl + b を押した後に ]

