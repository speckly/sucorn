# Author: Andrew Higgins
# https://github.com/speckly

import os
import csv
import re

def count_files(directory, export_csv=False):
    try:
        positive_count = negative_count = unlabelled = neutral_count = 0

        positive_dir = os.path.join(directory, "positive")
        negative_dir = os.path.join(directory, "negative")
        neutral_dir = os.path.join(directory, "neutral")

        positive_count = sum(1 for file_name in os.listdir(positive_dir) if file_name.lower().endswith(('.jpg', '.jpeg')))
        negative_count = sum(1 for file_name in os.listdir(negative_dir) if file_name.lower().endswith(('.jpg', '.jpeg')))
        neutral_count = sum(1 for file_name in os.listdir(neutral_dir) if file_name.lower().endswith(('.jpg', '.jpeg')))
        unlabelled = sum(1 for file_name in os.listdir(directory) if file_name.lower().endswith(('.jpg', '.jpeg')))

        total_files = positive_count + negative_count + neutral_count + unlabelled
        total_labeled = positive_count + negative_count + neutral_count

        accuracy = positive_count / total_labeled * 100 if total_labeled != 0 else 0
        ex_accuracy = (positive_count + neutral_count) / total_labeled * 100 if total_labeled != 0 else 0

        # For readability in visualization programs
        # PLEASE DONT PASS IN A PATH WITH THE FORWARDS SLASH IM PRAYING
        directory_name = directory.split("\\")[-1].replace("catgirls", "cg").replace("anime-girls", "ag")

        if export_csv:
            result = {
                "directory": directory_name,
                "positive": positive_count,
                "negative": negative_count,
                "neutral": neutral_count,
                "unlabelled": unlabelled,
                "total": total_files,
                "accuracy": round(accuracy, 4),
                "ex_accuracy": round(ex_accuracy, 4)
            }
        else:  # Omitted the directory as it is passed as a separate argument
            result = (
                f"Number of positive images: {positive_count}\n"
                f"Number of negative images: {negative_count}\n"
                f"Number of neutral images: {neutral_count}\n"
                f"Number of unlabelled images: {unlabelled}\n"
                f"Total number of files: {total_files}\n"
                f"**Accuracy**: {accuracy:.4f}%\n"
                f"Ex-Accuracy (including neutral): {ex_accuracy:.4f}%"
            )

        return result

    except FileNotFoundError:
        return "Skipped as it contains missing subdirectories"

def export_to_csv(file, result):
    with open(file, mode='a', newline='') as csv_file: 
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
        df[column] = df[column] / df['total'] * 100
        
    df = df.drop(columns=['total'])
    df.set_index('directory', inplace=True)

    df_combined = df.drop(columns=['accuracy', 'ex_accuracy'])
    df_accuracy = df.drop(columns=['positive', 'negative', 'neutral', 'unlabelled'])

    # fig, axes = plt.subplots(ncols=2, figsize=(18, 10))
    # ax=axes[x,y]
    # df.plot(kind='bar', title="Bar Plot")
    # df.plot(kind='line', ax=axes[0, 1], title="Line Plot")
    # plt.xticks(rotation=45)
    colors = ['green', 'red', 'blue', 'purple']
    ax = df_combined.plot(kind='bar', stacked=True, title="Type of labels", color=colors)
    ax.legend(loc='center', bbox_to_anchor=(1, 1))

    ax = df_accuracy.plot(kind='line', title="Accuracy")
    ax.legend(loc='center', bbox_to_anchor=(1, 1))

    plt.xticks(rotation=45)

    # df_combined.plot(kind='area', stacked=True, title="Area Plot")
    # df.plot(kind='scatter', x='ex_accuracy', y='accuracy', ax=axes[1, 0], title="Scatter Plot for accuracy")
    # df.plot(kind='hist', bins=10, ax=axes[1, 1], title="Histogram")
    # df['accuracy'].plot(kind='pie', autopct='%1.1f%%', ax=axes[1, 2], title="Pie Chart")

    # plt.xticks(rotation=45)
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
            if file:
                with open(file, mode='w', newline='') as csv_file: # Clear
                    csv_file.write("")
            di = sorted(os.listdir(f"{DIRECTORY}\..\images"), key=lambda x: int(x.split('-')[-1]) if x.split('-')[-1].isdigit() else float('inf'))
            print(di)
            for folder in di:
                if file:
                    result = count_files(f'{DIRECTORY}\..\images\{folder}', export_csv=True)
                    if result == "Skipped as it contains missing subdirectories":
                        print(f"{folder} has been skipped as it contains missing subdirectories")
                        continue

                    export_to_csv(file, result)
                    print(f"Results for {folder} exported to CSV file: {file}")
                else:
                    result = count_files(f'{DIRECTORY}\..\images\{folder}')
                    print(f"{folder}\n{result}", end="\n\n")