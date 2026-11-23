# 第5回 解答

## 演習

- 回答モデル（実行時の`[model]`）：gemini-3.5-flash-lite
- 比較した質問："第2回の説明では、LoRAは何を固定し何を学習しますか？ QLoRAは何を加えますか？"
- 対象資料（全文投入と他の方式で範囲が違う点も記録）：
compare.txt

### 各方式の結果

| 方式 | 回答の要点・正しさ | 引用ページと根拠 | 時間（秒） | 入力／出力トークン数 | モデル応答回数 | 生成API推定費用（USD） |
|---|---|---|---|---|---|---|
| 全文投入 |回答は避けており、該当する資料の閲覧を促している。記載範囲内は正しい。 |PDF p.51、PDF p.52 |4.11 秒 |入力 117,025 tokens 出力 263 token |1回 |0.004809 USD |
| ベクトル検索 |とても簡潔に項目ごとに分けて答えている、正しい。 |第2回・PDF p.51, p.52 |4.75 秒 |入力 3,027 tokens 出力 201 tokens |2回 |0.001411 USD |
| Tree |簡潔に項目ごとに分けて答えている、正しい。 |第2回・PDF p.52 |12.72 秒 |入力 9,214 tokens 出力 293 tokens |5回 |0.003497 USD |
| Graph |簡潔に項目ごとに分けて答えている、正しい。 |第2回・PDF p.51, p.52 | 3.17 秒|入力 5,771 tokens 出力 203 tokens |2回 |0.001691 USD |

<!-- 未実行・算定不可の場合は、その旨を書いてください。質問を追加した場合は、質問ごとに表を分けてください。 -->

- 検索だけを実行して見つかったページと、その本文で確認できたこと：
P.52, 51, 60, 47, 61

- `--trace`で見えたツール呼び出し（ツール名・引数・回数、Treeでたどった目次など）：
・ベクトル検索
[tool call]   search_materials({'query': 'LoRA QLoRA 固定 学習'})
[tool return] search_materials -> {"results": [{"page_id": "lec02-main-p052", "document_id": "lec02-main", "lecture": 2, "document_title": "基盤モデルの仕組み", "s…
・Tree
[tool call]   browse_tree({'node_id': 'lec02-main-p052'})
[目次を開く] AIエンジニアリング実践講座2026 資料 → 基盤モデルの仕組み → 選んだモデルを、いつ・どう直すか → LoRA と QLoRA ：大きなモデルも GPU 1 台で調整できる
    （末端ページ・本文717文字を取得）
・Graph
[tool call]   search_graph({'query': 'LoRA QLoRA 固定 学習'})
[tool return] search_graph -> {"seeds": [{"page_id": "lec02-main-p052", "document_id": "lec02-main", "lecture": 2, "document_title": "基盤モデルの仕組み", "sec…

- 取得した情報が足りなかった例、取得できたのに回答へ使えなかった例：
Tree検索ではPDFp.51の参照が足りなかった
- 今回の用途に採用したい方式と、その理由・比較条件の限界、気づき・疑問：
Treeは抜けるし、時間がかかるのであまり使いたくない。


## 宿題

<!-- 基礎・実装・発展のどれか1つに取り組めば完了です。 -->

- 取り組んだレベル：基礎 
- やったこと（変更したファイル・設定・処理、または設計した取得方法）：
app/tools.pyのdocstringを変更した
search_glossary関数内
講座の用語集から用語を検索し、定義と、どの回で扱うかを返す。
AIエンジニアリングの用語や、この講座（AIE2026）に固有の言葉について
答える前に使うこと。query には調べたい用語を複数入れる。

- 比較した質問と、固定した条件（モデル・対象資料など）：
比較した質問："第2回の説明では、LoRAは何を固定し何を学習しますか？ QLoRAは何を加えますか？"
モデルや対象資料は固定

- 結果（変更前後の回答・根拠、`--trace`の出力、時間・トークン数・生成API推定費用など）：
・全文検索
[full-context] 入力227,979文字
PDF p.51〜52ページ

・ベクトル検索
第2回・PDF p.51, p.52
[tool call]   search_materials({'query': 'LoRA 固定 学習 QLoRA 加える'})
[tool return] search_materials -> {"results": [{"page_id": "lec02-main-p052", "document_id": "lec02-main", "lecture": 2, "document_title": "基盤モデルの仕組み", "s…
[time] 回答完了まで 3.11 秒（検索・埋め込みを含む）
[usage] 入力 3,028 tokens / 出力 166 tokens / モデル応答 2 回
[cost] 生成APIの推定コスト: $0.001323 USD（埋め込み・索引構築分は含まない）

・Tree
第2回・PDF p.52
[tool call]   browse_tree({'node_id': 'lec02-main-p052'})
[目次を開く] AIエンジニアリング実践講座2026 資料 → 基盤モデルの仕組み → 選んだモデルを、いつ・どう直すか → LoRA と QLoRA ：大きなモデルも GPU 1 台で調整できる
    （末端ページ・本文717文字を取得）
[time] 回答完了まで 5.88 秒（検索・埋め込みを含む）
[usage] 入力 9,214 tokens / 出力 287 tokens / モデル応答 5 回
[cost] 生成APIの推定コスト: $0.003482 USD（埋め込み・索引構築分は含まない）

・Graph
第2回・PDF p.51, p.52
[tool call]   search_graph({'query': 'LoRA QLoRA 固定 学習'})
[tool return] search_graph -> {"seeds": [{"page_id": "lec02-main-p052", "document_id": "lec02-main", "lecture": 2, "document_title": "基盤モデルの仕組み", "sec…
[time] 回答完了まで 3.62 秒（検索・埋め込みを含む）
[usage] 入力 5,771 tokens / 出力 220 tokens / モデル応答 2 回
[cost] 生成APIの推定コスト: $0.001733 USD（埋め込み・索引構築分は含まない）

- 改善した例と、残る失敗・制約、気づき・疑問：
参照が複数並列（p.51,52）になることが増えた
全検索ではヒントをくれるのみにとどまっている。
