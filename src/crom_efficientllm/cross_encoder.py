from typing import List, Optional
import logging

class SafeCrossEncoderManager:
    """Cross-Encoder 상태를 명시적으로 관리하는 클래스"""
    
    def __init__(self, model_name: Optional[str] = None, device: str = "cpu"):
        self.model_name = model_name
        self.device = device
        self.model = None
        self.status = "unknown"
        self.last_error = None
        
        self._initialize()
    
    def _initialize(self):
        """Cross-Encoder 초기화 with 상세 상태 추적"""
        if not self.model_name:
            self.status = "disabled"
            logging.info("Cross-Encoder: DISABLED (no model specified)")
            return
        
        try:
            # sentence-transformers 임포트 체크
            from sentence_transformers import CrossEncoder
            
            # 모델 로딩 시도
            self.model = CrossEncoder(self.model_name, device=self.device)
            self.status = f"active ({self.model_name})"
            
            # 🆕 성공 시 상세 로깅
            logging.info(f"Cross-Encoder: ACTIVE")
            logging.info(f"  └─ Model: {self.model_name}")
            logging.info(f"  └─ Device: {self.device}")
            
        except ImportError as e:
            self.status = "unavailable (sentence-transformers not installed)"
            self.last_error = str(e)
            
            # 🆕 의존성 누락 시 명확한 안내
            logging.warning("Cross-Encoder: UNAVAILABLE")
            logging.warning("  └─ Reason: sentence-transformers not installed")
            logging.warning("  └─ Install: pip install sentence-transformers")
            
        except Exception as e:
            self.status = f"error ({type(e).__name__})"
            self.last_error = str(e)
            
            # 🆕 기타 오류 시 상세 로깅
            logging.error(f"Cross-Encoder: ERROR")
            logging.error(f"  └─ Model: {self.model_name}")
            logging.error(f"  └─ Error: {str(e)}")
    
    def get_status_for_response(self) -> str:
        """API 응답용 상태 문자열"""
        return self.status
    
    def rerank(self, query: str, documents: List[str]) -> List[float]:
        """안전한 리랭킹 with 상태 로깅"""
        if self.model is None:
            # 🆕 비활성화 상태 명시적 로깅
            logging.debug(f"Cross-Encoder rerank skipped: {self.status}")
            return [0.5] * len(documents)  # 중립 점수
        
        try:
            pairs = [(query, doc) for doc in documents]
            scores = self.model.predict(pairs)
            
            # 🆕 성공적 리랭킹 로깅
            logging.debug(f"Cross-Encoder reranked {len(documents)} documents")
            
            return scores.tolist() if hasattr(scores, 'tolist') else list(scores)
            
        except Exception as e:
            # 🆕 런타임 오류 시 상세 로깅
            logging.error(f"Cross-Encoder rerank failed: {str(e)}")
            logging.error(f"  └─ Fallback: returning neutral scores")
            return [0.5] * len(documents)
