🧪 Example Flow:
📱 User uploads image via mobile app

🛰 Backend sends metadata + image path to Kafka

🧠 ML service consumes it, processes image

💬 Generates Med-GEMMA prompt, sends to vLLM

📄 vLLM returns full report, saved to DB

📤 Backend returns report to frontend

### workflow
```text
[User / Mobile App]
       |
       | 1. Upload Image + Metadata (user_id, etc)
       v
 ┌──────────────────────────┐
 |      FastAPI Backend     |
 | - Receives image upload  |
 | - Generates task_id      |
 | - Sends to Kafka         |
 └──────────────────────────┘
       |
       | 2. Produce message to Kafka
       v
 ┌──────────────────────────┐
 |         Kafka            |
 | - Topic: skin_analysis   |
 └──────────────────────────┘
       |
       | 3. Consume from topic
       v
 ┌───────────────────────────────────────────────┐
 |               ML Service (Consumer)           |
 | ┌───────────────────────────────────────────┐ |
 | |           Pipeline Handler               | |
 | | - Loads image from path or bytes         | |
 | | - Calls Preprocessor                     | |
 | | - Extracts features                      | |
 | | - Builds prompt (Med-GEMMA format)       | |
 | | - Sends to vLLM                          | |
 | | - Receives completion                    | |
 | | - Formats structured report              | |
 | | - Stores result in DB                    | |
 | └───────────────────────────────────────────┘ |
 └───────────────────────────────────────────────┘
       |
       | 4. Store Result to DB
       v
 ┌─────────────────────────────┐
 |     PostgreSQL / SQLite     |
 | - User info                 |
 | - Analysis result           |
 | - Report JSON/Text          |
 └─────────────────────────────┘
       |
       | 5. Notify Backend / Poll Result
       v
 ┌──────────────────────────┐
 |      FastAPI Backend     |
 | - Provides report API    |
 | - Returns result to user |
 └──────────────────────────┘
       |
       | 6. View Report / Routine
       v
[User / Mobile App]
```

🧠 Breakdown of ML Modules

```text
ML Service:
├── kafka/
│   ├── consumer.py        # Consumes image analysis jobs
│   └── producer.py        # Sends results back if needed
├── pipeline/
│   └── handle_analysis.py # Full pipeline coordinator
├── image_processing/
│   └── cv_utils.py        # Image resize, denoise, etc.
├── preprocessors/
│   └── skin_feature_extractor.py
├── models/
│   ├── skin_analysis_model.py  # Prompt generator (Med-GEMMA format)
│   └── custom_vllm_pipeline.py # Communicate with vLLM
├── postprocessors/
│   └── report_formatter.py     # Convert vLLM output to JSON/Report
├── models/entities.py          # SQLAlchemy DB models
├── models/database.py          # DB connection

✅ Backend Workflow (FastAPI API Layer)

[Mobile App / Frontend]
       |
       | 1. Upload image + user_id (auth)
       v
 ┌──────────────────────────────────────────┐

 |         FastAPI Backend (API)            |
 |------------------------------------------|
 | Routers:                                 |
 |   - POST /analyze-skin                   |
 |   - GET /report/{task_id}                |
 |                                          |
 | Services:                                |
 |   - user_service.py                      |
 |   - skincare_service.py                  |
 |                                          |
 | Dependencies:                            |
 |   - auth (JWT / OAuth2)                  |
 |   - DB session (SQLAlchemy)              |
 └──────────────────────────────────────────┘

       |
       | 2. Store image temporarily
       |    Generate task_id
       v
 ┌───────────────────────────┐
 |     File Storage (Disk)   |
 |     or S3 Bucket (Cloud)  |
 └───────────────────────────┘
       |
       | 3. Send Kafka message
       v
 ┌─────────────────────────────┐
 | Kafka Producer               |
 | - Topic: skin_analysis      |
 | - Message: task_id, image   |
 |   path, user_id, timestamp  |
 └─────────────────────────────┘
       |
       | 4. Return response to client
       v
 ┌────────────────────────────────┐
 |  Response: { task_id, status } |
 └────────────────────────────────┘

```

🧩 Backend Folder Breakdown

```text
backend/
├── app/
│   ├── main.py                  # Start FastAPI
│   ├── routers/
│   │   ├── skincare.py          # /analyze-skin, /report/{id}
│   │   └── auth.py              # login, register
│   ├── services/
│   │   ├── skincare_service.py  # Kafka produce, task tracking
│   │   └── user_service.py
│   ├── models/
│   │   ├── user.py              # Pydantic schemas
│   │   └── skincare_result.py
│   ├── core/
│   │   ├── config.py            # env, Kafka, DB configs
│   │   └── database.py          # SQLAlchemy session
│   ├── kafka/
│   │   └── producer.py          # Async Kafka producer
│   └── dependencies.py          # JWT, DB injectors

```

🔁 Typical API Interaction Flow
Frontend calls POST /analyze-skin with image + user_id

Backend:

Authenticates user

Saves image (temporarily or cloud)

Produces Kafka message

Returns task_id to client

ML Service processes image

Once done, FastAPI Backend exposes result via GET /report/{task_id}
