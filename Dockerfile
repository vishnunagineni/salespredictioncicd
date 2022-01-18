FROM python:alpine
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app
CMD ["python","app.py"]