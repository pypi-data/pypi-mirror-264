
.PHONY: build-contract invoke-save invoke-load get-load whoami

CONTRACT_COUNT=5


#!/bin/bash

# MySQL 数据库登录信息
MYSQL_USER="root"
MYSQL_PASSWORD="123456"
MYSQL_HOST="localhost"
DB_NAME1="storage1"
DB_NAME2="storage2"
DB_NAME3="storage3"
DB_NAME4="storage4"



# build 智能合约
build-contract:
	cd contract_rust && cargo build --features test --release --target=wasm32-unknown-unknown --lib
	cp contract_rust/target/wasm32-unknown-unknown/release/*.wasm ./contract.wasm

build-prod-contract:
	cd contract_rust && cargo build --release --target=wasm32-unknown-unknown --lib
	cp contract_rust/target/wasm32-unknown-unknown/release/*.wasm ./contract.wasm

# build 后端可执行文件
build-backend:
	# swag init --output swagger --outputTypes json,yaml
	go build -o storage -tags debug  main.go

build-prod-backend:
	swag init --output swagger --outputTypes json,yaml
	go build -o storage main.go

# build 后端测试可执行文件
build-backend-test:
	go test -c ./test -tags debug -o backend-test


# 使用cmc命令行工具, 将合约上链
create-contract: build-contract
	./cmc client contract user create \
		--contract-name=example    \
		--runtime-type=WASMER         \
		--byte-code-path=./contract.wasm \
		--version=1.0                 \
		--sdk-conf-path=./sdk_config.yml \
		--admin-key-file-paths=./testdata/crypto-config/wx-org1.chainmaker.org/user/admin1/admin1.tls.key,./testdata/crypto-config/wx-org2.chainmaker.org/user/admin1/admin1.tls.key,./testdata/crypto-config/wx-org3.chainmaker.org/user/admin1/admin1.tls.key \
		--admin-crt-file-paths=./testdata/crypto-config/wx-org1.chainmaker.org/user/admin1/admin1.tls.crt,./testdata/crypto-config/wx-org2.chainmaker.org/user/admin1/admin1.tls.crt,./testdata/crypto-config/wx-org3.chainmaker.org/user/admin1/admin1.tls.crt \
		--sync-result=true \
		--params='{}'


# 使用cmc命令行工具, 调用合约的save方法
invoke-save:
	./cmc client contract user invoke \
		--contract-name=example    \
		--method=save         \
		--sdk-conf-path=./sdk_config.yml \
		--sync-result=true \
		--params='{"key":"hello","value":"world"}'

# 使用cmc命令行工具, 调用合约的load方法
invoke-load:
	./cmc client contract user invoke \
		--contract-name=example    \
		--method=load         \
		--sdk-conf-path=./sdk_config.yml \
		--sync-result=true \
		--params='{"key":"hello"}'

whoami:
	./cmc client contract user invoke \
		--contract-name=example    \
		--method=whoami         \
		--sdk-conf-path=./sdk_config.yml \
		--sync-result=true \
		--params='{}'

# 使用cmc命令行工具, 查询合约的load方法
get-load:
	./cmc client contract user get \
		--contract-name=example    \
		--method=load         \
		--sdk-conf-path=./sdk_config.yml \
		--params='{"key":"hello"}'

.PHONY: chain-up chain-down
# 启动测试用的长安链
chain-up:
	cd testdata && docker-compose -f four-nodes.docker-compose.yml up -d

# 停止测试用的长安链
chain-down:
	cd testdata && docker-compose -f four-nodes.docker-compose.yml down

.PHONY: update-schema
update-schema:
	cd contract_rust && cargo run -q --bin schemar >../schema.json

.PHONY: clean-all boot-all
# 清理所有制品
clean-all: 
	- ./scripts/stop.sh
	# - cd testdata && docker-compose -f four-nodes.docker-compose.yml down
	- rm ./contract.wasm
	- rm ./chainmodel
	- rm ./storage
	- mysql -u${MYSQL_USER} -p${MYSQL_PASSWORD} -h ${MYSQL_HOST} -e "DROP DATABASE IF EXISTS ${DB_NAME1};"
	- mysql -u${MYSQL_USER} -p${MYSQL_PASSWORD} -h ${MYSQL_HOST} -e "DROP DATABASE IF EXISTS ${DB_NAME2};"
	- mysql -u${MYSQL_USER} -p${MYSQL_PASSWORD} -h ${MYSQL_HOST} -e "DROP DATABASE IF EXISTS ${DB_NAME3};"
	- mysql -u${MYSQL_USER} -p${MYSQL_PASSWORD} -h ${MYSQL_HOST} -e "DROP DATABASE IF EXISTS ${DB_NAME4};"


.PHONY: contract-test
# 执行合约的单元测试
contract-test:
	./scripts/test.sh

prepare:
	rm -rf testdata/crypto-config
	cp ../chainmaker-go/tools/cmc/cmc .
	cp -r ../chainmaker-go/build/crypto-config testdata/crypto-config

# 启动测试用的长安链与后端
# 会首先关闭目前已经启动的组件
boot-all: prepare
	make clean-all
	# make chain-up
	make build-contract
	make build-backend
	@echo "wait chain ready"
	sleep 5
	@echo "begin create contract"
	make create-contract 
	./scripts/boot.sh
	@echo "boot success"

boot-prod-all:
	make clean-all
	make chain-up
	make build-prod-contract
	make build-prod-backend
	@echo "wait chain ready"
	sleep 5
	@echo "begin create contract"
	make create-contract 
	./scripts/boot.sh
	@echo "boot success"

.PHONY: backend-test
# 执行后端的测试
backend-test:
	go test -c ./test -o unit-test
	./unit-test -test.v

chainmodel-test:
	go test -c ./chain/chainmaker -tags debug -o chainmodel\
	CONTRACT_FMT='example' \
	CONFIG_PATH_FMT='./testdata/sdk_config%d.yaml' \
	./chainmodel -test.v


bench-query-contract:
	cassowary run -u http://127.0.0.1:9001/api/exec/v1/contract -c 10 -n 3000 --postfile http-test/contract/get-contract.json

bench-contract-exec:
	cassowary run -u http://127.0.0.1:9001/api/exec/v1/ -c 10 -n 1000 --postfile http-test/contract/contract-exec.json


mysql:
	mysql -uroot -p123456

create-data:
	hurl http-test/namespace/create_namespace.http
	hurl http-test/gongyin-basic/create_data_declare.http
	hurl http-test/gongyin-basic/create-function-declare.http
	hurl http-test/gongyin-basic/create-function-declare2.http
	hurl http-test/gongyin-basic/create_data_declare2.http
	hurl http-test/gongyin-basic/create-contract.http
	hurl http-test/gongyin-basic/create-data.http
	hurl http-test/gongyin-basic/create-function2.http
	hurl http-test/gongyin-basic/create-function.http
	hurl http-test/gongyin-basic/create-data2.http

exec-res:
	hurl http-test/gongyin-basic/exec-contract.http 
