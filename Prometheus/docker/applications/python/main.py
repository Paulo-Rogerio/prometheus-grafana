import random
import uvicorn
import prometheus_client

from fastapi import FastAPI, HTTPException, Response, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

heads_count = prometheus_client.Counter(
    "heads_count",
    "Number of heads",
)

tails_count = prometheus_client.Counter(
    "tails_count",
    "Number of tails",
)

flip_count = prometheus_client.Counter(
    "flip_count",
    "Number of flips",
)

@app.get("/flip-coins")
async def flip_coins(times=None):

    if times is None or not times.isdigit():
        raise HTTPException(
            status_code=404, 
            detail="Times must be set in request and an integer"
        )

    times_as_int = int(times)

    heads = 0
    for _ in range(times_as_int):
        if random.randint(0, 1):
            heads += 1
    
    tails = times_as_int - heads

    heads_count.inc(heads)
    tails_count.inc(tails)
    flip_count.inc(times_as_int)

    return {
        "heads": heads,
        "tails": tails
    }


@app.get("/metrics")
async def get_metrics():
    return Response(
        content=prometheus_client.generate_latest(),
        media_type="text/plain"
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3002)    
