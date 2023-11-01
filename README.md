# image_search_engine

[简体中文](./README.zh-CN.md) | [English](./README.md)

## Introduction

An open source image search engine that allows you to easily build your own image search system

- web service: python+fastapi
- Middleware: Mysql to store image meta information; Minio to store the images themselves; milvus to store vectors
- Algorithm: ResNet50 model with fine-tuning

## Preparation before running the program

### Introduction to project dependencies

#### Storing meta-information about images - Mysql

Images are stored into the system and we want to be able to have some meta-information, such as

- The file name of the image
- The storage path of the image (the image is stored in minio, so where it is stored in minio is something we need to remember)
- the hashcode of the image, which is used to uniquely mark an image for operations such as de-duplication

So, we need a database to store this meta information, and we use the most popular one, Mysql

For more on Mysql, see: https://dev.mysql.com/doc/

#### Storing the images themselves - Minio

The images themselves we also need to store, and there are many options for storing images, such as

- Local storage (directly to the disk of the machine where the program is running)
- Distributed file systems such as HDFS, FastDFS
- Cloud-native object storage such as AWS S3, Aliyun OSS, Minio, etc.

For all three of these options, I have chosen the object storage option here for the following reasons:

- Local storage limitations are too great for distributed deployment, losing the ability to scale up and down horizontally at the machine level and for disaster recovery
- HDFS, FastDFS These distributed file systems are not suitable for small file storage, but most importantly, the ecological support is too poor, i.e. difficult to operate and maintain, and there is no supporting GUI
- Cloud-native object storage is the best: inherently distributed so you don't have to think about disaster recovery and performance, a beautiful user-friendly interface, and an easy-to-use ecosystem.

For more on Mysql, see: https://min.io/

#### vector storage - Milvus

The principle behind the implementation of image search:

- A deep learning algorithm is used to extract the characteristics of a recorded image (called a master) (characteristics are represented as vectors)
- The features are extracted using a deep learning ResNet50 neural network
- The extracted features are transformed into a sequence of floats, which corresponds to the Python data structure `list[float]`, the length of the list is 512, which means there are 512 floats in total
- to store the extracted features
- When the user needs to search, he submits an image (called a sample) and wants to get a master image that is similar to the sample image
- Extract the features from the sample image as well
- The sample features are then compared one by one with a bunch of parent features, the result of the comparison is a "distance", also a float, where a smaller value means a higher similarity
- Then give the user the n images with the lowest distance

> For feature extraction, we use the iv2 library: https://github.com/ponponon/iv2
> We will install this library using `pip install iv2`

From the above description, we know that there is a step to "store the extracted features" and to store these features, we use milvus

milvus is a distributed vector database, dedicated to storing vectors

For more on milvus, see: https://milvus.io/

### Run

Using the following docker-compose.yaml file, you can start the front-end and back-end programs of the image search service with one click, as well as the associated object storage, vector database, and metadata database

