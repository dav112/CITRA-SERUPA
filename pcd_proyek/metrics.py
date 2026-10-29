import numpy as np

def precision_at_k(retrieved_labels, query_label, k=10):
    """
    Menghitung Precision@K: Proporsi citra yang relevan dalam daftar Top-K hasil pencarian.
    """
    retrieved_top_k = retrieved_labels[:k]
    if len(retrieved_top_k) == 0:
        return 0.0
    relevant_count = sum(1 for label in retrieved_top_k if label == query_label)
    return relevant_count / k

def recall_at_k(retrieved_labels, query_label, total_relevant_in_catalog, k=10):
    """
    Menghitung Recall@K: Proporsi item relevan yang berhasil ditemukan dalam Top-K 
    dibandingkan total item relevan di seluruh katalog.
    """
    if total_relevant_in_catalog <= 0:
        return 0.0
    retrieved_top_k = retrieved_labels[:k]
    relevant_count = sum(1 for label in retrieved_top_k if label == query_label)
    return relevant_count / total_relevant_in_catalog

def average_precision_at_k(retrieved_labels, query_label, k=10):
    """
    Menghitung Average Precision pada urutan Top-K (AP@K).
    """
    retrieved_top_k = retrieved_labels[:k]
    score = 0.0
    num_hits = 0.0
    for i, label in enumerate(retrieved_top_k):
        if label == query_label:
            num_hits += 1.0
            score += num_hits / (i + 1.0)
    return score / min(len(retrieved_top_k), k) if k > 0 else 0.0

def mean_average_precision(all_retrieved_labels, all_query_labels, k=10):
    """
    Menghitung Mean Average Precision (mAP@K) untuk seluruh query uji.
    """
    if not all_query_labels:
        return 0.0
    ap_scores = [
        average_precision_at_k(retrieved, query, k)
        for retrieved, query in zip(all_retrieved_labels, all_query_labels)
    ]
    return float(np.mean(ap_scores))

def mean_reciprocal_rank(all_retrieved_labels, all_query_labels):
    """
    Menghitung Mean Reciprocal Rank (MRR): Rata-rata dari 1 dibagi peringkat item relevan pertama.
    """
    if not all_query_labels:
        return 0.0
    rr_scores = []
    for retrieved, query in zip(all_retrieved_labels, all_query_labels):
        found = False
        for rank, label in enumerate(retrieved, 1):
            if label == query:
                rr_scores.append(1.0 / rank)
                found = True
                break
        if not found:
            rr_scores.append(0.0)
    return float(np.mean(rr_scores))
