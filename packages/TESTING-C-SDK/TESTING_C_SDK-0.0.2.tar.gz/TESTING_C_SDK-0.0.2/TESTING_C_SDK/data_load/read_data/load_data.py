#from covalense_test_fin.config.database_config import SessionLocal
from TESTING_C_SDK.data_load.monitor.models import ChatHistory 
from TESTING_C_SDK.data_load.config.database_config import SessionLocal
from sqlalchemy import create_engine,URL
from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from rich.console import Console
console = Console()
from sqlalchemy.orm import sessionmaker
import pandas as pd

class data_loading:

    def __init__(self) -> None:
        pass

    def _load_csv(self,filename):
        
        db = SessionLocal()
        try:
            data = pd.read_csv(filename)
            new_data = data.to_dict(orient="records")
            for ele in new_data:
                db_item = ChatHistory(**ele)
                db.add(db_item)
                db.commit()
                db.refresh(db_item)
            return "Data has been loaded successfully"
            #return db_item
        except Exception as e:
            print("Below is the error ",e)
        finally:
            db.close()
