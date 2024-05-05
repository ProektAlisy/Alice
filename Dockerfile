FROM python:3.12-slim
WORKDIR /alice_app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONPATH="/alice_app:${PYTHONPATH}"
EXPOSE 8000
CMD ["uvicorn", "app.main:application", "--host", "0.0.0.0"]
#CMD ["gunicorn", "app.main:application", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]
