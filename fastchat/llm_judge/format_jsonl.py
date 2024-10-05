# %%
import json
from pathlib import Path
import pandas as pd

# %%
data_dir = Path("/home/boren/data/llm/phi3/inflection_long_convo_gen_clean_0602/")
json_file = data_dir / "egs.json"
jsonl_file = data_dir / "test_sft.jsonl"
output_dir = data_dir / "multi_qa"
output_dir.mkdir(exist_ok=True, parents=True)
# %%


def get_turns(messages, role):
    return [msg["content"] for msg in messages if msg["role"] == role]


def to_qa(data, id):
    return (
        {
            "question_id": id,
            "category": data["metadata"]["subtopic"].split("/")[0],
            "turns": get_turns(data["messages"], "user"),
        },
        {
            "question_id": id,
            "answer_id": str(id),
            "model_id": "reference",
            "choices": [
                {"index": 0, "turns": get_turns(data["messages"], "assistant")}
            ],
            "tstamp": 0.0,
        },
    )


# %%
qas = []
with jsonl_file.open() as f:
    for i, line in enumerate(f):
        data = json.loads(line)
        qas.append(to_qa(data, i))

question_jsonl = output_dir / "questions.jsonl"
answer_jsonl = output_dir / "answers.jsonl"

with question_jsonl.open("w") as qf, answer_jsonl.open("w") as af:
    for q, a in qas:
        print(json.dumps(q), file=qf)
        print(json.dumps(a), file=af)
# %%
