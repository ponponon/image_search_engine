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

### 安装运行依赖

如果你不熟悉这些中间件，或者不想把时间浪费在部署这些中间件上，我们也为你准备了 docker-compose 脚本一键运行

> 中间件指的就是 Mysql、minio、milvus

运行 mysql

```shell
cd deploy/docker/mysql
docker-compose up -d
```

运行 minio

```shell
cd deploy/docker/minio
docker-compose up -d
```

运行 milvus

```shell
cd deploy/docker/milvus
docker-compose up -d
```

> 注意：如果你细心，你会发现 milvus 的 docker-compose.yaml 文件中，也存在一个 minio。这个时候你心中是不是就有疑问？为什么我们还要额外运行一个 minio？一共就有两个 minio 了？是的！我们需要两个 minio ，milvus 的 minio 是 milvus 运行所需要的，用于持久化向量数据等用途。而我们单独部署的 minio 是用于存储图片的

## 运行程序本体

运行下面的命令，就可以启动 api 服务

```python
python api.py
```

> 依赖的 python 版本 >= 3.10

该 api 服务负责以下功能：

- 母本入库
- 查看母本
- 样本查询

如果运行成功，你会看到类似下面的输出：

```shell
╰─➤  python api.py
2023-07-05 23:02:23.707 | DEBUG    | settings:<module>:12 - 当前的运行模式: local
INFO:     Started server process [75085]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:6200 (Press CTRL+C to quit)
```

此时你可以在浏览器输入 http://127.0.0.1:6200/docs 查看接口文档
