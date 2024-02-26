# Author: Andrew Higgins
# https://github.com/speckly

import os

def count_files(directory):
    try:
        positive_count = negative_count = placeholder_count = neutral_count = 0

        for file_name in os.listdir(directory):
            if file_name.endswith(('.jpg', '.jpeg')):
                f = file_name.lower()
                if "positive" in f:
                    positive_count += 1
                elif "negative" in f:
                    negative_count += 1
                elif "xxxxxxxx" in f:
                    placeholder_count += 1
                elif "ummmmmmm" in f:
                    neutral_count += 1

        total_files = len(os.listdir(directory))
        unaccounted_files = total_files - positive_count - negative_count - placeholder_count - neutral_count
        total_labeled = positive_count+negative_count
        accuracy = positive_count/total_labeled*100 if total_labeled != 0 else 0
        ex_accuracy = (positive_count+neutral_count)/total_labeled*100 if total_labeled != 0 else 0

        result = (
            f"Number of positive images: {positive_count}\n"
            f"Number of negative images: {negative_count}\n"
            f"Number of ummmmmmm images (neutral, review again): {neutral_count}\n"
            f"Number of unlabelled images (placeholder): {placeholder_count}\n"
            f"Unaccounted images: {unaccounted_files}\n"
            f"Total number of files: {total_files}\n"
            f"**Accuracy**: {accuracy:.2f}%\n"
            f"Ex-Accuracy (including neutral): {ex_accuracy:.2f}%"
        )

        return result

    except FileNotFoundError:
        return f"Directory not found: {directory}"

if __name__ == "__main__":
    directory_path = './images/catgirls-21-genesis'
    print(count_files(directory_path))
    
