FROM python:3.8.5
WORKDIR /code
RUN mkdir /code/staticfiles
COPY requirements.txt /code
RUN pip install -r /code/requirements.txt
COPY . /code
RUN python ./foodgram-project/the_end/manage.py collectstatic --noinput