"""
데이터 저장 모듈
- CSV, PKL 저장
- 품목명 텍스트 임베딩 (sentence-transformers 또는 간단한 TF-IDF)
"""
import os
import pickle
import pandas as pd
import numpy as np
from config import DATA_DIR, ITEMS

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(f"{DATA_DIR}/embeddings", exist_ok=True)

def save(df: pd.DataFrame, name: str):
    """CSV + PKL 저장"""
    if df is None or df.empty:
        print(f"  ⚠️  {name}: 데이터 없음, 저장 스킵")
        return
    csv_path = f"{DATA_DIR}/{name}.csv"
    pkl_path = f"{DATA_DIR}/{name}.pkl"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    df.to_pickle(pkl_path)
    print(f"  💾 {name}: {len(df)}행 저장 → {csv_path}, {pkl_path}")

def make_embeddings(dfs: dict):
    """
    품목명 기반 임베딩 생성
    sentence-transformers 있으면 사용, 없으면 TF-IDF 벡터로 대체
    """
    # 모든 df에서 품목명 텍스트 수집
    texts = []
    for name, df in dfs.items():
        if df is not None and not df.empty and "품목명" in df.columns:
            for _, row in df.iterrows():
                item = row.get("품목명", "")
                price_cols = [c for c in df.columns if "가격" in c or "price" in c.lower()]
                price_str = " ".join([f"{c}:{row.get(c,'')}" for c in price_cols[:3]])
                texts.append(f"{item} {price_str}".strip())

    texts = list(set(texts))  # 중복 제거
    print(f"  임베딩 대상 텍스트: {len(texts)}개")

    try:
        from sentence_transformers import SentenceTransformer
        print("  sentence-transformers 사용...")
        model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
        vectors = model.encode(texts, show_progress_bar=True)
        method = "sentence_transformers"
    except ImportError:
        print("  sentence-transformers 없음 → TF-IDF 벡터 사용...")
        from sklearn.feature_extraction.text import TfidfVectorizer
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(texts).toarray()
        method = "tfidf"

    emb_data = {
        "texts": texts,
        "vectors": vectors,
        "method": method,
        "items": [i["name"] for i in ITEMS],
    }
    path = f"{DATA_DIR}/embeddings/items_embedding.pkl"
    with open(path, "wb") as f:
        pickle.dump(emb_data, f)
    print(f"  💾 임베딩 저장 → {path} (방법: {method}, shape: {np.array(vectors).shape})")
    return emb_data

if __name__ == "__main__":
    # 저장된 pkl 불러와서 임베딩 테스트
    test = {}
    for fname in os.listdir(DATA_DIR):
        if fname.endswith(".pkl") and "embedding" not in fname:
            key = fname.replace(".pkl", "")
            test[key] = pd.read_pickle(f"{DATA_DIR}/{fname}")
    make_embeddings(test)
