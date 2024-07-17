FROM python:3.9-slim

WORKDIR /project

RUN apt-get update && apt-get install -y wget gnupg
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get install -y google-chrome-stable
RUN apt-get clean

COPY requirements.txt .
RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY . .

ENV PYTHONPATH=/project

CMD ["python", "main.py"]
