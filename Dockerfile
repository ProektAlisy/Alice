FROM python:3.12-slim
WORKDIR /
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONPATH="/:${PYTHONPATH}"
EXPOSE 8000
CMD ["uvicorn", "app.main:application", "--host", "0.0.0.0"]
