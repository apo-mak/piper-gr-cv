#!/usr/bin/env python3
"""
Filter Common Voice dataset to include only male voices.
This script processes the Greek Common Voice dataset and creates filtered versions
containing only male voices (gender='male_masculine').
"""

import os
import csv
import shutil
from pathlib import Path

def filter_tsv_for_male_voices(input_file, output_file, clips_dir=None):
    """
    Filter a TSV file to include only entries with male voices.
    
    Args:
        input_file: Path to input TSV file
        output_file: Path to output TSV file
        clips_dir: Optional path to clips directory for copying audio files
    """
    male_clips = []
    
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile, delimiter='\t')
        
        # Read header
        fieldnames = reader.fieldnames
        
        # Filter rows for male voices
        for row in reader:
            if row.get('gender') == 'male_masculine':
                male_clips.append(row)
    
    # Write filtered data
    with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        writer.writerows(male_clips)
    
    print(f"Filtered {input_file}: {len(male_clips)} male voice entries -> {output_file}")
    return [clip['path'] for clip in male_clips if 'path' in clip]

def copy_audio_files(clip_paths, source_clips_dir, target_clips_dir):
    """
    Copy audio files for filtered clips.
    
    Args:
        clip_paths: List of audio file paths
        source_clips_dir: Source clips directory
        target_clips_dir: Target clips directory
    """
    os.makedirs(target_clips_dir, exist_ok=True)
    copied_count = 0
    
    for clip_path in clip_paths:
        source_path = os.path.join(source_clips_dir, clip_path)
        target_path = os.path.join(target_clips_dir, clip_path)
        
        if os.path.exists(source_path):
            shutil.copy2(source_path, target_path)
            copied_count += 1
        else:
            print(f"Warning: Audio file not found: {source_path}")
    
    print(f"Copied {copied_count} audio files to {target_clips_dir}")

def main():
    # Base directories
    base_dir = Path("./voice_data/cv-corpus-22.0-2025-06-20/el")
    output_dir = base_dir / "male_filtered"
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Files to process (those that contain actual data entries)
    tsv_files_to_filter = ['train.tsv', 'dev.tsv', 'test.tsv', 'validated.tsv', 'other.tsv', 'invalidated.tsv']
    
    all_male_clips = set()
    
    print("Filtering TSV files for male voices...")
    print("=" * 50)
    
    # Process each TSV file
    for tsv_file in tsv_files_to_filter:
        input_path = base_dir / tsv_file
        output_path = output_dir / f"male_{tsv_file}"
        
        if input_path.exists():
            male_clips = filter_tsv_for_male_voices(input_path, output_path)
            all_male_clips.update(male_clips)
        else:
            print(f"File not found: {input_path}")
    
    print("\n" + "=" * 50)
    print(f"Total unique male voice clips: {len(all_male_clips)}")
    
    # Copy audio files
    if all_male_clips:
        print("\nCopying audio files...")
        source_clips_dir = base_dir / "clips"
        target_clips_dir = output_dir / "clips"
        
        if source_clips_dir.exists():
            copy_audio_files(list(all_male_clips), source_clips_dir, target_clips_dir)
        else:
            print(f"Warning: Source clips directory not found: {source_clips_dir}")
    
    # Copy other files that don't need filtering
    other_files = ['clip_durations.tsv', 'reported.tsv', 'unvalidated_sentences.tsv', 'validated_sentences.tsv']
    
    print("\nCopying other metadata files...")
    for file_name in other_files:
        source_path = base_dir / file_name
        target_path = output_dir / file_name
        
        if source_path.exists():
            shutil.copy2(source_path, target_path)
            print(f"Copied: {file_name}")
    
    print(f"\nFiltered dataset created in: {output_dir}")
    print("\nSummary of filtered files:")
    print("- Male-only TSV files with 'male_' prefix")
    print("- Corresponding audio files in clips/ directory")
    print("- Original metadata files copied as-is")

if __name__ == "__main__":
    main()
