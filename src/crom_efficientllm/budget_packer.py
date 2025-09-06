from typing import List, Dict
import logging

def enhanced_greedy_pack(chunks: List[Dict], budget: int, 
                        score_key: str = "score") -> tuple[List[Dict], Dict]:
    """
    기존 greedy_pack 함수를 확장하여 상세 통계 반환
    
    Returns:
        tuple: (packed_chunks, stats_dict)
    """
    if not chunks:
        return [], {
            "selected_count": 0,
            "packed_count": 0,
            "selected_tokens": 0,
            "packed_tokens": 0,
            "compression_ratio": 0.0,
            "token_savings": 0,
            "efficiency": 0.0
        }
    
    # 토큰 수 미리 계산
    for chunk in chunks:
        if "token_count" not in chunk:
            chunk["token_count"] = max(1, len(chunk.get("text", "")) // 4)
    
    # 효율성 기준 정렬 (score/token 비율)
    sorted_chunks = sorted(
        chunks, 
        key=lambda x: x.get(score_key, 0) / x["token_count"], 
        reverse=True
    )
    
    # 그리디 패킹
    packed_chunks = []
    used_tokens = 0
    
    for chunk in sorted_chunks:
        if used_tokens + chunk["token_count"] <= budget:
            packed_chunks.append(chunk)
            used_tokens += chunk["token_count"]
    
    # 상세 통계 계산
    total_selected_tokens = sum(chunk["token_count"] for chunk in chunks)
    
    stats = {
        "selected_count": len(chunks),
        "packed_count": len(packed_chunks),
        "selected_tokens": total_selected_tokens,
        "packed_tokens": used_tokens,
        "compression_ratio": len(packed_chunks) / len(chunks) if chunks else 0.0,
        "token_savings": total_selected_tokens - used_tokens,
        "efficiency": used_tokens / budget if budget > 0 else 0.0
    }
    
    # 📊 로깅 추가 (기존 코드에 없던 통계 가시성)
    logging.info(f"Packing completed: {stats['packed_count']}/{stats['selected_count']} chunks, "
                f"tokens: {stats['packed_tokens']}/{stats['selected_tokens']} "
                f"(efficiency: {stats['efficiency']:.1%})")
    
    return packed_chunks, stats
