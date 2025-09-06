import json
from pathlib import Path
from datetime import datetime
from typing import Union, Dict
import logging

class ExplainCapsuleLogger:
    """스키마 기반 설명 캡슐 저장 시스템"""
    
    def __init__(self, log_directory: str = "artifacts/logs"):
        self.log_dir = Path(log_directory)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # 로그 파일 경로들
        self.capsules_file = self.log_dir / "explain_capsules.jsonl"
        self.metrics_file = self.log_dir / "processing_metrics.jsonl"
        self.errors_file = self.log_dir / "error_log.jsonl"
        
        logging.info(f"ExplainCapsule Logger initialized: {self.log_dir}")
    
    def create_explain_capsule(self, query: str, response_data: Dict, 
                              processing_stats: Dict, 
                              cross_encoder_status: str) -> Dict:
        """스키마 준수 설명 캡슐 생성"""
        
        capsule = {
            # 🔖 메타데이터 (필수)
            "timestamp": datetime.now().isoformat(),
            "version": "1.0",
            "processor": "CRoM-Enhanced",
            
            # 📝 쿼리 정보
            "query": {
                "text": query,
                "length": len(query),
                "token_estimate": len(query) // 4
            },
            
            # 📊 처리 통계 (패치 1에서 확장된 정보)
            "processing_stats": {
                **processing_stats,
                "cross_encoder_status": cross_encoder_status
            },
            
            # 🔧 시스템 상태
            "system_state": {
                "cross_encoder_available": cross_encoder_status not in ["disabled", "unavailable"]
            },

            # 📦 원본 및 결과 청크
            "chunks": {
                "packed": response_data.get("chunks", [])
            }
        }
        return capsule

    def log_capsule(self, capsule: Dict):
        """설명 캡슐을 .jsonl 파일에 기록"""
        try:
            with open(self.capsules_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(capsule, ensure_ascii=False) + "\n")
        except Exception as e:
            logging.error(f"Failed to log explain capsule: {e}")

    def log_error(self, error_details: Dict):
        """오류 정보를 .jsonl 파일에 기록"""
        try:
            error_details["timestamp"] = datetime.now().isoformat()
            with open(self.errors_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(error_details, ensure_ascii=False) + "\n")
        except Exception as e:
            logging.error(f"Failed to log error: {e}")
