ワークショップの手順：https://moulongzhang.github.io/2025-Github-Copilot-Workshop/github-copilot-workshop/#0

## プロジェクト概要

ポモドーロタイマーのフルスタック実装へ向けたステップ1を構築しました。Flask を使ったバックエンドとシンプルなフロントエンドで、以下を満たしています。

- アプリケーションファクトリー構成
- モデル／サービス／リポジトリ層の分離
- 25 分タイマーのカウントダウン、開始・リセット操作
- 1 秒ごとのポーリングによるリアルタイム更新
- インメモリでの今日のセッション進捗管理

## セットアップ

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements/development.txt
```

## ローカル実行

```bash
python app.py
```

ブラウザで `http://127.0.0.1:5000` を開くと、日本語 UI のポモドーロタイマーが表示されます。

`POMODORO_CONFIG` 環境変数を設定すると `development` / `testing` / `production` いずれかの設定を切り替えられます（デフォルトは `development`）。

## テスト

```bash
pytest
```

現時点ではタイマーのビジネスロジックに対するユニットテストを提供しています。今後のステップでサービス層や API テストを拡充する予定です。
