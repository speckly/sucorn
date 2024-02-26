# Author: Andrew Higgins
# https://github.com/speckly

import os
import csv
import re

def count_files(directory, export_csv=False):
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
        total_labeled = positive_count + negative_count
        accuracy = positive_count / total_labeled * 100 if total_labeled != 0 else 0
        ex_accuracy = (positive_count + neutral_count) / total_labeled * 100 if total_labeled != 0 else 0

        if export_csv: # PLEASE DONT PASS IN A PATH WITH THE FORWARDS SLASH IM PRAYING
            result = {
                "directory": directory.split("\\")[-1],
                "positive_count": positive_count,
                "negative_count": negative_count,
                "neutral_count": neutral_count,
                "placeholder_count": placeholder_count,
                "unaccounted_files": unaccounted_files,
                "total_files": total_files,
                "accuracy": round(accuracy, 4),
                "ex_accuracy": round(ex_accuracy, 4)
            }
        else: # Omitted the directory as it is passed as a separate argument
            result = (
                f"Number of positive images: {positive_count}\n"
                f"Number of negative images: {negative_count}\n"
                f"Number of ummmmmmm images (neutral, review again): {neutral_count}\n"
                f"Number of unlabelled images (placeholder): {placeholder_count}\n"
                f"Unaccounted images: {unaccounted_files}\n"
                f"Total number of files: {total_files}\n"
                f"**Accuracy**: {accuracy:.4f}%\n"
                f"Ex-Accuracy (including neutral): {ex_accuracy:.4f}%"
            )

        return result

    except FileNotFoundError:
        return f"Directory not found: {directory}"

def export_to_csv(file, result):
    with open(file, mode='a', newline='') as csv_file:  # Change 'w' to 'a' for append mode
        fieldnames = result.keys()
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Check if the file is empty, and write header only if needed
        if csv_file.tell() == 0:
            writer.writeheader()

        writer.writerow(result)

def visualise(file):
    floatRe = re.compile(r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$')
    df = pd.read_csv(file)

    # Normalize all numeric columns based on the 'total_files' column
    numeric_columns = df.select_dtypes(include='number').columns
    for column in numeric_columns:
        df[column] = df[column] / df['total_files'] * 100
        
    df['unlabelled'] = df['placeholder_count'] + df['unaccounted_files']
    df_for_plot = df.drop(columns=['total_files', 'placeholder_count', 'unaccounted_files'])
    df_for_plot.set_index('directory', inplace=True)

    df_for_area_plot = df_for_plot.drop(columns=['accuracy', 'ex_accuracy'])

    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(18, 10))

    df_for_plot.plot(kind='bar', ax=axes[0, 0], title="Bar Plot")
    df_for_plot.plot(kind='line', ax=axes[0, 1], title="Line Plot")
    df_for_area_plot.plot(kind='area', figsize=(10, 6), stacked=False)
    
    df_for_plot.plot(kind='scatter', x='ex_accuracy', y='accuracy', ax=axes[1, 0], title="Scatter Plot for accuracy")
    df_for_plot.plot(kind='hist', bins=10, ax=axes[1, 1], title="Histogram")
    # df_for_plot['accuracy'].plot(kind='pie', autopct='%1.1f%%', ax=axes[1, 2], title="Pie Chart")

    # Adjust layout
    plt.tight_layout()
    # plt.xticks(rotation=45)

    # Show the plot
    plt.show()

if __name__ == "__main__":
    import argparse
    import pandas as pd
    import matplotlib.pyplot as plt

    DIRECTORY = os.path.dirname(os.path.realpath(__file__))

    parser = argparse.ArgumentParser(description='Image Labeling Program')
    parser.add_argument('--folder_name', type=str, help='Folder name of images')
    parser.add_argument('--csv', type=str, help='CSV file name')
    parser.add_argument('--mode', choices=['read', 'write'], default='read', help='Operation mode (read or write)')
    args = parser.parse_args()
    file = args.csv

    if args.folder_name:  # For one folder
        if file:
            result = count_files(f'{DIRECTORY}\..\images\{args.folder_name}', export_csv=True)
            export_to_csv(file, result)
            print(f"Results exported to CSV file: {file}")
        else:
            result = count_files(f'{DIRECTORY}\..\images\{args.folder_name}')
            print(result)
    else:  # Iterate through images folder
        if file and args.mode == 'read':  # Display table if the mode is 'r'
            if os.path.exists(file):
                visualise(file)
            else:
                print("File does not exist")
        else:
            for folder in sorted(os.listdir(f"{DIRECTORY}\..\images"), key=lambda x: int(x.split('-')[-1]) if x.split('-')[-1].isdigit() else float('inf')):
                if file:
                    result = count_files(f'{DIRECTORY}\..\images\{folder}', export_csv=True)
                    export_to_csv(file, result)
                    print(f"Results for {folder} exported to CSV file: {file}")
                else:
                    result = count_files(f'{DIRECTORY}\..\images\{folder}')
                    print(f"{folder}\n{result}", end="\n\n")