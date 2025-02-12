from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Tuple, Awaitable, Dict
import asyncio
from asyncio import Queue
from route0x.route_finder import RouteFinder
from gliner import GLiNER

from fastapi import FastAPI, HTTPException
from route0x.route_finder import RouteFinder
from gliner import GLiNER

app = FastAPI()

import numpy as np

def convert_numpy_numbers_to_python(data):
    for key, value in data.items():
        if isinstance(value, np.integer):
            data[key] = int(value)
        elif isinstance(value, np.floating):
            data[key] = float(value)
    return data




class ModelHealth:
    route_finder = None
    gliner_model = None

    @classmethod
    def load_models(cls):
        try:
            cls.route_finder = RouteFinder("/assets/run_20250117_101454/route0x_model")
            cls.gliner_model = GLiNER.from_pretrained("/assets/gliner_25_Med", load_tokenizer = True, local_files_only=True)
            print("Models loaded successfully.")
        except Exception as e:
            print(f"Failed to load models: {e}")




@app.get("/health-check")
async def health_check():
    try:
        if not (ModelHealth.route_finder and ModelHealth.route_finder.find_route("Test Route") and
                ModelHealth.gliner_model and ModelHealth.gliner_model.predict_entities(
                    "Nexon vs Car", labels = ["Car Model", "City"], threshold=0.5)
                ):
            raise ValueError("Model validation failed")
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Model health check failed: {str(e)}")
    return {"route_finder": "loaded and validated", "gliner": "loaded and validated"}



# Batching configuration
class Config:
    max_batch_size = 10
    wait_time = 0.1

queue_route_finder: Queue = Queue()
queue_gliner: Queue = Queue()


async def batch_process_routes(queue: Queue):
    while True:
        batch = [await queue.get()]
        while len(batch) < Config.max_batch_size and not queue.empty():
            batch.append(await queue.get())

        # Initialize an empty list to hold the results
        results = []

        # Process each query input individually
        for _, query in batch:
            result = ModelHealth.route_finder.find_route(query)
            result = convert_numpy_numbers_to_python(result)
            results.append(result)
        
        # Set results for each future in the batch
        for future, result in zip([item[0] for item in batch], results):
            future.set_result(result)
            queue.task_done()

async def batch_process_ner(queue: Queue):
    while True:
        batch = [await queue.get()]
        while len(batch) < Config.max_batch_size and not queue.empty():
            batch.append(await queue.get())

        # Initialize an empty list to hold the results
        results = []

        # Process each text input individually
        for _, text in batch:
            result = ModelHealth.gliner_model.predict_entities(text, labels=["Car Model", "City"], threshold=0.5)
            results.append(result)
        
        # Set results for each future in the batch
        for future, result in zip([item[0] for item in batch], results):
            future.set_result(result)
            queue.task_done()


class Query(BaseModel):
    text: str
    model: str

@app.post("/predict/")
async def predict(query: Query):
    future = asyncio.get_running_loop().create_future()
    if query.model == "route":
        await queue_route_finder.put((future, query.text))
    elif query.model == "ner":
        await queue_gliner.put((future, query.text))
    else:
        raise HTTPException(status_code=400, detail="Invalid model type")
    return await future


async def initialize_models():
    ModelHealth.load_models()

async def start_background_tasks():
    asyncio.create_task(batch_process_routes(queue_route_finder))
    asyncio.create_task(batch_process_ner(queue_gliner))

@app.on_event("startup")
async def startup_event():
    await initialize_models()
    await start_background_tasks()
