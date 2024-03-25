# 远端镜像仓库路径, 默认是华为云容器镜像服务
REPO = swr.cn-north-4.myhuaweicloud.com/buaa-dist-compute-ci

# 通过定义TAG来改变ci镜像的tag
# 可以使用make TAG='...' 来定义TAG
# 例如 make TAG='1.18' golang-ci
ifdef TAG
IMAGE_TAG = $(TAG)
else
IMAGE_TAG = latest
endif

GOLANG_IMAGE = $(REPO)/golang-ci:$(IMAGE_TAG)

.PHONY: golang-ci update-golang-ci use-golang-ci
# 构建golang-ci镜像
golang-ci:
	docker build . -f golang-ci.dockerfile -t $(GOLANG_IMAGE)

# 将更新的golang-ci镜像推送到镜像仓库
update-golang-ci: golang-ci
	docker push $(GOLANG_IMAGE)

# 直接在本机使用golang-ci镜像, 这个目标会把项目根目录挂载到镜像的/usr/bin
use-golang-ci: golang-ci
	@echo "project directory is mounted on /usr/bin"
	docker run -it --rm -v `pwd`/..:/usr/src $(GOLANG_IMAGE)


RUST_IMAGE = $(REPO)/rust-ci:$(IMAGE_TAG)

.PHONY: rust-ci update-rust-ci use-rust-ci
# 构建rust-ci镜像
rust-ci:
	docker build . -f rust-ci.dockerfile -t $(RUST_IMAGE)

# 将更新的rust-ci镜像推送到镜像仓库
update-rust-ci: rust-ci
	docker push $(RUST_IMAGE)

# 直接在本机使用rust-ci镜像, 这个目标会把项目根目录挂载到镜像的/usr/bin
use-rust-ci: rust-ci
	@echo "project directory is mounted on /usr/bin"
	docker run -it --rm -v `pwd`/..:/usr/src $(RUST_IMAGE)

MYSQL_IMAGE = $(REPO)/mysql-ci:$(IMAGE_TAG)

.PHONY: mysql-ci update-mysql-ci use-mysql-ci
mysql-ci:
	docker build . -f mysql-ci.dockerfile -t $(MYSQL_IMAGE)

update-mysql-ci:
	docker push $(MYSQL_IMAGE)

use-mysql-ci:
	@echo "project directory is mounted on /usr/bin"
	docker run -it --rm -v `pwd`/..:/usr/src $(MYSQL_IMAGE)


STORAGE_DEV_IMAGE = $(REPO)/storage-dev:$(IMAGE_TAG)
.PHONY: storage-dev update-storage-dev
storage-dev:
	cp ../hbc .
	docker build .. -f storage.dockerfile -t $(STORAGE_DEV_IMAGE)

update-storage-dev:
	docker push $(STORAGE_DEV_IMAGE)