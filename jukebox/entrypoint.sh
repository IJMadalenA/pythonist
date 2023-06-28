#!/bin/bash

pip install torch

python sample.py --model=5b_lyrics --name=sample_5b \
        --levels=3 --sample_length_in_seconds=20 \
        --total_sample_length_in_seconds=180 \
        --sr=44100 --n_samples=6 \
        --hop_fraction=0.5,0.5,0.125
