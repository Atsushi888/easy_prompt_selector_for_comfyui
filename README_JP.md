# Easy Prompt Selector For ComfyUI（日本語）

`ill_hair.yml` を読み込み、  
髪型・前髪・髪色などを **ドロップダウンで選択**しながら  
1本のプロンプト文字列を生成する ComfyUI 用カスタムノードです。

LoRA 学習や量産生成など、  
**プロンプトの安定性が重要な用途**を想定しています。

---

## 特徴

- `ill_hair.yml` を ComfyUI 起動時に一括読み込み
- 全カテゴリをドロップダウン UI で選択可能
- 指定したカテゴリは自動でデフォルト選択
- 出力は STRING（他ノードと接続しやすい）
- 起動中に YAML を編集しない前提の安定設計

---

## インストール手順

### 1. ComfyUI の custom_nodes ディレクトリへ移動

```bash
cd /workspace/ComfyUI/custom_nodes
```

### 2. リポジトリを clone

```bash
git clone https://github.com/Atsushi888/easy_prompt_selector_for_comfyui.git
```

### 3. 依存ライブラリをインストール

```bash
pip install pyyaml
```

### 4. ComfyUI を再起動

---

## 使い方

1. ComfyUI を起動
2. ノード検索で  
   **Easy Prompt Selector (All Hair from YAML)** を追加
3. 各カテゴリをドロップダウンで選択
4. 出力された `prompt (STRING)` を以下へ接続  
   - Text Concatenate / Join ノード  
   - または CLIP Text Encode ノード

---

## デフォルト自動選択について

`easy_prompt_selector/__init__.py` 内の  
以下の設定で制御します。

```python
DEFAULT_AUTO_SELECT_CATEGORIES = [
    "前髪",
    "髪色（単色）",
]
```

ここに指定されたカテゴリは：

- 空の選択肢が表示されません
- YAML 内の **先頭項目が自動選択**されます

「必須だが厳密なチェックは不要」という用途向けの設計です。

---

## 注意事項

- `ill_hair.yml` は ComfyUI 起動時に一度だけ読み込まれます
- YAML を編集した場合は **必ず ComfyUI を再起動**してください
- 起動中の動的リロードは意図的にサポートしていません

---

## ライセンス

MIT License
