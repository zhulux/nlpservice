FROM python:3.6

RUN mkdir -p /root/.pip && echo "[global]\nindex-url = https://mirrors.ustc.edu.cn/pypi/web/simple" > /root/.pip/pip.conf

RUN mkdir /app
WORKDIR /app

EXPOSE 8080

CMD python -u service.py

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY . /app

