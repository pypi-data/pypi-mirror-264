<div align="center">

# OpenBB Chat

<p align="center">
  <!-- X Badge -->
  <a href="https://twitter.com/GPTStonks"><img src="https://img.shields.io/badge/follow_us-000000?logo=x&logoColor=white" alt="X Follow Us Badge"></a>
  <!-- Discord Badge -->
  <a href="https://discord.gg/MyDDGuEd"><img src="https://img.shields.io/badge/Discord-5865F2?logo=discord&logoColor=white" alt="Discord Badge"></a>
  <!-- Docker Badge -->
  <a href="https://hub.docker.com/u/gptstonks">
    <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white" alt="Docker Badge">
  </a>
</p>
<p align="center">
    <a href="https://pytorch.org/get-started/locally/"><img alt="PyTorch" src="https://img.shields.io/badge/PyTorch-ee4c2c?logo=pytorch&logoColor=white"></a>
    <a href="https://pytorchlightning.ai/"><img alt="Lightning" src="https://img.shields.io/badge/-Lightning-792ee5?logo=pytorchlightning&logoColor=white"></a>
    <a href="https://hydra.cc/"><img alt="Config: Hydra" src="https://img.shields.io/badge/Config-Hydra-89b8cd"></a>
    <a href="https://huggingface.co/"><img alt="Models: HuggingFace" src="https://img.shields.io/badge/Models-HuggingFace-ffd21e"></a>
</p>

</div>

## Description

OpenBB Chat provides chat capabilities to [OpenBB](https://github.com/OpenBB-finance/OpenBBTerminal) by leveraging the generative potential of LLMs. The chat is implemented following [InstructGPT](https://openai.com/research/instruction-following). This repository contains the implementations of the NLP models and the training/inference infraestructure.

## Installation

#### PDM

```bash
# clone project
git clone https://github.com/Dedalo314/openbb-chat
cd openbb-chat

# install pdm
pip install pdm

# install package
pdm install
```

## How to run

Train model with default configuration

```bash
# train demo on CPU
python openbb_chat/train.py trainer=cpu

# train demo on GPU
python openbb_chat/train.py trainer=gpu
```

Train model with chosen experiment configuration from [configs/experiment/](configs/experiment/)

```bash
python openbb_chat/train.py experiment=experiment_name.yaml
```

You can override any parameter from command line like this

```bash
python openbb_chat/train.py trainer.max_epochs=20 data.batch_size=64
```

## Released models

The model [Griffin-3B-GPTQ](https://huggingface.co/daedalus314/Griffin-3B-GPTQ) has been created as part of this project by quantizing [Griffin-3B](https://huggingface.co/acrastt/Griffin-3B). In the future, more models will be trained and released as needed.

## Sample usage with pre-trained models

In the repository https://github.com/GPTStonks/api `openbb-chat` is used to perform [retrieval-augmented generation](https://arxiv.org/abs/2005.11401) (RAG) with OpenBB's official documentation and pre-trained models. In particular, the `classifiers` modules are used to find the appropriate function in OpenBB and the `llms` modules are used to complete the function call.

## License

The Dockerfile is based on the image `nvidia/cuda`, which states that the following notice must be included: *This software contains source code provided by NVIDIA Corporation.*
