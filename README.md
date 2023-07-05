# image_search_engine

[简体中文](./README.zh-CN.md) | [English](./README.md)

## Introduction

An open source image search engine that allows you to easily build your own image search system

- web service: python+fastapi
- Middleware: Mysql to store image meta information; Minio to store the images themselves; milvus to store vectors
- Algorithm: ResNet50 model with fine-tuning

## Preparation before running the program

### Installing dependencies

#### Storing meta-information about images - Mysql

Images are stored to the system and we want to be able to have some meta-information, such as

- The file name of the image
- The path where the image is stored (the image is stored in minio, so where it is stored in minio is something we need to remember)
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
- Then the user is given the n images with the lowest distance

From the above description, we know that there is a step to 'store the extracted features' and to store these features, we use milvus

milvus is a distributed vector database, dedicated to storing vectors

For more on milvus, see: https://milvus.io/

## Running the program proper

The api service can be started by running the following command

```python
python api.py
```

> Dependent python version >= 3.10

This api service is responsible for the following functions:

- parent entry
- viewing the masters
- sample query
