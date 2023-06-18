from fastapi import FastAPI, Query
from dotenv import load_dotenv
import os
import uvicorn
import logging
import src.opensearch.initialize
import src.setup.logging.logging
from src.opensearch.dao import OpensearchDao
from src.controller.controller import Controller

# Load the variables from .env file
load_dotenv()
if os.getenv("MIGRATION"):
    OpensearchDao.migration()

app = FastAPI()


# Get Data from Api Integration
# Push to Data Layer
# Get Response
@app.get("/get")
async def get_paragraph(nos_of_para: int = Query(1), nos_of_sentence: int = Query(50)):
    return await Controller.get(nos_of_para, nos_of_sentence)


# Get The Response from the Opensearch
@app.get("/search")
def search(query: str = Query(None)):
    return await Controller.search()


# Get Frequent Word from the Opensearch
# Get Dictionary Integration and get meaning
# return
@app.get("/dictionary")
async def get_dictionary_words(count: int = Query(10)):
    return await Controller.get_frequent_words(count)


@app.get("/")
def pong():
    return "pong"


if __name__ == "__main__":
    logging.info("Starting server at port 8000")
    uvicorn.run(app, host=os.getenv("HOST"), port=int(os.getenv("PORT")))
