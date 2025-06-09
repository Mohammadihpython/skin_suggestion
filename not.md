├── README.md
├── .gitignore
├── docs/
│   ├── api_documentation.md
│   ├── database_schema.md
│   └── architecture_diagrams.md
├── mobile_app/ (Frontend - e.g., React Native, Flutter, Swift/Kotlin)
│   ├── src/
│   ├── assets/
│   ├── components/
│   ├── screens/
│   ├── navigation/
│   └── package.json
├── backend/ (FastAPI)
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/ (API Endpoints)
│   │   │   ├── skincare.py
│   │   │   └── auth.py
│   │   ├── services/ (Business Logic)
│   │   │   ├── user_service.py
│   │   │   └── image_analysis_service.py
│   │   ├── models/ (Pydantic Models for Request/Response)
│   │   │   ├── user.py
│   │   │   └── skincare_result.py
│   │   ├── core/ (Configuration, Database Connections)
│   │   │   ├── config.py
│   │   │   └── database.py
│   │   └── dependencies.py (Dependency Injection)
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── ml_service/ (Machine Learning - vLLM, Med-GEMMA)
│   ├── app/
│   │   ├── main.py (FastAPI or similar for ML inference endpoint)
│   │   ├── models/ (Pre-trained Med-GEMMA models, vLLM setup)
│   │   │   ├── skin_analysis_model.py
│   │   │   └── custom_vllm_pipeline.py
│   │   ├── preprocessors/
│   │   └── postprocessors/
│   ├── training/ (Scripts for model training and fine-tuning)
│   ├── data/ (Dataset management)
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── devops/
│   ├── kubernetes/ (Deployment files, e.g., for GKE or AWS EKS)
│   ├── terraform/ (Infrastructure as Code)
│   └── scripts/ (Deployment, CI/CD scripts)
└── docker-compose.yml (for local development setup)