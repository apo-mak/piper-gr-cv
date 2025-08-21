# Greek Common Voice Dataset - Male Voice Filtering Report

## Overview
The Greek Common Voice dataset has been successfully filtered to include only male voices (speakers with `gender='male_masculine'`).

## Original Dataset Location
- Source: `/voice_data/cv-corpus-22.0-2025-06-20/el/`
- Language: Greek (el)

## Filtered Dataset Location
- Output: `/voice_data/cv-corpus-22.0-2025-06-20/el/male_filtered/`

## Dataset Statistics

### Male Voice Distribution by Dataset Split:
- **Training set** (`male_train.tsv`): 1,686 entries
- **Development set** (`male_dev.tsv`): 816 entries  
- **Test set** (`male_test.tsv`): 562 entries
- **Validated set** (`male_validated.tsv`): 12,717 entries
- **Other set** (`male_other.tsv`): 4,333 entries
- **Invalidated set** (`male_invalidated.tsv`): 634 entries

### Total Male Voice Clips: **17,631 unique audio files**

## Filtered Dataset Structure
```
male_filtered/
├── male_train.tsv          # Male voices from training set
├── male_dev.tsv            # Male voices from development set  
├── male_test.tsv           # Male voices from test set
├── male_validated.tsv      # Male voices from validated set
├── male_other.tsv          # Male voices from other set
├── male_invalidated.tsv    # Male voices from invalidated set
├── clips/                  # Audio files (17,631 .mp3 files)
├── clip_durations.tsv      # Duration metadata (copied as-is)
├── reported.tsv            # Reported issues (copied as-is)
├── unvalidated_sentences.tsv # Unvalidated sentences (copied as-is)
└── validated_sentences.tsv # Validated sentences (copied as-is)
```

## Data Quality Notes
- All filtered entries have `gender='male_masculine'`
- Audio files are in MP3 format
- Each entry includes:
  - `client_id`: Anonymized speaker ID
  - `path`: Audio file name
  - `sentence_id`: Unique sentence identifier
  - `sentence`: Greek text to be spoken
  - `up_votes`/`down_votes`: Quality ratings
  - `age`: Speaker age group (when available)
  - `gender`: Set to 'male_masculine' for all entries
  - `locale`: Set to 'el' (Greek)

## Next Steps for Piper Training
1. Use the `male_train.tsv` file as your primary training dataset (1,686 samples)
2. Use `male_dev.tsv` for validation during training (816 samples)
3. Use `male_test.tsv` for final evaluation (562 samples)
4. Consider using `male_validated.tsv` for additional training data if needed (12,717 samples)

## Recommended Training Split
- **Primary training**: `male_train.tsv` (1,686 samples)
- **Validation**: `male_dev.tsv` (816 samples)
- **Testing**: `male_test.tsv` (562 samples)
- **Additional training** (if needed): `male_validated.tsv` (12,717 samples)

The filtered dataset is now ready for Piper voice model training with a consistent male voice profile.
