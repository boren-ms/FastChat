#!/bin/bash

set -x
work_dir=dev_data
# model_path=microsoft/Phi-3.5-mini-instruct
# model_id=Phi-3.5-mini-instruct
# echo gen_model_answer.py  --work-dir ${work_dir} --model-path ${model_path} --model-id ${model_id}
# python gen_model_answer.py  --work-dir ${work_dir} --model-path ${model_path} --model-id ${model_id}
base_models=(
    gpt-4
    gpt-3.5-turbo
    Phi-3.5-mini-instruct
    )
new_models=(
    # Phi-Omni_20241009
    # Phi-Omni-Audio_20241010
    Phi3.5-Omni-text_20241010
    Phi3.5-Omni-speech_20241010
    )
    
models=(${base_models[@]} ${new_models[@]})

for model_id in ${new_models[@]}; do
    python gen_judgment.py --work-dir ${work_dir} --model-list $model_id --judge-model gpt-4
done

python show_result.py --work-dir ${work_dir} --model-list  ${models[@]}

python qa_browser.py --work-dir ${work_dir} --share