```yaml
version: "3"
services:
  image-search-engine:
    container_name: image-search-engine
    restart: always
    image: ponponon/image_search_engine:2023.11.01.1
    logging:
      driver: json-file
      options:
        max-size: "20m"
        max-file: "1"
    environment:
      - RUN_MODE=docker
      - LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libjemalloc.so.2
    ports:
      - "6200:6200"
    command: python api.py
    volumes:
      - ./config.yaml:/code/config.yaml
    deploy:
      resources:
        limits:
          cpus: "4"
          memory: 1200M
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:6200"]
      interval: 30s
      timeout: 30s
      retries: 3
      start_period: 30s
    depends_on:
      - "etcd"
      - "minio"
      - "standalone"
      - "image-search-engine-minio"
      - "mysql8"
  image-search-web:
    container_name: image_search_web
    restart: always
    image: ponponon/image_search_web:2023.11.01.1
    logging:
      driver: json-file
      options:
        max-size: "20m"
        max-file: "5"
    ports:
      - "6201:6201"
    depends_on:
      - "etcd"
      - "minio"
      - "standalone"
      - "image-search-engine-minio"
      - "mysql8"
      - "image-search-engine"
  etcd:
    container_name: image-search-engine-milvus-etcd
    image: quay.io/coreos/etcd:v3.5.5
    restart: always
    environment:
      - ETCD_AUTO_COMPACTION_MODE=revision
      - ETCD_AUTO_COMPACTION_RETENTION=1000
      - ETCD_QUOTA_BACKEND_BYTES=4294967296
      - ETCD_SNAPSHOT_COUNT=50000
    volumes:
      - ${DOCKER_VOLUME_DIRECTORY:-.}/volumes/etcd:/etcd
    command: etcd -advertise-client-urls=http://127.0.0.1:2379 -listen-client-urls http://0.0.0.0:2379 --data-dir /etcd
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:2379/health"]
      interval: 30s
      timeout: 20s
      retries: 3
    logging:
      driver: "json-file"
      options:
        max-file: "1"
        max-size: "50m"

  minio:
    container_name: image-search-engine-milvus-minio
    image: minio/minio:RELEASE.2023-03-20T20-16-18Z
    restart: always
    environment:
      MINIO_ACCESS_KEY: minioadmin
      MINIO_SECRET_KEY: minioadmin
    volumes:
      - ${DOCKER_VOLUME_DIRECTORY:-.}/volumes/minio:/minio_data
    command: minio server /minio_data --console-address ":9001"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 20s
      retries: 3
    logging:
      driver: "json-file"
      options:
        max-file: "1"
        max-size: "50m"

  standalone:
    container_name: image-search-engine-milvus-standalone
    image: milvusdb/milvus:v2.3.2
    command: ["milvus", "run", "standalone"]
    restart: always
    environment:
      ETCD_ENDPOINTS: etcd:2379
      MINIO_ADDRESS: minio:9000
    volumes:
      - ${DOCKER_VOLUME_DIRECTORY:-.}/volumes/milvus:/var/lib/milvus
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9091/healthz"]
      interval: 30s
      start_period: 90s
      timeout: 20s
      retries: 3
    ports:
      - "19530:19530"
      - "9091:9091"
    depends_on:
      - "etcd"
      - "minio"
    logging:
      driver: "json-file"
      options:
        max-file: "1"
        max-size: "50m"

  zilliz_attu:
    container_name: zilliz_attu
    image: zilliz/attu:v2.3.2
    restart: always
    environment:
      HOST_URL: http://0.0.0.0:8000
      MILVUS_URL: standalone:19530
    ports:
      - "8000:3000"
    logging:
      driver: "json-file"
      options:
        max-file: "1"
        max-size: "50m"

  image-search-engine-minio:
    container_name: image-search-engine-minio
    restart: always
    image: minio/minio:RELEASE.2023-09-04T19-57-37Z
    ports:
      - "9000:9000" # client port
      - "9002:9002" # console port
    command: server /data --console-address ":9002" #指定容器中的目录 /data
    volumes:
      - ./volumes/image-search-engine-minio/:/data
    environment:
      MINIO_ACCESS_KEY: ponponon #管理后台用户名
      MINIO_SECRET_KEY: ponponon #管理后台密码，最小8个字符
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 20s
      retries: 3
    logging:
      driver: "json-file"
      options:
        max-file: "1"
        max-size: "50m"

  mysql8:
    container_name: mysql8
    image: mysql:8.0.34
    restart: always
    ports:
      - "3306:3306"
    environment:
      - MYSQL_ROOT_PASSWORD=Ep7zMmBfXm4y3wx
      - MYSQL_DATABASE=image_search_engine
    volumes:
      - ./volumes/mysql/:/var/lib/mysql
      - ./my-custom.cnf:/etc/mysql/conf.d/my-custom.cnf
    healthcheck:
      test: ["CMD-SHELL", "mysqladmin ping -h localhost"]
      interval: 30s
      timeout: 10s
      retries: 3
    logging:
      driver: "json-file"
      options:
        max-file: "1"
        max-size: "50m"
```

Use http://127.0.0.1:6201/ or http://{yourIp}:6201/ to access the map search front-end service.

If you want to wrap the map search service, You can access http://{yourIp}:6200/docs You can access the interface documentation for the back-end API

## Related Projects

- Companion front-end page: https://github.com/ponponon/image_search_web
- Companion feature extraction library: https://github.com/ponponon/iv2
