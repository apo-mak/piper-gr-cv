# 📁 Local Directory Structure - Updated Paths Reference

## Overview
All training-related files have been moved to the `/local` directory for better organization. This document provides the updated paths and usage instructions.

## 📂 Directory Structure
```
piper1-gpl/
├── local/                                    # ← All training files moved here
│   ├── voice_data/
│   │   ├── cv-corpus-22.0-2025-06-20/
│   │   │   └── el/
│   │   │       └── male_filtered/
│   │   │           ├── clips/               # 17,631 male voice audio files
│   │   │           ├── male_train.tsv
│   │   │           ├── male_dev.tsv
│   │   │           ├── male_test.tsv
│   │   │           └── male_validated.tsv
│   │   ├── filter_male_voices.py
│   │   └── MALE_VOICE_FILTERING_REPORT.md
│   ├── training_data/
│   │   ├── train_combined.csv              # 14,403 samples (RECOMMENDED)
│   │   ├── dev.csv                         # 816 samples
│   │   ├── test.csv                        # 562 samples
│   │   ├── train.csv                       # 1,686 samples
│   │   └── validated.csv                   # 12,717 samples
│   ├── convert_to_piper_format.py
│   ├── train_greek_voice_local.sh         # Relative paths version (NEW)
│   ├── GREEK_VOICE_TRAINING_GUIDE.md
│   ├── DATA_PREPARATION_COMPLETE.md
│   └── cache/                             # (created during training)
│   └── output/                            # (created during training)
├── .venv/                                 # Virtual environment (in root)
├── src/                                   # Piper source code
└── ...                                    # Other project files
```

## 🚀 Quick Start Commands

### Method 1: Using Local Script (Recommended)
```bash
# Navigate to project root and activate environment
cd /piper1-gpl
source .venv/bin/activate

# Go to local directory and start training
cd local
./train_greek_voice_local.sh
```

### Method 2: Using Absolute Paths Script
```bash
# From anywhere, with environment activated
cd /piper1-gpl
source .venv/bin/activate
./local/train_greek_voice.sh
```

## 📋 Updated File Paths Reference

### Training Data Files:
- **Combined training CSV**: `./local/training_data/train_combined.csv`
- **Development CSV**: `./local/training_data/dev.csv`
- **Test CSV**: `./local/training_data/test.csv`
- **Audio files**: `./local/voice_data/cv-corpus-22.0-2025-06-20/el/male_filtered/clips/`

### Output Directories:
- **Cache**: `./local/cache/`
- **Output models**: `./local/output/`
- **Training logs**: `./local/lightning_logs/` (created during training)

### Configuration Files:
- **Voice config**: `./local/output/greek_male_cv.json`
- **Final model**: `./local/output/el_GR-male_cv-medium.onnx`

## 🔧 Scripts Available

| Script | Location | Purpose | Usage |
|--------|----------|---------|--------|
| `train_greek_voice_local.sh` | `/local/` | Training with relative paths | `cd local && ./train_greek_voice_local.sh` |
| `train_greek_voice.sh` | `/local/` | Training with absolute paths | `./local/train_greek_voice.sh` |
| `convert_to_piper_format.py` | `/local/` | Convert TSV to CSV format | `python local/convert_to_piper_format.py` |
| `filter_male_voices.py` | `/local/voice_data/` | Filter dataset for male voices | `python local/voice_data/filter_male_voices.py` |

## 📖 Documentation Files

| File | Location | Content |
|------|----------|---------|
| `GREEK_VOICE_TRAINING_GUIDE.md` | `/local/` | Complete training guide |
| `DATA_PREPARATION_COMPLETE.md` | `/local/` | Preparation status summary |
| `MALE_VOICE_FILTERING_REPORT.md` | `/local/voice_data/` | Filtering process details |
| `LOCAL_PATHS_REFERENCE.md` | `/local/` | This file - path reference |

## ⚡ Training Process

1. **Environment Setup** (from project root):
   ```bash
   source .venv/bin/activate
   ```

2. **Start Training** (choose one method):
   ```bash
   # Method A: Local script
   cd local
   ./train_greek_voice_local.sh
   
   # Method B: Absolute paths
   ./local/train_greek_voice.sh
   ```

3. **Monitor Progress**:
   - Logs appear in terminal
   - Checkpoints saved in `./local/lightning_logs/`
   - Config written to `./local/output/greek_male_cv.json`

4. **Export Model**:
   ```bash
   python3 -m piper.train.export_onnx \
     --checkpoint ./local/lightning_logs/version_X/checkpoints/best.ckpt \
     --output-file ./local/output/greek_male_cv.onnx
   ```

## ✅ Status
- ✅ All files moved to `/local` directory
- ✅ All scripts updated with correct paths
- ✅ Documentation updated
- ✅ Both relative and absolute path scripts available
- 🟢 **READY TO TRAIN**

---

**Recommended command**: `cd local && ./train_greek_voice_local.sh`
