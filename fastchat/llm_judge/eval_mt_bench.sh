#!/bin/bash

set -x
work_dir=dev_data
# model_path=microsoft/Phi-3.5-mini-instruct
# model_id=Phi-3.5-mini-instruct
# echo gen_model_answer.py  --work-dir ${work_dir} --model-path ${model_path} --model-id ${model_id}
# python gen_model_answer.py  --work-dir ${work_dir} --model-path ${model_path} --model-id ${model_id}
models=(
    # gpt-4
    # gpt-3.5-turbo
    Phi-3.5-mini-instruct
    # Phi-Omni_20241009
    # Phi-Omni-Audio_20241010
    # Phi3.5-Omni-audio_20241010
    # Phi3.5-Omni-text_20241010
    # Phi3.5-Omni-text-v0_20241010_221331
    # Phi3.5-Omni-audio-v0_20241010_222909
    Phi3.5-Omni-text-v0b_20241011_192510
    Phi3.5-Omni-audio-v0b_20241011_194120
    )
    

# for model_id in ${models[@]}; do
#     python gen_judgment.py --work-dir ${work_dir} --model-list $model_id --judge-model gpt-4
# done

# https://speechinsightseus.blob.core.windows.net/automatedinsights-prod/mt/bench/whisper/small/en-US/16b84634-ebf3-465c-a692-12ea7c015a15/UtteranceDetails_NonDisfluency_TER.html?skoid=1538c72b-dd4c-420b-b3a4-f23f07fd6a02&sktid=72f988bf-86f1-41af-91ab-2d7cd011db47&skt=2024-10-14T18%3A54%3A00Z&ske=2024-10-16T18%3A54%3A00Z&sks=b&skv=2024-05-04&sv=2024-05-04&spr=https&st=2024-10-14T18%3A54%3A00Z&se=2024-10-16T18%3A54%3A00Z&sr=c&sp=rl&sig=zeAsF0S5AJLckYv7kkxLG1nLVrwZ8vIrxEqaGtT54b8%3D
exclude_questions=(
                116
                117
                120
                124
                139
                140
)
python show_result.py --work-dir ${work_dir} --model-list  ${models[@]} --exclude ${exclude_questions[@]}

python qa_browser.py --work-dir ${work_dir} --share