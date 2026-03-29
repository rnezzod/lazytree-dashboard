# 🌲 LazyTree 研究ダッシュボード

**LazyTree** — 遅延評価型階層要約木による長文書RAGの効率化

## 概要

セグメント木の遅延伝播アイデアをLLM要約インデックスに応用した研究のダッシュボードです。

- 研究概要・実験結果の可視化
- GPT-4o-miniによる研究エージェントとの対話

## ローカル起動

```bash
pip install -r requirements.txt
OPENAI_API_KEY=sk-... python server.py
# → http://localhost:8787
```

## 主な実験結果

| 手法 | 構築コスト | キャッシュヒット |
|------|-----------|----------------|
| RAPTOR | 31 LLM calls（全ノード事前構築） | 0% |
| **LazyTree** | **0 calls（遅延評価）** | **100%（2回目以降）** |

→ 同一文書の集中クエリで **LLMコール90%削減**を確認。
