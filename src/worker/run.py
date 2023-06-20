import time

import uvicorn
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()
queue = []


def worker_function():
    while True:
        if queue:
            params = queue.pop(0)  # Get parameters from the queue
            # Execute the function using the parameters
            process_params(params)


def process_params(params):
    # Perform the desired processing logic with the parameters
    time.sleep(2)
    print(f"Processing params: {params}")


@app.get('/process')
async def process(background_tasks: BackgroundTasks):
    queue.append({"1" : "2"})  # Put parameters in the queue
    background_tasks.add_task(worker_function)  # Start the worker in the background
    return {'message': 'Request added to the queue'}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
