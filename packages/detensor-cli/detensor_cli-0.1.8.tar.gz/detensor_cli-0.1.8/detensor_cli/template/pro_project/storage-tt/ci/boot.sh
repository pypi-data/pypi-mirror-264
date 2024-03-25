#! /usr/bin/env bash

set -x

cp ../storage .

cd ..

mysql --user=root --password=$MYSQL_ROOT_PASSWORD --host=127.0.0.1 mysql < testdata/mysql/init/init.sql

if [ $? -ne 0 ]; then
  echo "init mysql failed"
  exit
fi

cd ci

STORAGE_CONFIG_PATH=./config/config1.yaml \
  ./storage </dev/null >../logs/storage.1.log 2>&1 &
PID=$!
echo "PID: $PID"
echo $PID >> ./pids

STORAGE_CONFIG_PATH=./config/config2.yaml \
  ./storage </dev/null >../logs/storage.2.log 2>&1 &
PID=$!
echo "PID: $PID"
echo $PID >> ./pids

STORAGE_CONFIG_PATH=./config/config3.yaml \
  ./storage </dev/null >../logs/storage.3.log 2>&1 &
PID=$!
echo "PID: $PID"
echo $PID >> ./pids

STORAGE_CONFIG_PATH=./config/config4.yaml \
  ./storage </dev/null >../logs/storage.4.log 2>&1 &
PID=$!
echo "PID: $PID"
echo $PID >> ./pids

sleep 3

echo "start test"

cd ..
./backend-test -test.v
OUT=$?

cd ci
./stop.sh

exit $OUT