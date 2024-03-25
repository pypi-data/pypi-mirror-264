# 使用cmc命令行工具, 将合约上链
create-contract:
	cmc client contract user create \
		--contract-name=example    \
		--runtime-type=WASMER         \
		--byte-code-path=../contract.wasm \
		--version=1.0                 \
		--sdk-conf-path=./sdk_config1.yaml \
		--admin-key-file-paths=./crypto/wx-org1.chainmaker.org/certs/user/admin1/admin1.tls.key,./crypto/wx-org2.chainmaker.org/certs/user/admin1/admin1.tls.key,./crypto/wx-org3.chainmaker.org/certs/user/admin1/admin1.tls.key \
		--admin-crt-file-paths=./crypto/wx-org1.chainmaker.org/certs/user/admin1/admin1.tls.crt,./crypto/wx-org2.chainmaker.org/certs/user/admin1/admin1.tls.crt,./crypto/wx-org3.chainmaker.org/certs/user/admin1/admin1.tls.crt \
		--admin-org-ids=wx-org1.chainmaker.org,wx-org2.chainmaker.org,wx-org3.chainmaker.org \
		--sync-result=true \
		--params='{}'

NS=gitlab-ci

prepare:
	@echo "prepare crypto and sdk config, instance: $(INSTANCE)"
	./prepare.py $(INSTANCE)

chain-up:
	@echo "blockchain up, instance: $(INSTANCE)"
	kubectl create configmap $(INSTANCE)-node1 \
		--from-file=./flat/wx-org1.chainmaker.org \
		-n $(NS)
	kubectl label configmap $(INSTANCE)-node1 \
		buaa-gitlab-ci=$(INSTANCE) \
		-n $(NS)

	kubectl create configmap $(INSTANCE)-node2 \
		--from-file=./flat/wx-org2.chainmaker.org \
		-n $(NS)
	kubectl label configmap $(INSTANCE)-node2 \
		buaa-gitlab-ci=$(INSTANCE) \
		-n $(NS)

	kubectl create configmap $(INSTANCE)-node3 \
		--from-file=./flat/wx-org3.chainmaker.org \
		-n $(NS)
	kubectl label configmap $(INSTANCE)-node3 \
		buaa-gitlab-ci=$(INSTANCE) \
		-n $(NS)

	kubectl create configmap $(INSTANCE)-node4 \
		--from-file=./flat/wx-org4.chainmaker.org \
		-n $(NS)
	kubectl label configmap $(INSTANCE)-node4 \
		buaa-gitlab-ci=$(INSTANCE) \
		-n $(NS)

	kubectl apply -f deployment.yml -n $(NS)
	kubectl rollout status deployment/cm-$(INSTANCE)-node1 -n $(NS)
	kubectl rollout status deployment/cm-$(INSTANCE)-node2 -n $(NS)
	kubectl rollout status deployment/cm-$(INSTANCE)-node3 -n $(NS)
	kubectl rollout status deployment/cm-$(INSTANCE)-node4 -n $(NS)

chain-down:
	@echo "blockchain down"
	- kubectl delete -f deployment.yml -n $(NS)
	- kubectl delete configmap -l "buaa-gitlab-ci=$(INSTANCE)"

.PHONY: prepare chain-up chain-down create-contract