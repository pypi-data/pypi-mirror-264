FROM python:3.11

WORKDIR /code
COPY requirements.txt /code/requirements.txt
RUN pip3 install -r requirements.txt

ENV NLTK_DATA /data/nltk_data
RUN python3 -m nltk.downloader punkt stopwords -d /data/nltk_data

COPY komodo /code/komodo/
COPY sample /code/sample/
