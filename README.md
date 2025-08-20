# HoikuNavi - 保育園見学管理アプリ

保育園の見学スケジュール管理と感想記録ができるWebアプリケーションです。

## 主な機能

- 🏫 **保育園情報管理** - 施設情報、連絡先、保育時間などを登録
- 📅 **見学スケジュール管理** - 見学日程の登録とGoogleカレンダー連携
- ⭐ **見学感想記録** - 5段階評価と詳細な感想を記録
- 🗺️ **地図連携** - Google Mapsで位置確認とルート検索
- 🔐 **ユーザー認証** - ログイン機能でデータを安全に管理

## 技術スタック

- **Backend**: Django 4.2
- **Database**: PostgreSQL (Supabase)
- **Frontend**: Bootstrap 5
- **Maps**: Google Maps (リンク連携)

## セットアップ

### 必要要件

- Python 3.9以上
- PostgreSQL (Supabaseアカウント)

### インストール手順

1. リポジトリをクローン
```bash
git clone [repository-url]
cd hoiku-navi
```

2. 仮想環境を作成して有効化
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. 依存パッケージをインストール
```bash
pip install -r requirements.txt
```

4. 環境変数を設定
`.env.example`をコピーして`.env`を作成し、必要な情報を入力：
```bash
cp .env.example .env
```

`.env`ファイルの内容：
```
# Supabase データベース設定
SUPABASE_DATABASE_URL=your_database_url_here
SUPABASE_PROJECT_URL=your_project_url_here

# Django設定
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Google Maps API（オプション）
GOOGLE_MAPS_API_KEY=
```

5. データベースマイグレーション
```bash
python manage.py migrate
```

6. 管理者ユーザーを作成
```bash
python manage.py createsuperuser
```

7. 開発サーバーを起動
```bash
python manage.py runserver
```

8. ブラウザでアクセス
```
http://localhost:8000/
```

## 使い方

1. **ログイン/新規登録**
   - 初回は「新規登録」からアカウントを作成
   - 既存ユーザーはログイン

2. **保育園登録**
   - サイドメニューから「保育園登録」を選択
   - 施設情報を入力して保存

3. **見学スケジュール登録**
   - 「見学予定追加」から日程を登録
   - Googleカレンダーボタンでカレンダーに追加可能

4. **見学感想記録**
   - 見学完了後、感想と評価を記録
   - 写真も3枚まで添付可能

## 無料で利用可能

このアプリケーションは以下の無料サービスを使用しています：

- **Supabase Free Plan**: 500MBまでのデータベース
- **Google Maps リンク**: APIキー不要で地図連携
- **Googleカレンダー連携**: APIキー不要でカレンダー追加

## ライセンス

MIT License

## 作者

HoikuNavi Development Team

## サポート

問題や要望がある場合は、Issuesに報告してください。