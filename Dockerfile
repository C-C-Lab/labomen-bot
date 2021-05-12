FROM python:3
USER root

RUN apt-get update && \
    apt-get -y install locales locales-all && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

COPY . /app/labomen-bot
WORKDIR /app/labomen-bot
RUN pip3 install --upgrade pip && \
    pip3 install --upgrade setuptools && \
    pip3 install -r requirements.txt

CMD python3 -m labomen_bot
