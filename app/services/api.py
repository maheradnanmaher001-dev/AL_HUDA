import os, requests
BASE=os.getenv("ALHUDA_API_BASE_URL","https://your-domain.example/api")
def post(path,payload):
    return requests.post(BASE.rstrip("/")+"/"+path.lstrip("/"),json=payload,timeout=15)
