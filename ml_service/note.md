 مرحله 1: نصب vLLM و اجرای مدل Med-GEMMA
✅ Dockerfile (داخل ml_service/)


✅ مرحله 2: اجرای vLLM روی Med-GEMMA


python3 -m vllm.entrypoints.openai.api_server \
  --model google/med-gemma-7b-it \
  --dtype float16 \
  --gpu-memory-utilization 0.85 \
  --served-model-name med-gemma
