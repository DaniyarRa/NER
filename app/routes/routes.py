from fastapi import APIRouter, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

tokenizer = AutoTokenizer.from_pretrained('yeshpanovrustem/xlm-roberta-large-ner-kazakh')
model = AutoModelForTokenClassification.from_pretrained('yeshpanovrustem/xlm-roberta-large-ner-kazakh')

nlp_none = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="none")
nlp_simple = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")


router = APIRouter()


router.mount("/app/static", StaticFiles(directory="app/static"), name="static")


@router.get("/", response_class=HTMLResponse)
async def get_page():
    with open("app/static/index.html", "r") as f:
        return f.read()


@router.post("/label")
async def submit_text(request: Request):
    data = await request.json()
    text = data["text"]
    option = data["option"]

    ner_results, message = None, 'N/A'
    if option == "Simple":
        message = _normalize_simple_ner(nlp_simple(text))
    elif option == "None":
        message = _normalize_ner(nlp_none(text))

    return {"message": message}


def _normalize_simple_ner(ner_results):
    result = '\n'.join([f'{result["word"]}\t{result["entity_group"]}' for result in ner_results])

    return result


def _normalize_ner(ner_results):
    token = ""
    label_list = []
    token_list = []

    for result in ner_results:
        if result["word"].startswith("▁"):
            if token:
                token_list.append(token.replace("▁", ""))
            token = result["word"]
            label_list.append(result["entity"])
        else:
            token += result["word"]

    token_list.append(token.replace("▁", ""))

    result = '\n'.join([f'{token}\t{label}' for token, label in zip(token_list, label_list)])

    return result