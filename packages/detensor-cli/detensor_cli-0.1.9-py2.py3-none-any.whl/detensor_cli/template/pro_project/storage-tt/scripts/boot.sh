#! /usr/bin/env bash

set -e

mysql --user=root --password=123456 --host=127.0.0.1 mysql < testdata/mysql/init/init.sql

STORAGE_CONFIG_PATH=./testdata/config1.yaml \
  nohup ./storage >logs/storage.1.log &
PID=$!
echo "PID: $PID"
echo $PID >> ./pids

STORAGE_CONFIG_PATH=./testdata/config2.yaml \
  nohup ./storage >logs/storage.2.log &
PID=$!
echo "PID: $PID"
echo $PID >> ./pids

STORAGE_CONFIG_PATH=./testdata/config3.yaml \
  nohup ./storage >logs/storage.3.log &
PID=$!
echo "PID: $PID"
echo $PID >> ./pids

STORAGE_CONFIG_PATH=./testdata/config4.yaml \
  nohup ./storage >logs/storage.4.log &
PID=$!
echo "PID: $PID"
echo $PID >> ./pids