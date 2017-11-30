FROM python:3
LABEL maintainer = "Corey Watson"

ENV PYTHONPATH=/modules
WORKDIR /modules/app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install -U flask-cors
COPY app .
EXPOSE 80
ENTRYPOINT ["python", "Server.py"]
