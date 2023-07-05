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

### Installing and running dependencies

If you are not familiar with the middleware, or don't want to waste time deploying it, we also have a docker-compose script for you to run with one click

> Middleware refers to Mysql, minio, milvus

Run mysql

```shell
cd deploy/docker/mysql
docker-compose up -d
```

Run minio

```shell
cd deploy/docker/minio
docker-compose up -d
```

Run milvus

```shell
cd deploy/docker/milvus
docker-compose up -d
```

> Note: If you're careful, you'll notice that there is a minio in the milvus docker-compose.yaml file. Why do we need to run an extra minio when we have two minio's? Yes! We need two minio's, the milvus minio is needed for milvus to run, for example to persist vector data. And the minio we deploy separately is for storing images

## Running the program proper

The api service can be started by running the following command

```python
python api.py
```

> Dependent python version >= 3.10

This api service is responsible for the following functions:

- parent entry
- viewing the masters
- Sample query

If it runs successfully, you will see output similar to the following:

```shell
╰─➤ python api.py
2023-07-05 23:02:23.707 | DEBUG | settings:<module>:12 - Current run mode: local
INFO: Started server process [75085]
INFO: Waiting for application startup.
INFO: Application startup complete.
INFO: Uvicorn running on http://0.0.0.0:6200 (Press CTRL+C to quit)
```

At this point you can view the interface documentation by typing http://127.0.0.1:6200/docs into your browser

## Related Projects

- Companion front-end page: https://github.com/ponponon/image_search_web
- Companion feature extraction library: https://github.com/ponponon/iv2
