# %%
# pylint: disable=all
import pandas as pd
from pathlib import Path
import json
import fire


def read_jsonl(jsonl_path: Path, pfx=""):
    with jsonl_path.open() as f:
        dfs = []
        for line in f:
            data = json.loads(line)
            df = pd.DataFrame(
                {"qid": [data["question_id"]] * len(data["turns"]), "turn": data["turns"]}
            )
            df["text"] = df["turn"].str.replace(r"[\n\t\s]+", " ", regex=True)
            df["id"] = df.apply(lambda x: f"{pfx}{x.qid}_{x.name}", axis=1)
            dfs.append(df)
        data = pd.concat(dfs, ignore_index=True)
    return data


def proc_jsonl(input_dir, output_dir):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    for jsonl_file in input_dir.glob("*.jsonl"):
        name = jsonl_file.stem
        tsv_file = output_dir / f"{name}.tsv"
        print(f"Processing {jsonl_file}")
        data = read_jsonl(jsonl_file, pfx=f"mt_")
        data.to_csv(tsv_file, sep="\t", index=False, columns=["qid", "id", "text"])
        n_chat = len(data.groupby("qid"))
        print(f"Processed {n_chat} chats with {len(data)} utterances.")
        print(f"Saved to {tsv_file}")


# %%
input_dir = "/home/boren/FastChat/fastchat/llm_judge/dev_data/mt_bench"
output_dir = "/home/boren/FastChat/fastchat/llm_judge/dev_data/mt_bench"
proc_jsonl(input_dir, output_dir)
# %%
trans_dir = Path(input_dir) / "tts_tsv"
trans_dir.mkdir(exist_ok=True)
# use the clean ref wav
# https://tsstd01wus2.blob.core.windows.net/users/jingpan/tts_audioprompt/extracteddata/enus/
# librivox/waves/chunk_007ce7684fa4db4da85afadea93b7229_0_00008.wav
ref_wav = "chunk_007ce7684fa4db4da85afadea93b7229_0_00008.wav"

for tsv_file in Path(input_dir).glob("quest*.tsv"):
    data = pd.read_csv(tsv_file, sep="\t")
    n_chat = len(data.groupby("qid"))
    print("Processed", tsv_file.stem)
    print(f"Processed {n_chat} chats with {len(data)} utterances.")
    data["ref_wav"] = ref_wav
    tts_data = data[["ref_wav", "id", "text"]]
    tts_tsv = (trans_dir / tsv_file.name).with_suffix(".tts.tsv")
    print(f"Saved {len(tts_data)} utts to {tts_tsv}")
    tts_data.to_csv(tts_tsv, sep="\t", index=False, header=False)

    ref_tsv = (trans_dir / tsv_file.name).with_suffix(".ref.tsv")
    print(f"Saved {len(tts_data)} utts to {ref_tsv}")
    tts_data[["id", "text"]].to_csv(ref_tsv, sep="\t", index=False, header=False)


# %%
if __name__ == "__main__":
    fire.Fire(proc_jsonl)
