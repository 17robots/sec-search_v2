FROM python:3

ENV USERPROFILE /usr/src/user/

run mkdir -p $USERPROFILE.aws

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN mkdir output
