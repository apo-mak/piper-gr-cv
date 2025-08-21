#!/usr/bin/env python3
"""
Convert filtered Common Voice TSV data to Piper training CSV format.
This script converts the male-filtered Common Voice data to the CSV format required by Piper:
filename.wav|Text content
"""

import csv
import os
from pathlib import Path

def convert_tsv_to_piper_csv(tsv_file, output_csv, audio_dir):
    """
    Convert Common Voice TSV to Piper training CSV format.
    
    Args:
        tsv_file: Path to input TSV file
        output_csv: Path to output CSV file
        audio_dir: Directory containing audio files
    """
    entries = []
    skipped_count = 0
    
    with open(tsv_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile, delimiter='\t')
        
        for row in reader:
            audio_path = row.get('path', '').strip()
            sentence = row.get('sentence', '').strip()
            
            # Skip if missing essential data
            if not audio_path or not sentence:
                skipped_count += 1
                continue
            
            # Check if audio file exists
            full_audio_path = os.path.join(audio_dir, audio_path)
            if not os.path.exists(full_audio_path):
                print(f"Warning: Audio file not found: {audio_path}")
                skipped_count += 1
                continue
            
            # Format: filename|text
            entries.append(f"{audio_path}|{sentence}")
    
    # Write to CSV (actually pipe-delimited text file)
    with open(output_csv, 'w', encoding='utf-8') as outfile:
        for entry in entries:
            outfile.write(entry + '\n')
    
    print(f"Converted {tsv_file}:")
    print(f"  - {len(entries)} entries written to {output_csv}")
    print(f"  - {skipped_count} entries skipped")
    
    return len(entries)

def main():
    # Base directories
    base_dir = Path("./voice_data/cv-corpus-22.0-2025-06-20/el/male_filtered")
    audio_dir = base_dir / "clips"
    output_dir = Path("./training_data")
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Files to convert
    conversions = [
        {
            'tsv': base_dir / "male_train.tsv",
            'csv': output_dir / "train.csv",
            'description': "Training data"
        },
        {
            'tsv': base_dir / "male_dev.tsv", 
            'csv': output_dir / "dev.csv",
            'description': "Development/validation data"
        },
        {
            'tsv': base_dir / "male_test.tsv",
            'csv': output_dir / "test.csv", 
            'description': "Test data"
        },
        {
            'tsv': base_dir / "male_validated.tsv",
            'csv': output_dir / "validated.csv",
            'description': "Additional validated data"
        }
    ]
    
    print("Converting Common Voice TSV to Piper CSV format...")
    print("=" * 60)
    
    total_entries = 0
    
    for conversion in conversions:
        if conversion['tsv'].exists():
            print(f"\n{conversion['description']}:")
            entries_count = convert_tsv_to_piper_csv(
                conversion['tsv'], 
                conversion['csv'],
                audio_dir
            )
            total_entries += entries_count
        else:
            print(f"File not found: {conversion['tsv']}")
    
    print("\n" + "=" * 60)
    print(f"Total entries converted: {total_entries}")
    print(f"Output directory: {output_dir}")
    
    # Create a combined training file (train + validated for more data)
    combined_csv = output_dir / "train_combined.csv"
    print(f"\nCreating combined training file: {combined_csv}")
    
    combined_entries = 0
    with open(combined_csv, 'w', encoding='utf-8') as outfile:
        # Add training data
        train_csv = output_dir / "train.csv"
        if train_csv.exists():
            with open(train_csv, 'r', encoding='utf-8') as infile:
                for line in infile:
                    outfile.write(line)
                    combined_entries += 1
        
        # Add validated data
        validated_csv = output_dir / "validated.csv"
        if validated_csv.exists():
            with open(validated_csv, 'r', encoding='utf-8') as infile:
                for line in infile:
                    outfile.write(line)
                    combined_entries += 1
    
    print(f"Combined training file created with {combined_entries} entries")
    
    # Display sample entries
    print("\nSample entries from train.csv:")
    train_csv = output_dir / "train.csv"
    if train_csv.exists():
        with open(train_csv, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i < 3:  # Show first 3 entries
                    print(f"  {line.strip()}")
                else:
                    break
    
    print("\nFiles ready for Piper training:")
    print(f"  - Audio directory: {audio_dir}")
    print(f"  - Training CSV: {output_dir}/train.csv")
    print(f"  - Validation CSV: {output_dir}/dev.csv") 
    print(f"  - Test CSV: {output_dir}/test.csv")
    print(f"  - Combined training CSV: {output_dir}/train_combined.csv")

if __name__ == "__main__":
    main()
