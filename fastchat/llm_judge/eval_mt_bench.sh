#!/bin/bash

set -x
model_path=microsoft/Phi-3.5-mini-instruct
model_id=Phi-3.5-mini-instruct
python gen_model_answer.py --model-path ${model_path} --model-id ${model_id}

# export OPENAI_API_KEY=XXXXXX  # set the OpenAI API key
# python gen_judgment.py --model-list [LIST-OF-MODEL-ID] --parallel [num-concurrent-api-call]


  python show_result.py
  --judgment_dir 