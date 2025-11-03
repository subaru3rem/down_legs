FROM python:3.11.9-slim-bullseye
WORKDIR /app

# We need wget to set up the PPA and xvfb to have a virtual screen and unzip to install the Chromedriver
RUN apt-get update && apt-get install -y wget xvfb unzip gnupg2 unixodbc-dev curl unzip libglib2.0-0 libnss3 libdbus-1-3 \
	libatk1.0-0 libatk-bridge2.0-0 libcups2 libxcomposite1 libxrandr2 libgbm-dev libxkbcommon-x11-0 libpango1.0-0 \
	libasound2

# Set up the Chrome PPA
RUN wget https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.86/linux64/chrome-linux64.zip \
	&& mkdir -p /opt/google/chrome \
	&& unzip chrome-linux64.zip "chrome-linux64/*" -d /opt/google/chrome \
	&& mv /opt/google/chrome/chrome-linux64/* /opt/google/chrome

# Set up Chromedriver Environment variables
ENV CHROMEDRIVER_VERSION=2.19
ENV CHROMEDRIVER_DIR=/opt/google/chrome
# /opt/google/chrome

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-u", "main.py"] 

