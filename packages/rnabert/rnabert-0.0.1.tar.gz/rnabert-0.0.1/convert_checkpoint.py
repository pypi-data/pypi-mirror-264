import sys
from typing import Optional

import chanfig
import torch

from rnabert import RnaBertConfig, RnaBertModel

vocab_list = [
    "<pad>",
    "<mask>",
    "A",
    "U",
    "G",
    "C",
]


def convert_checkpoint(checkpoint_path: str, output_path: Optional[str] = None):
    if output_path is None:
        output_path = "rnabert"
    config = RnaBertConfig.from_dict(chanfig.load("config.json"))
    config.vocab_list = vocab_list
    ckpt = torch.load(checkpoint_path)
    bert_state_dict = ckpt
    state_dict = {}

    model = RnaBertModel(config)

    for key, value in bert_state_dict.items():
        if key.startswith("module.cls"):
            continue
        key = key[12:]
        key = key.replace("gamma", "weight")
        key = key.replace("beta", "bias")
        state_dict[key] = value

    model.load_state_dict(state_dict)
    model.save_pretrained(output_path)


if __name__ == "__main__":
    convert_checkpoint(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
