import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline


class ClassificationRequest(BaseModel):
    text: str
    return_proba: bool = False


class ClassificationResponse(BaseModel):
    label: str
    score: float = None


app = FastAPI()
device = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
classifier = pipeline("text-classification", model=model_name, device=device)


@app.post("/classify")
async def classify(request: ClassificationRequest) -> ClassificationResponse:
    try:
        output = classifier(request.text)
        if request.return_proba:
            return ClassificationResponse(
                label=output[0]["label"], score=output[0]["score"]
            )
        else:
            return ClassificationResponse(label=output[0]["label"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
