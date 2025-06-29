# WhiteboardLM-Server

## 概要

WhiteboardLM-Server は WhiteboardLM-Web における認証サービスを提供するAPIサーバーです。  
ユーザー登録、ログイン、ログアウト、認証確認の機能を提供します。  

本リポジトリの他にも関連リポジトリがあります。  
そちらも参照してください。  

https://github.com/gerusuraimu-admin/whiteboardlm-frontend  
https://github.com/gerusuraimu-admin/WhiteboardLM-Proxy  
https://github.com/gerusuraimu-admin/WhiteboardLM-Bot

## エンドポイント

### 認証確認 (Authentication)

**エンドポイント**: `/auth`  
**メソッド**: POST  
**説明**: ユーザーの認証状態を確認します。  
**リクエスト本文**:

```json
{
  "uid": "ユーザーID",
  "session_id": "セッションID"
}
```

### ログイン (Login)

**エンドポイント**: `/login`  
**メソッド**: POST  
**説明**: ユーザー名とパスワードを使用してログインします。  
**リクエスト本文**:

```json
{
  "email": "メールアドレス",
  "password": "パスワード"
}
```

### ログアウト (Logout)

**エンドポイント**: `/logout`  
**メソッド**: POST  
**説明**: 現在のセッションからログアウトします。  
**リクエスト本文**:

```json
{
  "uid": "ユーザーID",
  "session_id": "セッションID"
}
```

### ユーザー登録 (Register)

**エンドポイント**: `/register`  
**メソッド**: POST  
**説明**: 新しいユーザーアカウントを作成します。  
**リクエスト本文**:

```json
{
  "email": "メールアドレス",
  "password": "パスワード"
}
```

### RAGデータソース更新 (Embedding)

**エンドポイント**: `/embed`  
**メソッド**: POST  
**説明**: ユーザーに紐づいたRAGコーパスのデータソースを更新する。  
**リクエスト本文**:

```json
{
  "uid": "ユーザーID",
  "session_id": "セッションID"
}
```

### クエリ実行 (Query)

**エンドポイント**: `/query`  
**メソッド**: POST  
**説明**: クエリを実行する。  
**リクエスト本文**:

```json
{
  "uid": "ユーザーID",
  "message": "メッセージ"
}
```

## レスポンス形式

すべてのエンドポイントは以下の形式でレスポンスを返します：

```json
{
  "status_code": 200,
  "content": {
    "key1": "value1",
    "key2": "value2"
  }
}
```
