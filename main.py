from fastapi import FastAPI, Query, BackgroundTasks
from dotenv import load_dotenv
import os
import uvicorn
import logging
import src.opensearch.initialize
import src.setup.logging.logging
from src.models.models import pgdb_migration

from src.pgdb.initialize import connect

from src.opensearch.initialize import check_opensearch_status
from src.opensearch.dao import OpensearchDao
from src.controller.controller import Controller
from src.worker.paragraph_worker import ParagraphWorker
from src.worker.frequent_word_worker import FrequentWordWorker

from src.worker.worker import Worker

# Load the variables from .env file
load_dotenv()
logging.info(os.getenv("OPENSEARCH_HOST"))

# This is for connecting to Postgres
while not connect():
    continue

if os.getenv("MIGRATION"):
    check_opensearch_status()
    OpensearchDao.migration()

Worker.register_worker("paragraph", ParagraphWorker.process_paragraph)
Worker.register_worker("frequent_word", FrequentWordWorker.process_frequent_words)


app = FastAPI()

# Get Data from Api Integration
# Push to Data Layer
# Get Response
@app.get("/get")
async def get_paragraph(background_tasks: BackgroundTasks, nos_of_para: int = Query(1),
                        nos_of_sentence: int = Query(50)):
    # background_tasks.add_task(ParagraphWorker.worker_function)
    # background_tasks2.add_task(FrequentWordWorker.worker_function)

    background_tasks.add_task(Worker.worker_function)

    return await Controller.get(nos_of_para, nos_of_sentence)


# Get The Response from the Opensearch
@app.get("/search")
async def search(search_or: str = Query(None), search_and: str = Query(None)):
    return await Controller.search(search_or, search_and)


# Get Frequent Word from the Opensearch
# Get Dictionary Integration and get meaning
# return
@app.get("/dictionary")
async def get_dictionary_words():
    return await Controller.get_frequent_words()


@app.get("/")
def pong():
    return "pong"


if __name__ == "__main__":
    logging.info("Starting server at port {}".format(os.getenv("HOST")))
    uvicorn.run(app, host=os.getenv("HOST"), port=int(os.getenv("PORT")))
