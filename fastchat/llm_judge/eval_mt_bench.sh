#!/bin/bash

set -x
model_path=microsoft/Phi-3.5-mini-instruct
model_id=Phi-3.5-mini-instruct
work_dir=dev_data
models=(gpt-4 gpt-3.5-turbo llama-13b $model_id)


# python gen_model_answer.py  --work-dir ${work_dir} --model-path ${model_path} --model-id ${model_id}

# export AZURE_OPENAI_API_KEY=XXXXXX  # set the OpenAI API key
# python gen_judgment.py --work-dir ${work_dir} --model-list $model_id --judge-model gpt-4

python show_result.py --work-dir ${work_dir} --model-list  ${models[@]}

# python qa_browser.py --work-dir ${work_dir} --share