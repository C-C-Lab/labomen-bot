FROM python:3
USER root
LABEL Name "labomen-bot"
LABEL Version "prod"

WORKDIR /usr/local/labomen-bot

RUN apt-get update && \
    apt-get -y install locales locales-all && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8 && \
    echo "ja_JP UTF-8" > /etc/locale.gen && \
    pip3 install --upgrade pip && \
    pip3 install --upgrade setuptools && \
    pip3 install -r requirements.txt

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

CMD ["python3", "-m", "labomen_bot"]
