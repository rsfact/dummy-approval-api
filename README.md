# 基幹システムの見積承認フローをエミュレートするAPI

## リンク集

- [操作パネル](https://dummy-approval-api.onrender.com)
- [Swagger](https://dummy-approval-api.onrender.com/docs)
- [Render.com](https://dummy-approval-api.onrender.com)

## デモの流れ

1. ブラウザで操作パネルを開きます。
2. 承認待ちの見積を承認中に移動させます。
3. Swaggerから承認するか、PowerAutomateなどから承認します。
4. ブラウザをリロードして確認します。

## 開発環境のセットアップ

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows の場合: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## 実行方法

1. バックエンドの起動:

   ```bash
   cd backend
   python main.py
   ```

   サーバーが[http://localhost:8000](http://localhost:8000) で起動します。

2. フロントエンドの表示:
   `http://localhost:8000` をウェブブラウザで開きます。
