from argparse import ArgumentParser, Namespace

import torch
from transformers import (
    DistilBertForSequenceClassification,
    DistilBertTokenizer,
    pipeline,
)


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--input", type=str, required=True)
    return parser.parse_args()


args = parse_args()
device = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
# model_name = "distilbert-base-uncased"

# # OPTION 1
# tokenizer = DistilBertTokenizer.from_pretrained(model_name)
# model = DistilBertForSequenceClassification.from_pretrained(model_name)
# model.to(device)

# inputs = tokenizer(args.input, return_tensors="pt")
# with torch.no_grad():
#     output = model(**{k: v.to(device) for k, v in inputs.items()})

# id2label = {0: "Positive", 1: "Negative"}
# print(f"Input: {args.input}")
# print(f"Output: {id2label[output.logits.argmax().item()]}")

# # OPTION 2
classifier = pipeline("text-classification", model=model_name, device=device)
output = classifier(args.input)


# label2label = {"LABEL_0": "Positive", "LABEL_1": "Negative"}
print(f"Input: {args.input}")
print(f"Output: {output}")
