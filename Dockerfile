FROM python:3.8-slim-buster
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
RUN jupyter nbconvert --to python /app/MLPipeline.ipynb
RUN python /app/MLPipeline.py
CMD ["python","app.py"]