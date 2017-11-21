FROM python:3
LABEL maintainer = "Corey Watson"

ENV PYTHONPATH=/modules
WORKDIR /modules/app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app .
EXPOSE 80
ENTRYPOINT ["python", "server_rough.py"]
