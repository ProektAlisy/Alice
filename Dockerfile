FROM python:3.12
COPY . ./
RUN pip install -r /requirements.txt
WORKDIR /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]