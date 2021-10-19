FROM debian:buster

WORKDIR /usr/src/app
# set environment variables
# python이 pyc파일을 디스크에 쓰는 것을 방지.
ENV PYTHONDONTWRITEBYTECODE 1
# python이 stdout, stderr를 버퍼링하는 것을 방지.
ENV PYTHONUNBUFFERED 1
# install python3.9.6 dependencies
RUN apt-get update \
	&& apt-get install -y build-essential \
		zlib1g-dev \
		libncurses5-dev \
		libgdbm-dev \
		libnss3-dev \
		libssl-dev \
		libsqlite3-dev \
		libreadline-dev \
		libffi-dev \
		curl \
		libbz2-dev \
		wget \
# download python3.9.6
	&& wget https://www.python.org/ftp/python/3.9.6/Python-3.9.6.tgz \
	&& tar -xf Python-3.9.6.tgz \
	&& ./Python-3.9.6/configure --enable-optimizations \
	&& make -j 2 \
	&& make altinstall \
# install psycopg2 dependencies
	&& apt-get install -y postgresql \
	gcc \
	python3-dev \
	python3-pip \
	musl-dev \
# install dependencies
	&& pip3 install --upgrade pip
COPY requirement.txt .
RUN pip3 install -r requirement.txt
# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh \
	&& chmod +x /usr/src/app/entrypoint.sh

# copy project
COPY . .
# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"] 
