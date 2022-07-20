FROM python:3.8-buster

RUN mkdir /telegram_bot

ADD . /telegram_bot

WORKDIR /telegram_bot

RUN pip install numpy spacy
RUN python -m spacy download ru_core_news_lg
RUN pip install -r requirements.txt

CMD ["python", "bot.py"]