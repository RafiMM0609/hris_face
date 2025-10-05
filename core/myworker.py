import traceback
import httpx
import requests

async def trigger_worker(function_name: str, data: dict):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"http://85.31.233.176:8003/run-heavy-tasks/{function_name}", json=data)
            # response = await client.post(f"http://localhost:8001/run-heavy-tasks/{function_name}", json=data)
            # response = await client.post(f"http://worker-service:8001/run-heavy-tasks/{function_name}", json=data)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        print(f"Error triggering worker for function {function_name}: {e}")
        traceback.print_exc()
        return {"error": str(e)}

def trigger_worker_sync(function_name: str, data: dict):
    """
    Synchronous version of trigger_worker function
    """
    try:
        response = requests.post(f"http://85.31.233.176:8003/run-heavy-tasks/{function_name}", json=data)
        # response = requests.post(f"http://localhost:8001/run-heavy-tasks/{function_name}", json=data)
        # response = requests.post(f"http://worker-service:8001/run-heavy-tasks/{function_name}", json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error triggering worker for function {function_name}: {e}")
        traceback.print_exc()
        return {"error": str(e)}

