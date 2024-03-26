import os
import time
import logging

logging.basicConfig(
  format = '[%(asctime)s] Evalverse {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
  datefmt = '%y/%m/%d %H:%M:%S',
  level = logging.INFO
)

from pathlib import Path
from argparse import ArgumentParser

from .connector import lm_evaluation_harness

class Evaluator:
    def __init__(self):
        self.args = self.get_args()

    def get_args(self):
        parser = ArgumentParser()

        # Common Args
        parser.add_argument("--ckpt_path", type=str, default="upstage/SOLAR-10.7B-Instruct-v1.0")
        parser.add_argument("--output_path", type=str, default=f"{os.getcwd()}/results")
        parser.add_argument("--model_name", type=str, default="SOLAR-10.7B-Instruct-v1.0", help="model name, e.g. HF model or OpenAI API models")
        parser.add_argument("--use_fast_tokenizer", action="store_true", default=False)
        parser.add_argument("--devices", type=str, default="0", help="The size of data parallel.")
        parser.add_argument("--use_flash_attention_2", action="store_true", default=False)

        # lm-evaluation-harness
        parser.add_argument("--batch_size", type=int, default=16)
        parser.add_argument("--use_vllm", action="store_true", default=False)
        parser.add_argument("--gpu_memory_utilization", type=float, default=0.8)
        parser.add_argument("--model_parallel", type=int, default=1, help="The size of model parallel")
        parser.add_argument("--data_parallel", type=int, default=1, help="The size of data parallel")
        parser.add_argument("--load_in_8bit", action="store_true", default=False)
        parser.add_argument("--load_in_4bit", action="store_true", default=False)

        # FastChat
        parser.add_argument("--baselines", type=str, default=None)
        parser.add_argument("--judge_model", type=str, default="gpt-4")
        parser.add_argument("--num_gpus_total", type=int, default=1, help="The total number of GPUs.")
        parser.add_argument("--num_gpus_per_model", type=int, default=1, help="The number of GPUs per model.")
        parser.add_argument("--parallel_api", type=int, default=1, help="The number of concurrent API calls.")
        
        args = parser.parse_args(args=[])

        # update path to work regardless of /
        args.ckpt_path = str(Path(args.ckpt_path))
        args.output_path = str(Path(args.output_path))

        return args

    def run(self, model, benchmark, **kwargs):
        # update args
        args = self.args
        for k, v in kwargs.items():
            if k in args:
                setattr(args, k, v)
                logging.info(f"The value of argument \"{k}\" has been changed to \"{v}\".")
            else:
                logging.warning(f"The argument \"{k}\" does not exist.")
        args.ckpt_path = model
        logging.info(f"Args {vars(args)}")
        
        # h6_en (with lm-evaluation-harness)
        if benchmark=="h6_en":
            task_and_shot = [
                ('arc_challenge', 25),
                # ('hellaswag', 10),
                # ('mmlu', 5),
                # ('truthfulqa_mc2', 0),
                # ('winogrande', 5),
                # ('gsm8k', 5)            
            ]
            for _task_name, _num_fewshot in task_and_shot:
                start_time = time.time()
                #############################################
                cmd = lm_evaluation_harness(
                    model_path=args.ckpt_path,
                    tasks=_task_name,
                    batch_size=args.batch_size,
                    use_vllm=args.use_vllm,
                    gpu_memory_utilization=args.gpu_memory_utilization,
                    tensor_parallel_size=args.model_parallel,
                    data_parallel_size=args.data_parallel,
                    num_fewshot=_num_fewshot,
                    use_fast_tokenizer=args.use_fast_tokenizer,
                    use_flash_attention_2=args.use_flash_attention_2,
                    output_path=args.output_path,
                    load_in_8bit=args.load_in_8bit,
                    load_in_4bit=args.load_in_4bit,
                )
                #############################################
                end_time = time.time()            
                total_min = round((end_time-start_time)/60)
                bench_name = _task_name+'_'+str(_num_fewshot)+'shot'
                logging.info(f"eval_cmd: {cmd}")
                logging.info(f"Done! exec_time: {total_min} min for {bench_name} with {model}")
                