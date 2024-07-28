FROM python:3.9-slim

WORKDIR /project

# Download the specific version of Google Chrome .deb file (64-bit)
RUN apt-get update && apt-get install -y wget gnupg
RUN wget -q https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_126.0.6478.182-1_amd64.deb -O /tmp/google-chrome-stable.deb

# Install the .deb file
RUN apt-get update && apt-get install -y /tmp/google-chrome-stable.deb && rm /tmp/google-chrome-stable.deb

RUN apt-get clean

COPY requirements.txt .
RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN apt-get update
RUN apt-get install -y espeak-ng

COPY . .

ENV PYTHONPATH=/project

CMD ["python", "main.py"]

#FROM python:3.9-slim

#WORKDIR /project

#RUN apt-get update && apt-get install -y wget gnupg
#RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
#RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

#ENV CHROME_VERSION 126.0.6478.182-1

#RUN wget -q https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_114.0.5735.198-1_amd64.deb -O /tmp/google-chrome-stable.deb

#RUN apt-get update && apt-get install -y google-chrome-stable=${CHROME_VERSION}
#RUN apt-get clean

#COPY requirements.txt .
#RUN pip install --trusted-host pypi.python.org -r requirements.txt

#RUN apt-get update
#RUN apt-get install -y espeak-ng

#COPY . .

#ENV PYTHONPATH=/project

#CMD ["python", "main.py"]
