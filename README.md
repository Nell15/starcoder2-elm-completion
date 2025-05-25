# Deep learning project

This projetct is our attempt at creating an elm code completion IA by creating an elm dataset and fine-tuning a Starcoder2 model.


## Contents

This project contains

- `./starcoder_elm_finetuned` a version of the model that was fine-tuned for 68646 steps (took 37 hours !).
- `./starcoder_elm_finetuned_2` a version of the model that was fine-tuned for 3000 steps.
- `parser.py` is used to verify that a given script is a valid elm code. (Has a few bugs)
- `dataset_builder.py`, the script that was used to create our dataset from our elm files which were located in `./data/files/`.
  Our dataset is not provided and you should provide your own if you were to replicate this experiment.
- `fine_tuning.ipynb` is the file containing the scripts for the fine-tuning process.
- `verification.ipynb` contains the script used to verify the generated code samples.
- `test.json` contains the prompts for the verification process.

## Install
This project was developped using Python-3.12.8; most required libraries can be installed using the Python notebooks (.ipynb) using the provided install cells.

These include:
Transformers, datasets, peft, accelerate, bitsandbytes, torch, tqdm and Cuda