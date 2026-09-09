from fastapi import FastAPI

app = FastAPI(title="Enterprise AI Knowledge Copilot")


@app.get("/")
def root():
    return {
        "message": "Enterprise AI Knowledge Copilot API is running!"
    }