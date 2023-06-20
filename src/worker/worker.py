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
            if queue:
                time.sleep(1)
                params = queue.pop(0)
                worker_name = params["name"]
                worker_data = params["data"]

                if worker_name in registered_worker:
                    logging.info("Worker {} fired with data {}".format(worker_name, worker_data))
                    registered_worker[worker_name](worker_data)
