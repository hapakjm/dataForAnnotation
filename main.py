import os
import subprocess
import shlex
import random
import pandas as pd

os.system('cls')
# subprocess.call(shlex.split('pip freeze > requirements.txt'), shell=True)

def rename_files(data_directory):
    for root, dirs, files in os.walk(data_directory, topdown=False):
        root_to_list = root.split('\\')
        if (len(root_to_list) < 5):
            break

        for file in files:
            if file.endswith('.csv'):
                annotation = file.split('_')[0]
                break
            else:
                annotation = ''
        if annotation != '':
            for file in files:
                if file.endswith('.csv'):
                    new_filename = f'{annotation}_{root_to_list[1]}_{root_to_list[2]}_{root_to_list[3]}_{root_to_list[4]}_{file.split('_')[-1]}'
                else:
                    new_filename = f'{annotation}_{root_to_list[1]}_{root_to_list[2]}_{root_to_list[3]}_{root_to_list[4]}.mp4'
                old_path = os.path.join(root, file)
                new_path = os.path.join(root, new_filename)
                os.rename(old_path, new_path)



def shuffle_and_rename_vid_files(data_directory):
    for participant in os.listdir(data_directory):
        if (os.path.isdir(os.path.join(data_directory, participant))):
            for angle in os.listdir(os.path.join(data_directory, participant)):
                if (os.path.isdir(os.path.join(data_directory, participant, angle))):
                    for exercise in os.listdir(os.path.join(data_directory, participant, angle)):
                        if (os.path.isdir(os.path.join(data_directory, participant, angle, exercise))):
                            path_list, old_filenames, new_filenames = [], [], []

                            for root, dirs, files in os.walk(os.path.join(data_directory, participant, angle, exercise), topdown=False):
                                for file in files:
                                    if file.endswith('.mp4'):
                                        path = os.path.join(root, file)
                                        path_list.append((path, file))

                            for _ in range(42):
                                random.shuffle(path_list)
                            
                            for ind, (path, old_filename) in enumerate(path_list):
                                new_filename = old_filename[2:-7] + f'{ind+1:03d}.mp4'
                                output_root_dir = 'newD' + path[1:(-1*len(new_filename))-7]
                                os.makedirs(output_root_dir, exist_ok=True)
                                command = shlex.split(f'ffmpeg -i {path.replace('\\', '/')} -c copy -an {os.path.join(output_root_dir, new_filename).replace('\\', '/')}')
                                subprocess.call(command, shell=True)
                                old_filenames.append(old_filename)
                                new_filenames.append(new_filename)

                            csv_path = os.path.join(data_directory, participant, f'{participant}_{angle}_{exercise}_changelogs.csv')
                            pd.DataFrame(data={'old_filenames':old_filenames, 'new_filenames':new_filenames}).to_csv(path_or_buf=csv_path, index=False)



if __name__ == '__main__':
    data_directory = 'data'
    rename_files(data_directory)
    shuffle_and_rename_vid_files(data_directory)
    ...