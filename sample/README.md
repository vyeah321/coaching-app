# コーチングアプリサンプル集

このディレクトリには、コーチング業務をサポートする3つのStreamlitアプリケーションが含まれています。

## 📁 アプリ一覧

### 1. coaching_support_app - コーチ向け管理アプリ
コーチがクライアントやセッションを管理するための業務用アプリ

**主な機能:**
- クライアント情報の管理
- セッション記録
- 目標設定とトラッキング
- レポート生成

**起動方法:**
```bash
cd coaching_support_app
pip install -r requirements.txt
streamlit run app.py
```

**アクセス:** http://localhost:8501

詳細は [coaching_support_app/README.md](coaching_support_app/README.md) を参照

---

### 2. client_motivation_app - クライアント向けモチベーションアプリ
クライアントが自分で使うゲーミフィケーション型目標管理アプリ

**主な機能:**
- レベルシステムとバッジコレクション
- 目標設定と進捗トラッキング
- 毎日の振り返り
- 達成時のアニメーション効果

**起動方法:**
```bash
cd client_motivation_app
pip install -r requirements.txt
streamlit run app.py --server.port 8081
```

**アクセス:** http://localhost:8081

詳細は [client_motivation_app/README.md](client_motivation_app/README.md) を参照

---

### 3. personality_insights - パーソナリティインサイト診断アプリ
クライアントが自分の強みやスタイルを発見する診断アプリ

**主な機能:**
- 強み診断（5つの才能）
- コミュニケーションスタイル診断
- リーダーシップスタイル診断
- レーダーチャートによる結果表示

# ターミナル3
cd personality_insights && streamlit run app.py --server.port 8503
- 診断履歴の保存

**起動方法:**
```bash
cd personality_insights
pip install -r requirements.txt
streamlit run app.py --server.port 8503
```

| 強み・適性診断 | personality_insights | クライアント |
| 自己理解 | personality_insights | クライアント |
| スタイル分析 | personality_insights | コーチ/クライアント |
**アクセス:** http://localhost:8503

詳細は [personality_insights/README.md](personality_insights/README.md) を参照

---

## 🚀 すべてを同時に起動する

```bash
# ターミナル1
cd coaching_support_app && streamlit run app.py

# ターミナル2
cd client_motivation_app && streamlit run app.py --server.port 8081
```

## 📊 アプリの使い分け

| 用途 | アプリ | ユーザー |
|------|--------|----------|
| クライアント管理 | coaching_support_app | コーチ |
| セッション記録 | coaching_support_app | コーチ |
| レポート確認 | coaching_support_app | コーチ |
| 個人の目標管理 | client_motivation_app | クライアント |
| モチベーション維持 | client_motivation_app | クライアント |
| 毎日の振り返り | client_motivation_app | クライアント |

## 🔧 開発環境
、`client_data/`、`results/`）
- すべてのython 3.8以上
- Streamlit 1.30.0以上

## 📝 注意事項

- データは各アプリのディレクトリ内に保存されます（`data/` または `client_data/`）
- 両アプリは独立して動作し、データの共有はありません
- 本番環境で使用する場合は、適切な認証とデータベースの実装を推奨します
