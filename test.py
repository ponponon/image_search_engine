from fastapi import FastAPI, File, UploadFile, Form
from vectors import create_vector
from apps.schemas import CreateMetaResponse, ListMetaResponse, DeleteMetasResponse, ListMetaResult
from core.milvus.crud import insert_vector
from loguru import logger


logger.debug(ListMetaResponse.schema())
