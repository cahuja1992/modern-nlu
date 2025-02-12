import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def post_ner_query():
    url = "http://localhost:8000/predict/"
    headers = {'Content-Type': 'application/json'}
    data = '{"text": "Compare Nexon vs Car", "model": "ner"}'
    response = requests.post(url, headers=headers, data=data)
    return response.text

def post_route_query():
    url = "http://localhost:8000/predict/"
    headers = {'Content-Type': 'application/json'}
    data = '{"text": "Compare Nexon vs Car", "model": "route"}'
    response = requests.post(url, headers=headers, data=data)
    return response.text

def session_task(session_id):
    start_time = time.time()
    ner_response = post_ner_query()
    route_response = post_route_query()
    end_time = time.time()
    elapsed_time = end_time - start_time
    return f"Session {session_id}: NER Response: {ner_response}, Route Response: {route_response}, Elapsed Time: {elapsed_time:.2f} seconds"

def simulate_concurrent_sessions(num_sessions):
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=num_sessions) as executor:
        # Creating a future for each session
        futures = [executor.submit(session_task, i) for i in range(num_sessions)]
        
        # As each future completes, print its result
        for future in as_completed(futures):
            print(future.result())

    total_time = time.time() - start_time
    print(f"Total Execution Time: {total_time:.2f} seconds")

num_sessions = 5
simulate_concurrent_sessions(num_sessions)
