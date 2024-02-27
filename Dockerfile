FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONPATH="/app:${PYTHONPATH}"
EXPOSE 8000
CMD ["uvicorn", "app.main:application", "--host", "0.0.0.0"]
