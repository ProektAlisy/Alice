FROM python:3.12
WORKDIR /app
COPY . .
RUN pip install -r /requirements.txt
COPY app/ .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]