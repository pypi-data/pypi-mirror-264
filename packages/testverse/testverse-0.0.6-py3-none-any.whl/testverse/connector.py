import os
import re

import logging
logging.basicConfig(level=logging.WARNING)


def lm_evaluation_harness(model_path='upstage/SOLAR-10.7B-Instruct-v1.0',
                          tasks='arc_challenge,hellaswag,hendrycks*,truthfulqa_mc2,winogrande,gsm8k',
                          batch_size=16,
                          use_vllm=False,
                          gpu_memory_utilization=0.8,
                          tensor_parallel_size=1,
                          data_parallel_size=1,
                          num_fewshot=0,
                          use_fast_tokenizer=False,
                          use_flash_attention_2=False,
                          load_in_8bit=False,
                          load_in_4bit=False,
                          output_path="../results"):
    model_name = model_path.split('/')[-1]
    task_name = tasks.split('/')[-1]
    output_json_path = os.path.join(output_path, model_name, f"{task_name}_{num_fewshot}.json")
    
    if os.path.exists(output_json_path):
        print(f"The result already exists: {os.path.abspath(output_json_path)}")

    else:
        if use_vllm:
            tokenizer_mode = 'auto' if use_fast_tokenizer else 'slow'
            eval_cmd = f"""
            lm_eval --model vllm \
                --model_args pretrained={model_path},trust_remote_code=True,tensor_parallel_size={tensor_parallel_size},dtype=float16,gpu_memory_utilization={gpu_memory_utilization},data_parallel_size={data_parallel_size},tokenizer_mode={tokenizer_mode} \
                --tasks {tasks} \
                --batch_size {batch_size} \
                --num_fewshot {num_fewshot} \
                --output_path {output_json_path} \
                --limit 10
            """
        else:
            hf_cmd = "lm_eval --model hf"
            model_args = f"pretrained={model_path},trust_remote_code=True,dtype=float16,use_fast_tokenizer={use_fast_tokenizer},use_flash_attention_2={use_flash_attention_2}"

            if data_parallel_size > 1:
                hf_cmd = "accelerate launch -m " + hf_cmd
            if tensor_parallel_size > 1:
                model_args = model_args + ",parallelize=True"
            if load_in_8bit:
                model_args = model_args + ",load_in_8bit=True"
            if load_in_4bit:
                model_args = model_args + ",load_in_4bit=True"

            eval_cmd = f"""
            {hf_cmd} \
                --model_args {model_args}  \
                --tasks {tasks} \
                --batch_size {batch_size} \
                --num_fewshot {num_fewshot} \
                --output_path {output_json_path} \
                --limit 10
            """
        os.system(eval_cmd)
        pretty_cmd = re.sub(r'\s+', ' ', eval_cmd).strip()
        return pretty_cmd