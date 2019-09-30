FROM python:3.7
RUN pip install --upgrade pip
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install psycopg2
RUN apt-get update \
    && apt-get -y install \
    libpq-dev \
    python-dev \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/doc/*
# ARG user=developer
ARG requirements=./requirements.txt
# ENV USERPATH /home/$user
RUN echo "root:Docker!" | chpasswd
# RUN useradd -m $user || echo "User alredy exists!"
COPY $requirements .
RUN pip install -r $requirements && rm $requirements
WORKDIR /webapi
VOLUME /webapi
EXPOSE 8000