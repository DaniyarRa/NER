from fastapi import APIRouter, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from transformers import AutoTokenizer
import onnxruntime
import numpy as np
import torch
import torch.nn.functional as F
import json

tokenizer = AutoTokenizer.from_pretrained('tokenizer_onnx')
ort_session = onnxruntime.InferenceSession('tokenizer_onnx/model.onnx', providers=["CPUExecutionProvider"])

router = APIRouter()


router.mount("/app/static", StaticFiles(directory="app/static"), name="static")


@router.get("/", response_class=HTMLResponse)
async def get_page():
    with open("app/static/index.html", "r") as f:
        return f.read()


@router.post("/label")
async def submit_text(request: Request):
    data = await request.json()
    text = data['text']
    probabilities, input_ids = run_ner_inference(text)

    predicted_classes = np.argmax(probabilities, axis=-1)

    config = json.load(open('tokenizer_onnx/config.json'))
    id2label = config['id2label']

    predicted_labels = [id2label[str(class_id)] for class_id in predicted_classes[0]]

    tokens = tokenizer.convert_ids_to_tokens(input_ids[0])
    clean_tokens, clean_labels = clean_and_combine_tokens(tokens, predicted_labels)

    message = ' '.join([label if label in ['B-CONTACT', 'B-PERSON'] else token for token, label in zip(clean_tokens, clean_labels)])

    return {"message": message}


def run_ner_inference(input_text):
    encoded_input = tokenizer(input_text, padding=True, truncation=True, return_tensors="pt", add_special_tokens=True)
    input_ids = encoded_input['input_ids'].numpy()
    attention_mask = encoded_input['attention_mask'].numpy()

    ort_inputs = {
        "input_ids": input_ids,
        "attention_mask": attention_mask
    }

    ort_outs = ort_session.run(['logits'], ort_inputs)
    logits = ort_outs[0]

    probabilities = F.softmax(torch.from_numpy(logits), dim=-1).numpy()

    return probabilities, input_ids


def clean_and_combine_tokens(tokens, labels):
    cleaned_tokens = []
    cleaned_labels = []
    current_word = ""
    current_label = None

    for token, label in zip(tokens, labels):
        if token in ["<s>", "</s>", "<unk>"]:
            continue

        if token.startswith("▁"):
            if current_word:
                cleaned_tokens.append(current_word)
                cleaned_labels.append(current_label)
            current_word = token[1:]
            current_label = label
        else:
            current_word += token

        if current_label == "O":
            current_label = label

    if current_word:
        cleaned_tokens.append(current_word)
        cleaned_labels.append(current_label)

    return cleaned_tokens, cleaned_labels
