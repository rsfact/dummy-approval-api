Todo
Render.comにフロントとバックがデプロイされるようにする
Base URLを動的にする


# 基幹システムの見積もり承認フローをエミュレートするAPI

https://dummy-approval-api.onrender.com/docs
https://dummy-approval-api.onrender.com/frontend/index.html

## セットアップ

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

   サーバーが http://localhost:8000 で起動します。

2. フロントエンドの表示:
   `frontend/index.html` をウェブブラウザで開きます。

## デモの流れ

1. バックエンドサーバーを起動します。

2. ブラウザで `frontend/index.html` を開きます。

3. 画面に承認待ちの見積もり一覧が表示されます。

4. 任意の見積もりの「承認」ボタンをクリックします。

5. http://localhost:8000/docs でGETとPOSTをします。

6. ブラウザをリロードして確認します。

## API仕様

APIの詳細な仕様については、サーバー起動後に http://localhost:8000/docs にアクセスしてSwagger UIをご確認ください。
