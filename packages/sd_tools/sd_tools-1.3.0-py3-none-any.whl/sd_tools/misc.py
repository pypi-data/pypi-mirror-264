import torch
import json
import struct
from argparse import ArgumentParser
from safetensors.torch import save_file
import operator as op
from functools import reduce

def pt2st():

    parser = ArgumentParser('pt to safetensors')
    parser.add_argument('--input', '-i', type=str)
    parser.add_argument('--output', '-o', type=str)
    args = parser.parse_args()

    save_file(torch.load(args.input), args.output)

def st_inspect():

    parser = ArgumentParser('safetensor inspect')
    parser.add_argument('file', type=str)
    args = parser.parse_args()

    with open(args.file, 'rb') as f:
        files = json.loads(f.read(struct.unpack('<Q', f.read(8))[0]).decode())
        for k, v in files.items():
            if not v.get('shape'): continue
            print(k, reduce(op.mul, v['shape'], 1), 'x'.join(map(str, v['shape'])))

def to_fp16():

    parser = ArgumentParser('save model as fp16')
    parser.add_argument('model', type=str)
    parser.add_argument('output', type=str)
    args = parser.parse_args()

    from diffusers import AutoPipelineForText2Image
    pipe = AutoPipelineForText2Image.from_pretrained(args.model, torch_dtype=torch.float16)

    pipe.save_pretrained(args.output, variant='fp16')
