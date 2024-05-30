# Author: Andrew Higgins
# https://github.com/speckly

import os
import csv
import argparse
import pandas as pd
import matplotlib.pyplot as plt

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

        return (
            {
                "directory": directory_name,
                "positive": positive_count,
                "negative": negative_count,
                "neutral": neutral_count,
                "unlabelled": unlabelled,
                "total": total_files,
                "accuracy": round(accuracy, 4),
                "ex_accuracy": round(ex_accuracy, 4),
            }
            if export_csv
            else f"Number of positive images: {positive_count}\nNumber of negative images: {negative_count}\nNumber of neutral images: {neutral_count}\nNumber of unlabelled images: {unlabelled}\nTotal number of files: {total_files}\n**Accuracy**: {accuracy:.4f}%\nEx-Accuracy (including neutral): {ex_accuracy:.4f}%"
        )
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

def visualise(file, main=False, render=True):
    # main flag is so that sucorn bot can display a saved image onto Discord

    # directory,positive,negative,neutral,unlabelled,total,accuracy,ex_accuracy
    df = pd.read_csv(file)
    ticks = list(df['directory'])
    
    # Normalize all numeric columns except the total
    numeric_columns = df.select_dtypes(include='number').columns
    for column in [column for column in numeric_columns if column != "total"]: 
        df[column] = df[column] / df['total'] * 100
   
    df_combined = df.drop(columns=['accuracy', 'ex_accuracy', 'total'])
    df_accuracy = df.drop(columns=['positive', 'negative', 'neutral', 'unlabelled', 'total'])
    df_total = pd.DataFrame({'directory': df['directory'], 'total': df['total']})

    for dataframe in [df, df_combined, df_accuracy, df_total]:
        dataframe.set_index('directory', inplace=True)
    
    colors = ['green', 'red', 'blue', 'gray']
    ax = df_combined.plot(kind='bar', stacked=True, title="Type of labels", color=colors)
    ax.legend(loc='center', bbox_to_anchor=(1, 1))
    plt.xticks(rotation=90)
    if render:
        plt.savefig(f'{DIRECTORY}/../statistics/types.png')

    ax = df_accuracy.plot(kind='line', title="Accuracy")
    ax.legend(loc='center', bbox_to_anchor=(1, 1))
    ax.set_xticks(range(len(ticks)))
    ax.set_xticklabels(ticks)
    plt.xticks(rotation=90)
    if render:
        plt.savefig(f'{DIRECTORY}/../statistics/accuracy.png')

    ax = df_total.plot(kind='line', title="Total files")
    ax.legend(loc='center', bbox_to_anchor=(1,1))
    ax.set_xticks(range(len(ticks)))
    ax.set_xticklabels(ticks)
    plt.xticks(rotation=90)
    if render:
        plt.savefig(f'{DIRECTORY}/../statistics/total.png')
    
    # fig, axes = plt.subplots(ncols=2, figsize=(18, 10))
    # ax=axes[x,y]
    # df.plot(kind='bar', title="Bar Plot")
    # df.plot(kind='line', ax=axes[0, 1], title="Line Plot")
    # plt.xticks(rotation=45)

    # df_combined.plot(kind='area', stacked=True, title="Area Plot")
    # df.plot(kind='scatter', x='ex_accuracy', y='accuracy', ax=axes[1, 0], title="Scatter Plot for accuracy")
    # df.plot(kind='hist', bins=10, ax=axes[1, 1], title="Histogram")
    # df['accuracy'].plot(kind='pie', autopct='%1.1f%%', ax=axes[1, 2], title="Pie Chart")
    if main:
        plt.show()

DIRECTORY = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Image Labeling Program')
    parser.add_argument('--folder_name', type=str, help='Folder name of images')
    parser.add_argument('--csv', type=str, help='CSV file name')
    parser.add_argument('--mode', choices=['read', 'write'], default='read', help='Operation mode (read or write)')
    parser.add_argument('--no-save', action='store_true', help='Disable rendering and saving of image to /statistics')
    args = parser.parse_args()
    file = args.csv
    no_save = args.no_save

    if not no_save and not os.path.exists(f'{DIRECTORY}\..\statistics'):
        os.makedirs(f'{DIRECTORY}/../statistics')
        print("Created folder ../statistics")
    if args.folder_name:  # For one folder
        if file:
            result = count_files(f'{DIRECTORY}/../images/{args.folder_name}', export_csv=True)
            export_to_csv(file, result)
            print(f"Results exported to CSV file: {file}")
        else:
            result = count_files(f'{DIRECTORY}/../images/{args.folder_name}')
            print(result)
    elif file and args.mode == 'read':  # Display table if the mode is 'r'
        if os.path.exists(file):
            visualise(file, main=True, render=not no_save)
        else:
            print("File does not exist")
    else:
        if file:
            with open(file, mode='w', newline='') as csv_file: # Clear
                csv_file.write("")
        di = sorted(os.listdir(f"{DIRECTORY}/../images"), key=lambda x: int(x.split('-')[-1]) if x.split('-')[-1].isdigit() else float('inf'))

        for folder in di:
            if file:
                result = count_files(f'{DIRECTORY}/../images/{folder}', export_csv=True)
                if result == "Skipped as it contains missing subdirectories":
                    print(f"{folder} has been skipped as it contains missing subdirectories")
                    continue

                export_to_csv(file, result)
                print(f"Results for {folder} exported to CSV file: {file}")
            else:
                result = count_files(f'{DIRECTORY}/../images/{folder}')
                print(f"{folder}\n{result}", end="\n\n")