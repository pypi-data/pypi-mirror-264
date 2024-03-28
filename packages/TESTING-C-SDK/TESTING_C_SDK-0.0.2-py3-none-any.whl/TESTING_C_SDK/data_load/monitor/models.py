import datetime as dt
from sqlalchemy import Column, Integer, String, DateTime,JSON
from sqlalchemy.ext.declarative import declarative_base

from TESTING_C_SDK.data_load.config.database_config import engine


Base = declarative_base()



class ChatHistory(Base):
    """This model is to store the chat history of the user"""
    __tablename__ = "sdk_chat_history"
    id = Column(Integer, primary_key=True)
    like = Column("like",Integer)
    view =  Column("view",Integer)

Base.metadata.create_all(engine)