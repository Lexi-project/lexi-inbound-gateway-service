FROM python:3.11

WORKDIR /app

COPY . /app

RUN make install

EXPOSE 8001

CMD ["make", "start"]