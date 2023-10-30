FROM python:3.11.5-bookworm
RUN rm -rf /etc/apt/sources.list.d/*
RUN echo "deb http://mirrors.aliyun.com/debian/ bookworm main non-free contrib" > /etc/apt/sources.list
RUN apt update
# debian11 以及下
# RUN apt install -y vim netcat telnet less
# debian12 的  netcat 变成 netcat-openbsd 了，详见: https://unix.stackexchange.com/questions/749306/discrepancies-in-netcat-installation-process-between-debian-bullseye-vs-debian-b
RUN apt install -y vim netcat-openbsd telnet less
RUN apt install -y sysstat htop
RUN apt install -y ncdu
RUN /usr/local/bin/python -m pip install --upgrade pip -i https://mirror.baidu.com/pypi/simple

RUN mkdir /code
WORKDIR /code

COPY requirements-dev.txt /code/
RUN pip install -r requirements-dev.txt -i https://mirror.baidu.com/pypi/simple

COPY requirements-prd.txt /code/
RUN pip install -r requirements-prd.txt -i https://mirror.baidu.com/pypi/simple


RUN mkdir -p /code/models
RUN wget -P /code/models http://cmp.felk.cvut.cz/cnnimageretrieval/data/networks/gl18/gl18-tl-resnet50-gem-w-83fdc30.pth

ADD . /code/