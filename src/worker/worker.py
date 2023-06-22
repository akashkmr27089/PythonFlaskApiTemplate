import logging
import time

queue = []
registered_worker = {}


class Worker:

    @staticmethod
    def register_worker(worker_name: str, func):
        registered_worker[worker_name] = func

    @staticmethod
    def worker_function():
        while True:
            try:
                if queue and len(queue) > 0:
                    time.sleep(1)
                    print("value of queue", queue)
                    params = queue.pop(0)
                    worker_name = params["name"]
                    worker_data = params["data"]

                    if worker_name in registered_worker:
                        logging.info("Worker {} fired with data".format(worker_name))
                        registered_worker[worker_name](worker_data)
            except Exception as ex:
                logging.info("Error while consuming queue for work")
                print("Error ", ex)
                pass
