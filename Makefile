NAME = ponponon/image_search_engine
VERSION = 2023.10.31.1

.PHONY: build up stop logs

build:  docker-build
up: docker-compose-up
stop: docker-compose-stop
logs: docker-compose-logs
test: image-search-engine-test

docker-build:
	docker build -t "${NAME}:${VERSION}" . -f deploy/docker/private/Dockerfile

docker-compose-up:
	docker-compose -f deploy/docker/private/docker-compose.yml up -d

docker-compose-stop:
	docker-compose -f deploy/docker/private/docker-compose.yml stop

docker-compose-logs:
	docker-compose -f deploy/docker/private/docker-compose.yml logs --tail=100 -f
image-search-engine-test:
	python -m unittest discover
