FROM python:alpine
WORKDIR /usr/src/app
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/
RUN pip install -r requirements.txt
COPY . /usr/src/app
CMD ["python","app.py"]