# FROM：基底映像檔
FROM python:alpine3.10

RUN apk add --no-cache bash
RUN apk update && apk add gcc libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev 
# 安裝 chrone  # 安裝 chrone-driver
RUN apk add wget && apk add unzip
RUN bin/bash -c 'wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/115.0.5790.170/linux64/chrome-linux64.zip'
RUN bin/bash -c 'unzip chrome-linux64.zip'
RUN bin/bash -c 'wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/115.0.5790.170/linux64/chromedriver-linux64.zip'
RUN bin/bash -c 'unzip chromedriver-linux64.zip'
RUN bin/bash -c 'pwd'
RUN bin/bash -c 'mv ./chromedriver-linux64/chromedrive -d ./website/chromedriver/'
#tk-dev
RUN /usr/local/bin/python -m pip install --upgrade pip

EXPOSE 5000

RUN adduser -D admin
USER admin
WORKDIR /home/admin

# ADD：將檔案加到 images 內
ADD . /admin


# 只有build 時使用，會執行此命令
COPY --chown=admin:admin requirements.txt /home/admin
ENV PATH="/home/admin/.local/bin:${PATH}"

RUN pip3 install --user --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org --no-cache-dir -r requirements.txt



# run container 時要執行的命令 COPY . /home/app
COPY --chown=admin:admin . /home/admin

CMD python3 ./main.py