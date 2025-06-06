FROM python:3.12-slim
WORKDIR /app
COPY hourlydata.py .
RUN pip install requests boto3
CMD ["python","hourlydata.py"]
