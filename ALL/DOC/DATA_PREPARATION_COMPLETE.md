#  Greek Male Voice Training - Data Preparation 


### 1. Dataset Filtering Complete
- **Started with**: Mozilla Common Voice Greek dataset (~20K+ clips, mixed gender)
- **Filtered to**: 17,631 male voice clips (`gender='male_masculine'`)
- **Quality**: High-quality validated audio with text transcriptions

### 2. Format Conversion Complete  
- **Converted from**: Common Voice TSV format
- **Converted to**: Piper training CSV format with `|` delimiter
- **Format**: `filename.mp3|Greek text content`
- **Total training samples**: 14,403 (combined dataset)

### 3. Training Files Ready
📁 **Training Data Structure:**
```
/local/training_data/
├── train_combined.csv    # 14,403 samples (RECOMMENDED for training)
├── dev.csv              # 816 samples (for validation)  
├── test.csv             # 562 samples (for testing)
├── train.csv            # 1,686 samples (original train split)
└── validated.csv        # 12,717 samples (additional data)
```

📁 **Audio Files:**
```
/local/voice_data/cv-corpus-22.0-2025-06-20/el/male_filtered/clips/
└── 17,631 MP3 files (male voices only)
```

### 4. Training Scripts Ready
- **Training script**: `train_greek_voice.sh` (executable)
- **Configuration**: Pre-configured for Greek (`el`) with optimal settings
- **Documentation**: Complete training guide in `GREEK_VOICE_TRAINING_GUIDE.md`

## 🚀 Next Steps - Ready to Train!

### Quick Start Training:
```bash
# 1. Activate environment
source .venv/bin/activate

# 2. Install dependencies (if not done)
python3 -m pip install -e .[train]
./build_monotonic_align.sh
python3 setup.py build_ext --inplace

# 3. Start training
cd local
./train_greek_voice.sh
```

### Training Configuration:
- **Voice name**: `greek_male_cv`
- **Language**: Greek (`el`)
- **Sample rate**: 22,050 Hz
- **Training data**: 14,403 male voice samples
- **Validation data**: 816 samples
- **Expected training time**: 2-8 hours (with checkpoint), 12-24 hours (from scratch)

## 📊 Dataset Statistics

| Metric | Value |
|--------|--------|
| **Total male audio clips** | 17,631 |
| **Training samples** | 14,403 |
| **Validation samples** | 816 |
| **Test samples** | 562 |
| **Language** | Greek (el) |
| **Gender** | Male only |
| **Audio format** | MP3 |
| **Text encoding** | UTF-8 Greek |

## 🎯 Training Goals
After training completion, you'll have:
- `el_GR-male_cv-medium.onnx` - Trained Greek male voice model
- `el_GR-male_cv-medium.onnx.json` - Model configuration
- Ready-to-use TTS model for Greek text synthesis

## 🔧 Files Created
- ✅ `filter_male_voices.py` - Dataset filtering script
- ✅ `convert_to_piper_format.py` - Format conversion script  
- ✅ `train_greek_voice.sh` - Training execution script
- ✅ `GREEK_VOICE_TRAINING_GUIDE.md` - Complete training guide
- ✅ `MALE_VOICE_FILTERING_REPORT.md` - Filtering process report

---

**Status**: 🟢 **READY TO TRAIN** - All data preparation steps complete!

**Command to start training**: `cd local && ./train_greek_voice.sh`
