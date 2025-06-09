FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

RUN apt update && apt install -y python3 python3-pip git
RUN pip install vllm

# مدل Med-GEMMA
RUN mkdir /app
WORKDIR /app

CMD ["python3", "main.py"]