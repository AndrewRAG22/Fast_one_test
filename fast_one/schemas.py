from pydantic import BaseModel


# verifica se esta correto
class Message(BaseModel):
    message: str
