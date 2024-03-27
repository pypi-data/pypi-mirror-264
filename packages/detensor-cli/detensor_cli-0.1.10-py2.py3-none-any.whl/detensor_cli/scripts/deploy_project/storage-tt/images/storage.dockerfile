FROM golang:1.18.3 as builder

ENV GOPROXY=https://goproxy.cn,direct
RUN go install github.com/swaggo/swag/cmd/swag@latest

COPY . /usr/src
WORKDIR /usr/src

RUN make build-backend

FROM ubuntu:22.04

COPY --from=builder /usr/src/storage /storage/storage
COPY ./hbc /hbc

WORKDIR /storage

CMD "./storage"
