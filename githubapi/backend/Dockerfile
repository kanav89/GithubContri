# Dockerfile -> image -> container
FROM python:3.10-alpine
# check out python docker for more specifications

WORKDIR /githubdocker


# ADD main.py .
COPY main.py .


# RUN pip install -r requirements.txt
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000
ENV FLASK_APP=main.py
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"] 