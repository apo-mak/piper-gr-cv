#!/bin/bash
# Piper Greek Male Voice Training Script (Local Version)
# This script sets up and runs the training for a Greek male voice using the filtered Common Voice dataset
# Run this script from the 'local' directory: cd local && ./train_greek_voice_local.sh

set -e  # Exit on any error

# Configuration
VOICE_NAME="greek_male_cv"
ESPEAK_VOICE="el"  # Greek language code for espeak-ng
SAMPLE_RATE=22050
BATCH_SIZE=32

# Check if we're in the local directory
if [ ! -d "voice_data" ] || [ ! -d "training_data" ]; then
    echo "ERROR: This script must be run from the 'local' directory"
    echo "Usage: cd local && ./train_greek_voice_local.sh"
    exit 1
fi

# Paths (relative to local directory)
AUDIO_DIR="./voice_data/cv-corpus-22.0-2025-06-20/el/male_filtered/clips"
TRAINING_DATA_DIR="./training_data"
CACHE_DIR="./cache"
OUTPUT_DIR="./output"

# Training files
TRAIN_CSV="${TRAINING_DATA_DIR}/train_combined.csv"  # Using combined dataset for more data
DEV_CSV="${TRAINING_DATA_DIR}/dev.csv"
CONFIG_PATH="${OUTPUT_DIR}/${VOICE_NAME}.json"

# Create necessary directories
mkdir -p "${CACHE_DIR}"
mkdir -p "${OUTPUT_DIR}"

echo "=== Piper Greek Male Voice Training (Local) ==="
echo "Voice name: ${VOICE_NAME}"
echo "Training data: ${TRAIN_CSV}"
echo "Validation data: ${DEV_CSV}"
echo "Audio directory: ${AUDIO_DIR}"
echo "Cache directory: ${CACHE_DIR}"
echo "Output directory: ${OUTPUT_DIR}"
echo

# Verify files exist
if [ ! -f "${TRAIN_CSV}" ]; then
    echo "ERROR: Training CSV not found: ${TRAIN_CSV}"
    exit 1
fi

if [ ! -f "${DEV_CSV}" ]; then
    echo "ERROR: Development CSV not found: ${DEV_CSV}"
    exit 1
fi

if [ ! -d "${AUDIO_DIR}" ]; then
    echo "ERROR: Audio directory not found: ${AUDIO_DIR}"
    exit 1
fi

echo "All files verified. Starting training..."
echo

# Check if virtual environment is activated
if [ -z "${VIRTUAL_ENV}" ]; then
    echo "WARNING: No virtual environment detected. Make sure you have activated the Piper training environment."
    echo "Run: cd .. && source .venv/bin/activate && cd local"
    echo
fi

# Verify GPU is available before training
echo "Checking GPU availability..."
python3 -c "
import torch
print(f'PyTorch version: {torch.__version__}')
print(f'CUDA available: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'CUDA device: {torch.cuda.get_device_name(0)}')
    print(f'CUDA memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB')
    print(f'Current GPU memory allocated: {torch.cuda.memory_allocated(0) / 1e9:.2f} GB')
"

# Training command
echo "Running Piper training command with GPU..."
echo "Monitor GPU usage in another terminal with: watch -n 1 nvidia-smi"
echo
python3 -m piper.train fit \
    --data.voice_name "${VOICE_NAME}" \
    --data.csv_path "${TRAIN_CSV}" \
    --data.audio_dir "${AUDIO_DIR}" \
    --model.sample_rate ${SAMPLE_RATE} \
    --data.espeak_voice "${ESPEAK_VOICE}" \
    --data.cache_dir "${CACHE_DIR}" \
    --data.config_path "${CONFIG_PATH}" \
    --data.batch_size ${BATCH_SIZE} \
    --trainer.max_epochs 1000 \
    --trainer.check_val_every_n_epoch 5 \
    --trainer.log_every_n_steps 100 \
    --data.validation_split 0.1 \
    --trainer.accelerator gpu \
    --trainer.devices 1 \
    --trainer.strategy auto



echo
echo "Training completed!"
echo "Config file written to: ${CONFIG_PATH}"
echo "Model checkpoints saved in: lightning_logs/"
echo
echo "To export the model to ONNX format, run:"
echo "python3 -m piper.train.export_onnx --checkpoint lightning_logs/version_X/checkpoints/checkpoint.ckpt --output-file ${OUTPUT_DIR}/${VOICE_NAME}.onnx"
