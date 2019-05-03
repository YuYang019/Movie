FROM python:3

WORKDIR /usr/src/pyapp

COPY requirements.txt ./

# surprise的bug，需要先下载numpy
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple numpy

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple  --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "app:app", "-c", "./gunicorn.conf.py"]