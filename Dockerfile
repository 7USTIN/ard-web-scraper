FROM debian:latest

RUN apt update && apt upgrade -y

RUN apt install python3 python3-pip wget unzip chromium -y && \
    pip install selenium webdriver-manager
    
RUN mkdir -p /app/data && cd /app && \
    wget https://chromedriver.storage.googleapis.com/107.0.5304.62/chromedriver_linux64.zip -O chromedriver.zip && \
    unzip chromedriver.zip

WORKDIR /app

COPY scraper.py .

CMD ["python3", "scraper.py"]