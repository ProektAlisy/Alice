FROM python:3.12-slim
WORKDIR ./app
COPY requirements.txt .
RUN pip3 install -r ./requirements.txt --no-cache-dir
COPY ./app .
#ENV PYTHONPATH "${PYTHONPATH}:/app"
EXPOSE 8000
CMD ["uvicorn", "app.main:application", "--host", "0.0.0.0"]
