# image_search_engine

[简体中文](./README.zh-CN.md) | [English](./README.md)

## 简介

开源的图片搜索引擎，让你可以便捷的搭建自己的以图搜图系统

- web 服务：python+fastapi
- 中间件：Mysql 存储图片元信息；使用 Minio 存储图片本身；milvus 存储向量
- 算法：配合微调的 ResNet50 模型

## 运行程序前的准备工作

### 项目依赖介绍

#### 存储图片的元信息——Mysql

图片存储到系统中，我们希望可以有一些元信息，比如：

- 图片的文件名
- 图片的存储路径（图片存储到 minio 中，所以存储在 minio 的什么位置，我们是需要记得的）
- 图片的 hashcode，用于唯一标记一个图片，方便去重等操作

所以，我们需要一个数据库来存储这些元信息，我们选用最流行的 Mysql

关于 Mysql 的更多内容，可以参考：https://dev.mysql.com/doc/

#### 存储图片本身——Minio

图片本身我们也需要存储，存储图片的方案有很多，比如：

- 本地存储（直接存储到运行程序的机器的磁盘上）
- HDFS、FastDFS 等分布式文件系统
- AWS S3、Aliyun OSS、Minio 等云原生的对象存储

对于上述的三种方案，我这里选择的是对象存储方案，原因如下：

- 本地存储局限性太大，分布式部署，失去了机器层面的水平扩缩容和容灾能力
- HDFS、FastDFS 这些分布式文件系统不适合小文件的存储，但是最重要的是生态配套太差，即运维困难，又没有配套的 GUI
- 云原生的对象存储是最好的：天生的分布式特性让你无须考虑容灾和性能问题、漂亮人性化的界面、易用的生态

关于 Mysql 的更多内容，可以参考：https://min.io/

#### 向量存储——Milvus

以图搜图的实现原理：

- 对于录入的图片（称之为母本），使用深度学习算法提取图片的特性（特性用向量表示）
- 特性具体使用深度学习的 ResNet50 神经网络提取
- 提取的特征，转化成一个浮点数序列，对应 Python 的数据结构就是 `list[float]`, list 的长度是 512，就是一共有 512 个 float
- 将提取的特征存储起来
- 当用户需要搜索的时候，会提交图片（称之为样本），希望得到和这个样本图片相似的母本图片
- 将样本图片也提取特征
- 然后将样本特征和一堆母本特征挨个比较，比较结果是一个「距离」，也是一个浮点数，数值越小表示相似度越高
- 然后给用户距离最小的 n 个图片

> 特征提取，我们使用 iv2 这个库：https://github.com/ponponon/iv2
> 我们会使用 `pip install iv2` 安装这个库

根据上面的描述，我们知道，有一个步骤是「将提取的特征存储起来」，存储这些特征，我们就用 milvus

milvus 是一个分布式的向量数据库，专门存储向量的

关于 milvus 的更多内容，可以参考：https://milvus.io/

### 运行程序

使用下面的 docker-compose.yaml 文件，可以一键启动以图搜图服务的前端、后端程序、以及相关的对象存储、向量数据库、元数据数据库

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

使用 http://127.0.0.1:6201/ 或者 http://{yourIp}:6201/ 访问以图搜图的前端服务

如果你想要包装这个以图搜图服务，可以访问 http://{yourIp}:6200/docs 可以访问后端 API 的接口文档

## 相关项目

- 配套的前端页面：https://github.com/ponponon/image_search_web
- 配套的特征提取库：https://github.com/ponponon/iv2
