---
license: cc-by-4.0
language:
- kk
metrics:
- seqeval
pipeline_tag: token-classification
tags:
- Named Entity Recognition
- NER
widget:
- text: >-
    Қазақстан Республикасы — Шығыс Еуропа мен Орталық Азияда орналасқан
    мемлекет.
  example_title: Example 1
- text: Ахмет Байтұрсынұлы — қазақ тілінің дыбыстық жүйесін алғашқы құрған ғалым.
  example_title: Example 2
- text: >-
    Қазақстан мен ЕуроОдақ арасындағы тауар айналым былтыр 38% өсіп, 40 миллиард
    долларға жетті. Екі тарап серіктестікті одан әрі нығайтуға мүдделі. Атап
    айтсақ, Қазақстан Еуропаға құны 2 млрд доллардан асатын 175 тауар экспорттын
    ұлғайтуға дайын.
  example_title: Example 3
datasets:
- yeshpanovrustem/ner-kazakh
---

# A Named Entity Recognition Model for Kazakh
- The model was inspired by the [LREC 2022](https://lrec2022.lrec-conf.org/en/) paper [*KazNERD: Kazakh Named Entity Recognition Dataset*](https://aclanthology.org/2022.lrec-1.44).
- The model was trained for 3 epochs on [*ner_kazakh*](https://huggingface.co/datasets/yeshpanovrustem/kaznerd_cleaned).
- The original repository for the paper can be found at *https://github.com/IS2AI/KazNERD*.

## How to use
You can use this model with the Transformers pipeline for NER. 

```python
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

tokenizer = AutoTokenizer.from_pretrained("yeshpanovrustem/xlm-roberta-large-ner-kazakh")
model = AutoModelForTokenClassification.from_pretrained("yeshpanovrustem/xlm-roberta-large-ner-kazakh")

# aggregation_strategy = "none"
nlp = pipeline("ner", model = model, tokenizer = tokenizer, aggregation_strategy = "none")
example = "Қазақстан Республикасы — Шығыс Еуропа мен Орталық Азияда орналасқан мемлекет."

ner_results = nlp(example)
for result in ner_results:
    print(result)

# output:
# {'entity': 'B-GPE', 'score': 0.9995646, 'index': 1, 'word': '▁Қазақстан', 'start': 0, 'end': 9}
# {'entity': 'I-GPE', 'score': 0.9994935, 'index': 2, 'word': '▁Республикасы', 'start': 10, 'end': 22}
# {'entity': 'B-LOCATION', 'score': 0.99906737, 'index': 4, 'word': '▁Шығыс', 'start': 25, 'end': 30}
# {'entity': 'I-LOCATION', 'score': 0.999153, 'index': 5, 'word': '▁Еуропа', 'start': 31, 'end': 37}
# {'entity': 'B-LOCATION', 'score': 0.9991597, 'index': 7, 'word': '▁Орталық', 'start': 42, 'end': 49}
# {'entity': 'I-LOCATION', 'score': 0.9991725, 'index': 8, 'word': '▁Азия', 'start': 50, 'end': 54}
# {'entity': 'I-LOCATION', 'score': 0.9992299, 'index': 9, 'word': 'да', 'start': 54, 'end': 56}

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

for token, label in zip(token_list, label_list):
    print(f"{token}\t{label}")

# output:
# Қазақстан	B-GPE
# Республикасы	I-GPE
# Шығыс	B-LOCATION
# Еуропа	I-LOCATION
# Орталық	B-LOCATION
# Азияда	I-LOCATION

# aggregation_strategy = "simple"
nlp = pipeline("ner", model = model, tokenizer = tokenizer, aggregation_strategy = "simple")
example = "Қазақстан Республикасы — Шығыс Еуропа мен Орталық Азияда орналасқан мемлекет."

ner_results = nlp(example)
for result in ner_results:
    print(result)

# output:
# {'entity_group': 'GPE', 'score': 0.999529, 'word': 'Қазақстан Республикасы', 'start': 0, 'end': 22}
# {'entity_group': 'LOCATION', 'score': 0.9991102, 'word': 'Шығыс Еуропа', 'start': 25, 'end': 37}
# {'entity_group': 'LOCATION', 'score': 0.9991874, 'word': 'Орталық Азияда', 'start': 42, 'end': 56}

```

## Evaluation results on the validation and test sets
|  | Validation set |  |  | Test set|  |
|:---:| :---: | :---: | :---: | :---: | :---: |
| **Precision** | **Recall** | **F<sub>1</sub>-score** | **Precision** | **Recall** | **F<sub>1</sub>-score** |
| 96.58% | 96.66% | 96.62% | 96.49% | 96.86% | 96.67% |

## Model performance for the NE classes of the validation set
| NE Class | Precision | Recall | F<sub>1</sub>-score | Support |
| :---: | :---: | :---: | :---: | :---: |
| **ADAGE** | 90.00% | 47.37% | 62.07% | 19 |
| **ART** | 91.36% | 95.48% | 93.38% | 155 |
| **CARDINAL** | 98.44% | 98.37% | 98.40% | 2,878 |
| **CONTACT** | 100.00% | 83.33% | 90.91% | 18 |
| **DATE** | 97.38% | 97.27% | 97.33% | 2,603 |
| **DISEASE** | 96.72% | 97.52% | 97.12% | 121 |
| **EVENT** | 83.24% | 93.51% | 88.07% | 154 |
| **FACILITY** | 68.95% | 84.83% | 76.07% | 178 |
| **GPE** | 98.46% | 96.50% | 97.47% | 1,656 |
| **LANGUAGE** | 95.45% | 89.36% | 92.31% | 47 |
| **LAW** | 87.50% | 87.50% | 87.50% | 56 |
| **LOCATION** | 92.49% | 93.81% | 93.14% | 210 |
| **MISCELLANEOUS** | 100.00% | 76.92% | 86.96% | 26 |
| **MONEY** | 99.56% | 100.00% | 99.78% | 455 |
| **NON_HUMAN** | 0.00% | 0.00% | 0.00% | 1 |
| **NORP** | 95.71% | 95.45% | 95.58% | 374 |
| **ORDINAL** | 98.14% | 95.84% | 96.98% | 385 |
| **ORGANISATION** | 92.19% | 90.97% | 91.58% | 753 |
| **PERCENTAGE** | 99.08% | 99.08% | 99.08% | 437 |
| **PERSON** | 98.47% | 98.72% | 98.60% | 1,175 |
| **POSITION** | 96.15% | 97.79% | 96.96% | 587 |
| **PRODUCT** | 89.06% | 78.08% | 83.21% | 73 |
| **PROJECT** | 92.13% | 95.22% | 93.65% | 209 |
| **QUANTITY** | 97.58% | 98.30% | 97.94% | 411 |
| **TIME** | 94.81% | 96.63% | 95.71% | 208 |
| **micro avg** | **96.58%** | **96.66%** | **96.62%** | **13,189** |
| **macro avg** | **90.12%** | **87.51%** | **88.39%** | **13,189** |
| **weighted avg** | **96.67%** | **96.66%** | **96.63%** | **13,189** |

## Model performance for the NE classes of the test set
| NE Class | Precision | Recall | F<sub>1</sub>-score | Support |
| :---: | :---: | :---: | :---: | :---: |
| **ADAGE** | 71.43% | 29.41% | 41.67% | 17 |
| **ART** | 95.71% | 96.89% | 96.30% | 161 |
| **CARDINAL** | 98.43% | 98.60% | 98.51% | 2,789 |
| **CONTACT** | 94.44% | 85.00% | 89.47% | 20 |
| **DATE** | 96.59% | 97.60% | 97.09% | 2,584 |
| **DISEASE** | 87.69% | 95.80% | 91.57% | 119 |
| **EVENT** | 86.67% | 92.86% | 89.66% | 154 |
| **FACILITY** | 74.88% | 81.73% | 78.16% | 197 |
| **GPE** | 98.57% | 97.81% | 98.19% | 1,691 |
| **LANGUAGE** | 90.70% | 95.12% | 92.86% | 41 |
| **LAW** | 93.33% | 76.36% | 84.00% | 55 |
| **LOCATION** | 92.08% | 89.42% | 90.73% | 208 |
| **MISCELLANEOUS** | 86.21% | 96.15% | 90.91% | 26 |
| **MONEY** | 100.00% | 100.00% | 100.00% | 427 |
| **NON_HUMAN** | 0.00% | 0.00% | 0.00% | 1 |
| **NORP** | 99.46% | 99.18% | 99.32% | 368 |
| **ORDINAL** | 96.63% | 97.64% | 97.14% | 382 |
| **ORGANISATION** | 90.97% | 91.23% | 91.10% | 718 |
| **PERCENTAGE** | 98.05% | 98.05% | 98.05% | 462 |
| **PERSON** | 98.70% | 99.13% | 98.92% | 1,151 |
| **POSITION** | 96.36% | 97.65% | 97.00% | 597 |
| **PRODUCT** | 89.23% | 77.33% | 82.86% | 75 |
| **PROJECT** | 93.69% | 93.69% | 93.69% | 206 |
| **QUANTITY** | 97.26% | 97.02% | 97.14% | 403 |
| **TIME** | 94.95% | 94.09% | 94.52% | 220 |
| **micro avg** | **96.54%** | **96.85%** | **96.69%** | **13,072** |
| **macro avg** | **88.88%** | **87.11%** | **87.55%** | **13,072** |
| **weighted avg** | **96.55%** | **96.85%** | **96.67%** | **13,072** |