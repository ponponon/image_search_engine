from pydantic import BaseModel


class RabbitMQConfig(BaseModel):
    host: str
    port: int
    username: str
    password: str
    vhost: str
