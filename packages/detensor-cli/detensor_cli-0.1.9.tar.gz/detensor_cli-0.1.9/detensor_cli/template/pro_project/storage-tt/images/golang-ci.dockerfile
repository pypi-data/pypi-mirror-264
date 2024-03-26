FROM golang:1.18.3

ENV GOPROXY=https://goproxy.cn,direct
RUN go install github.com/swaggo/swag/cmd/swag@latest
