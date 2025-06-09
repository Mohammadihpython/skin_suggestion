# Full pipeline: image preprocess -> med-gemma prompt -> vLLM -> store + return

from app.image_processing.cv_utils import preprocess_image
from app.preprocessors.skin_feature_extractor import extract_features
from app.vllm_client import get_vllm_response
from app.postprocessors.report_formatter import format_report
from app.models.database import get_db
from app.models.entities import AnalysisResult
│   │
def run_analysis(image_path: str, user_id: int, db_session):
│   │       # Step 1: Preprocess image (e.g., crop, enhance)
│   │       face_data = preprocess_image(image_path)
│   │
│   │       # Step 2: Extract structured features
│   │       features = extract_features(face_data)
│   │
│   │       # Step 3: Build prompt and get response
│   │       vllm_result = get_vllm_response(features)
│   │
│   │       # Step 4: Postprocess to structured report
│   │       report = format_report(vllm_result)
│   │
│   │       # Step 5: Store in DB
│   │       analysis = AnalysisResult(user_id=user_id, result=report)
│   │       db_session.add(analysis)
│   │       db_session.commit()
│   │
│   │       return report