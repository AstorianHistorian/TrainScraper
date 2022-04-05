FROM python:3.10-alpine
LABEL Author="Dmitry Mutik"

ENV PYTHONUNBUFFERED 1

RUN pip install --no-cache wheel

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D AsHisUser465345643
USER AsHisUser465345643

CMD ["python", "./app/TuTu scraper.py"]
