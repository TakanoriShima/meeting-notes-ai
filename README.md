# 会議メモ AI 構造化ツール

Gemini API の Structured Output を利用して、**非構造化された会議メモを、業務で扱いやすい構造化データへ変換する AI アプリケーション**です。

Streamlit による Web UI から会議メモを入力すると、Gemini API が内容を分析し、以下の情報を自動的に整理します。

- 会議内容の要約
- 決定事項
- TODO
- TODO の担当者
- TODO の期限

さらに、構造化した結果を **JSON / CSV ファイルとしてダウンロード**できます。

---

## デモ

### ① 会議メモを入力

Streamlit の Web UI から、自由形式の会議メモを入力します。

[![会議メモ入力画面](https://i.gyazo.com/6a76a1f66b23703326873faf1045ad71.png)](https://gyazo.com/6a76a1f66b23703326873faf1045ad71)

入力例：

```text
田中さんと佐藤さんで営業会議を実施。

新商品の発売日は10月1日に決定。

田中さんが9月15日までに商品資料を作成する。

佐藤さんは9月20日までに顧客リストを確認する。
```

入力後、**「会議メモを構造化する」** ボタンをクリックします。

### ② Gemini API による構造化

入力された会議メモを Gemini API が分析し、あらかじめ定義したデータ構造に沿って情報を整理します。

```text
会議メモ
   │
   ▼
Gemini API
   │
   ▼
Structured Output
   │
   ├── 要約
   ├── 決定事項
   └── TODO
         ├── 担当者
         └── 期限
```

### ③ AI による構造化結果

AI によって、会議内容から要約・決定事項・TODO が整理されます。

[![AIによる構造化結果](https://i.gyazo.com/804bbec155c0bea82c82783b239921f2.png)](https://gyazo.com/804bbec155c0bea82c82783b239921f2)

#### 要約

田中さんと佐藤さんによる営業会議。新商品の発売日の決定および各自の準備タスクを確認した。

#### 決定事項

- 新商品の発売日を 10 月 1 日に決定

#### TODO

| タスク               | 担当者 | 期限       |
| -------------------- | ------ | ---------- |
| 商品資料を作成する   | 田中   | 9 月 15 日 |
| 顧客リストを確認する | 佐藤   | 9 月 20 日 |

### ④ JSON / CSV として出力

構造化された結果は、アプリケーション上で確認できるだけでなく、ファイルとしてダウンロードできます。

**JSON**

```json
{
  "summary": "田中さんと佐藤さんによる営業会議。新商品の発売日の決定および各自の準備タスクを確認した。",
  "decisions": ["新商品の発売日を10月1日に決定"],
  "todos": [
    {
      "task": "商品資料を作成する",
      "owner": "田中",
      "due_date": "9月15日"
    },
    {
      "task": "顧客リストを確認する",
      "owner": "佐藤",
      "due_date": "9月20日"
    }
  ]
}
```

**CSV**

```text
タスク,担当者,期限
商品資料を作成する,田中,9月15日
顧客リストを確認する,佐藤,9月20日
```

JSON は後続のアプリケーションや API 連携、CSV は Excel などでのデータ活用を想定しています。

---

## 背景・目的

会議メモは自然言語で記録されることが多く、そのままではタスク管理や業務システムへの登録に利用しにくいという課題があります。

本アプリでは、生成 AI を利用して会議メモから、

- 要約
- 決定事項
- TODO
- 担当者
- 期限

を構造化データとして抽出します。

これにより、会議後の情報整理を効率化するとともに、後続の業務システムや自動化処理へ接続しやすいデータ形式に変換します。

---

## 主な機能

### 1. 会議メモ入力

Streamlit のテキストエリアから、自由形式の会議メモを入力できます。

### 2. AI による構造化

Gemini API を利用して、会議メモから以下の情報を抽出します。

- 要約
- 決定事項
- TODO
- 担当者
- 期限

### 3. Structured Output

Gemini API の Structured Output を利用し、AI の出力をあらかじめ定義したデータ構造に沿った JSON として取得します。

単なる自然言語による AI 応答ではなく、後続のプログラムや業務システムで利用しやすい形式でデータを取得することを目的としています。

### 4. Pydantic によるデータ検証

Pydantic でデータモデルを定義し、Gemini API から返された JSON を検証しています。

```python
class Todo(BaseModel):
    task: str
    owner: str
    due_date: str
```

```python
class MeetingNotes(BaseModel):
    summary: str
    decisions: list[str]
    todos: list[Todo]
```

### 5. JSON ダウンロード

構造化された会議メモを `meeting_notes.json` としてダウンロードできます。

### 6. CSV ダウンロード

TODO 情報を CSV に変換し、Excel などで利用できる形式でダウンロードできます。

---

## 設計上のポイント

### 1. 非構造化データから構造化データへの変換

自然言語で記録された会議メモを、後続のシステムで利用しやすい JSON 形式へ変換しています。

### 2. Structured Output による出力形式の制御

Gemini API の Structured Output を利用し、あらかじめ定義したデータ構造に沿って AI の出力を取得しています。

### 3. Pydantic によるデータモデル検証

Gemini API から返された JSON を Pydantic モデルで検証し、アプリケーション側で扱うデータ構造の整合性を確保しています。

### 4. 後続の業務システムへの連携を想定

JSON / CSV として出力できる設計とし、将来的に Power Automate、SharePoint などの業務システムへ連携できる構成を意識しています。

---

## システム構成

```text
┌──────────────────────┐
│      Streamlit       │
│   会議メモ入力画面   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│      Gemini API      │
│   gemini-3.6-flash   │
│   Structured Output  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│      Pydantic        │
│    データモデル検証  │
└──────────┬───────────┘
           │
           ▼
      構造化されたデータ
           │
      ┌────┴────┐
      ▼         ▼
    JSON       CSV
  ダウンロード ダウンロード
```

---

## 技術スタック

| 技術              | 用途                   |
| ----------------- | ---------------------- |
| Python            | アプリケーション開発   |
| Streamlit         | Web UI                 |
| Gemini API        | 会議メモの AI 処理     |
| Gemini 3.6 Flash  | テキスト生成・構造化   |
| Structured Output | JSON 形式での出力制御  |
| Pydantic          | データモデル定義・検証 |
| pandas            | CSV 生成               |
| Git / GitHub      | ソースコード管理       |

---

## プロジェクト構成

```text
meeting-notes-ai/

├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit/
    └── secrets.toml
```

`secrets.toml` はローカル環境で作成し、Gemini API キーを設定します。

```toml
GEMINI_API_KEY = "YOUR_API_KEY"
```

API キーなどの機密情報は GitHub にコミットしないよう、`.gitignore` で管理しています。

---

## セットアップ

### 1. リポジトリをクローン

```bash
git clone https://github.com/TakanoriShima/meeting-notes-ai.git
cd meeting-notes-ai
```

### 2. 仮想環境を作成

```bash
python -m venv .venv
```

Windows の場合：

```powershell
.venv\Scripts\Activate.ps1
```

### 3. パッケージをインストール

```bash
pip install -r requirements.txt
```

### 4. Gemini API キーを設定

`.streamlit/secrets.toml` を作成します。

```toml
GEMINI_API_KEY = "YOUR_API_KEY"
```

### 5. Streamlit を起動

```bash
streamlit run app.py
```

ブラウザで表示された画面から会議メモを入力して利用できます。

---

## 想定する業務利用

このアプリは、以下のような業務への応用を想定しています。

- 会議メモの整理
- 議事録作成の補助
- 会議後の TODO 抽出
- 担当者・期限の整理
- 会議情報のデータベース登録
- 業務システムへのデータ連携

特に、**非構造化された自然言語を、後続の業務システムで利用できる構造化データへ変換する処理**を意識して設計しています。

### 業務利用イメージ

```text
会議メモ
   │
   ▼
Gemini API
   │
   ▼
構造化データ
   │
   ├── 要約
   ├── 決定事項
   ├── TODO
   ├── 担当者
   └── 期限
   │
   ▼
JSON / CSV
   │
   ▼
業務システム・Excel・自動化処理
```

将来的には、以下のような業務フローへの発展を想定しています。

```text
会議メモ
   ↓
生成AIによる情報抽出
   ↓
構造化データ
   ↓
Power Automate
   ↓
SharePoint / Teams / Excel
   ↓
タスク管理・通知・データ蓄積
```

---

## 今後の改善予定

今後は以下の機能追加を検討しています。

- 会議日時・参加者の抽出
- TODO の優先度判定
- 期限が記載されていない TODO への対応
- Excel 形式（xlsx）での出力
- 会議履歴の保存
- Streamlit 上での編集・修正機能
- Microsoft 365 / Power Automate との連携
- SharePoint への構造化データ登録

---

## 開発で得た知見

本プロジェクトでは、生成 AI を単純なチャット用途として利用するのではなく、

**「自然言語 → 構造化データ → 業務システムで利用可能な形式」**

という流れを意識して AI アプリケーションを設計・実装しました。

特に、Gemini API の Structured Output と Pydantic を組み合わせることで、生成 AI の出力をアプリケーション側で扱いやすいデータ構造として取得・検証する方法を実装しています。

また、JSON / CSV 出力まで実装することで、生成 AI の結果を単なる画面表示で終わらせず、**後続の業務処理へ接続できる形式に変換するところまで**を実装しています。
