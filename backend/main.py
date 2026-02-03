from fastapi import FastAPI
from datetime import datetime
import random

app = FastAPI()

@app.get("/live-sales")
def live_sales(count: int = 100):
    data = []
    for _ in range(count):
        data.append({
            "amount": random.randint(100, 5000),
            "time": datetime.now().isoformat()
        })
    return data
