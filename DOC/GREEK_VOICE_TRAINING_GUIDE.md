# Greek Male Voice Training Guide for Piper

## Overview
This guide covers the complete process of training a Greek male voice model using the filtered Common Voice dataset with Piper TTS.

## Dataset Preparation ✅ COMPLETED

### 1. Original Dataset
- **Source**: Mozilla Common Voice v22.0 Greek dataset
- **Location**: `/voice_data/cv-corpus-22.0-2025-06-20/el/`
- **Total original clips**: ~20,000+ (mixed gender)

### 2. Male Voice Filtering ✅
- **Filtered for**: `gender='male_masculine'` only
- **Output location**: `/voice_data/cv-corpus-22.0-2025-06-20/el/male_filtered/`
- **Total male clips**: 17,631 audio files

### 3. Training Format Conversion ✅
Converted to Piper's required CSV format with `|` delimiter:
```
filename.mp3|Greek text content
```

## Training Data Summary

### Available Datasets:
| Dataset | File | Entries | Purpose |
|---------|------|---------|---------|
| Training | `train.csv` | 1,686 | Primary training |
| Development | `dev.csv` | 816 | Validation during training |
| Test | `test.csv` | 562 | Final evaluation |
| Validated | `validated.csv` | 12,717 | Additional training data |
| **Combined** | `train_combined.csv` | **14,403** | **Recommended for training** |

### Recommended Training Split:
- **Training**: `train_combined.csv` (14,403 samples) - combines train + validated
- **Validation**: `dev.csv` (816 samples)
- **Testing**: `test.csv` (562 samples)

## Training Configuration

### Key Parameters:
- **Voice name**: `greek_male_cv`
- **Language**: Greek (`el`)
- **Sample rate**: 22,050 Hz
- **Batch size**: 32
- **espeak-ng voice**: `el` (Greek)

### File Locations:
```
Audio files: /local/voice_data/cv-corpus-22.0-2025-06-20/el/male_filtered/clips/
Training CSV: /local/training_data/train_combined.csv
Validation CSV: /local/training_data/dev.csv
Cache directory: /local/cache/
Output directory: /local/output/
```

## Pre-Training Setup

### 1. Environment Setup
```bash
# Ensure you're in the project directory
cd /piper1-gpl

# Activate virtual environment
source .venv/bin/activate

# Install training dependencies (if not already done)
python3 -m pip install -e .[train]

# Build required extensions
./build_monotonic_align.sh
python3 setup.py build_ext --inplace
```

### 2. Verify espeak-ng
```bash
# Check Greek voice is available
espeak-ng --voices | grep el
# Should show: 5  el  --/M  Greek  grk/el
```

## Training Execution

### Option 1: Using the provided script (Recommended)
```bash
cd /piper1-gpl/local
./train_greek_voice.sh
```

### Option 2: Manual command
```bash
python3 -m piper.train fit \
  --data.voice_name "greek_male_cv" \
  --data.csv_path "/piper1-gpl/local/training_data/train_combined.csv" \
  --data.audio_dir "/piper1-gpl/local/voice_data/cv-corpus-22.0-2025-06-20/el/male_filtered/clips" \
  --model.sample_rate 22050 \
  --data.espeak_voice "el" \
  --data.cache_dir "/piper1-gpl/local/cache" \
  --data.config_path "/piper1-gpl/local/output/greek_male_cv.json" \
  --data.batch_size 32 \
  --trainer.max_epochs 1000 \
  --trainer.check_val_every_n_epoch 5
```

### Optional: Using a pre-trained checkpoint (Recommended)
For faster training, download a checkpoint from [Piper checkpoints](https://huggingface.co/datasets/rhasspy/piper-checkpoints) and add:
```bash
--ckpt_path /path/to/checkpoint.ckpt
```

## Training Monitoring

### Expected Output:
- Training logs in terminal
- Checkpoints saved in `lightning_logs/`
- Config file: `output/greek_male_cv.json`
- Cached phonemes and audio in `cache/`

### Training Time:
- With pre-trained checkpoint: 2-8 hours (depending on hardware)
- From scratch: 12-24+ hours

## Post-Training: Model Export

### 1. Export to ONNX format
```bash
python3 -m piper.train.export_onnx \
  --checkpoint /path/to/best/checkpoint.ckpt \
  --output-file /piper1-gpl/local/output/greek_male_cv.onnx
```

### 2. Rename for compatibility
```bash
# Rename to standard Piper format
mv local/output/greek_male_cv.onnx local/output/el_GR-male_cv-medium.onnx
mv local/output/greek_male_cv.json local/output/el_GR-male_cv-medium.onnx.json
```

## Testing the Model

### Test synthesis
```bash
echo "Γεια σας, αυτή είναι μια δοκιμή." | python3 -m piper \
  --model local/output/el_GR-male_cv-medium.onnx \
  --output-file test_output.wav
```

## Troubleshooting

### Common Issues:
1. **CUDA out of memory**: Reduce `--data.batch_size` (try 16 or 8)
2. **File not found errors**: Check all file paths are correct
3. **espeak-ng errors**: Ensure Greek language support is installed
4. **Slow training**: Use a pre-trained checkpoint with `--ckpt_path`

### Hardware Requirements:
- **Minimum**: 8GB RAM, 4GB disk space
- **Recommended**: 16GB RAM, GPU with 6GB+ VRAM, 10GB disk space

## Files Generated
After successful training, you'll have:
- `el_GR-male_cv-medium.onnx` - The trained voice model
- `el_GR-male_cv-medium.onnx.json` - Model configuration
- `lightning_logs/` - Training checkpoints and logs
- `cache/` - Preprocessed training data

The voice model is now ready for use with Piper TTS!
