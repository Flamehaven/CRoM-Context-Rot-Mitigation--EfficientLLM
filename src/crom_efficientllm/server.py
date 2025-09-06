from fastapi import FastAPI, HTTPException
import time
from typing import List, Dict
import logging

# 내부 모듈 임포트
from .budget_packer import enhanced_greedy_pack
from .cross_encoder import SafeCrossEncoderManager
from .capsule_logger import ExplainCapsuleLogger

# --- FastAPI 앱 및 주요 컴포넌트 초기화 ---

app = FastAPI(
    title="CRoM-EfficientLLM Server",
    description="Context Reranking and Management for Efficient LLMs",
    version="1.0.1"
)

logging.basicConfig(level=logging.INFO)

# 컴포넌트 인스턴스화
# TODO: 설정 파일(config.yaml)에서 모델 이름 등을 로드하도록 개선 필요
ce_manager = SafeCrossEncoderManager(model_name="ms-marco-TinyBERT-L-2-v2")
capsule_logger = ExplainCapsuleLogger(log_directory="artifacts/logs")


# --- 응답 스키마 및 헬퍼 함수 ---

class ProcessResponseV2:
    """확장된 /process 엔드포인트 응답 스키마 헬퍼"""
    
    @staticmethod
    def create_response(query: str, packed_chunks: List[Dict], 
                       processing_stats: Dict, cross_encoder_status: str, 
                       processing_time: float) -> Dict:
        """개선된 응답 생성"""
        
        response = {
            "success": True,
            "query": query,
            "chunks": packed_chunks,
            "stats": processing_stats, # packing 통계
            "meta": {
                "cross_encoder_status": cross_encoder_status,
                "processing_time_ms": processing_time * 1000,
                "timestamp": time.time()
            }
        }
        return response

# --- API 엔드포인트 정의 ---

@app.post("/process", summary="Rerank and pack text chunks")
def process_chunks(query: str, chunks: List[Dict], budget: int = 4096):
    """
    주어진 쿼리와 청크 목록을 리랭킹하고 예산에 맞게 패킹합니다.
    """
    start_time = time.time()

    try:
        # 1. Cross-Encoder로 리랭킹 (활성화 시)
        doc_texts = [chunk.get("text", "") for chunk in chunks]
        scores = ce_manager.rerank(query, doc_texts)
        for chunk, score in zip(chunks, scores):
            chunk["score"] = score

        # 2. 예산에 맞게 패킹
        packed_chunks, stats = enhanced_greedy_pack(chunks, budget=budget, score_key="score")

        # 3. 최종 응답 생성
        processing_time = time.time() - start_time
        response_data = ProcessResponseV2.create_response(
            query=query,
            packed_chunks=packed_chunks,
            processing_stats=stats,
            cross_encoder_status=ce_manager.get_status_for_response(),
            processing_time=processing_time
        )

        # 4. 설명 캡슐 로깅
        capsule = capsule_logger.create_explain_capsule(
            query=query,
            response_data=response_data,
            processing_stats=stats,
            cross_encoder_status=ce_manager.get_status_for_response()
        )
        capsule_logger.log_capsule(capsule)

        return response_data

    except Exception as e:
        logging.error(f"Error during /process: {e}", exc_info=True)
        # 오류 로깅
        capsule_logger.log_error({
            "endpoint": "/process",
            "error": str(e),
            "query": query,
        })
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

@app.get("/healthz", summary="Health check")
def health_check():
    """서버의 상태를 확인합니다."""
    return {"status": "ok", "cross_encoder": ce_manager.get_status_for_response()}

@app.get("/metrics", summary="Get Prometheus metrics")
def get_metrics():
    """Prometheus 메트릭을 노출합니다."""
    # TODO: Prometheus-client를 사용하여 실제 메트릭을 구현해야 함
    return {"message": "Metrics endpoint is active. Implement with prometheus-client."}
