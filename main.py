import os
import subprocess
import shlex
import random
import pandas as pd

os.system('cls')
subprocess.call(shlex.split('pip freeze > requirements.txt'), shell=True)

def main():
    old_filenames = []
    new_filenames = []
    directory = './.data'
    saving_directory = './.newData'
    participants_list = os.listdir(directory)

    if not os.path.exists(saving_directory):
            os.mkdir(saving_directory)
    for participant in participants_list:
        next_directory1 = '/' + participant
        if not os.path.exists(saving_directory + next_directory1):
            os.mkdir(saving_directory + next_directory1)
        angle_list = os.listdir(directory + next_directory1)

        for angle in angle_list:
            next_directory2 = next_directory1 + '/' + angle
            if not os.path.exists(saving_directory + next_directory2):
                os.mkdir(saving_directory + next_directory2)
            exercise_list = os.listdir(directory + next_directory2)

            for exercise in exercise_list:
                next_directory3 = next_directory2 + '/' + exercise
                if not os.path.exists(saving_directory + next_directory3):
                    os.mkdir(saving_directory + next_directory3)
                iteration_list = os.listdir(directory + next_directory3)
                count_list = list(range(1, len(iteration_list)+1))

                for iteration in iteration_list:
                    file_list = os.listdir(directory + next_directory3 + '/' + iteration)

                    for file in file_list:
                        if file.endswith('.mp4'):
                            old_filenames.append(file)
                            random_number = random.choice(count_list)
                            count_list.remove(random_number)
                            new_filename = participant + '_' + angle + '_' + exercise + '_0' + str(random_number) + '.mp4'
                            new_filenames.append(new_filename)
                            # print(file, new_filename)
                            file_path = directory + next_directory3 + '/' + iteration + '/' + file
                            save_path = saving_directory + next_directory3 + '/' + new_filename
                            print(file_path)
                            # print(save_path)
                            # videoclip = VideoFileClip(file_path)
                            # new_clip = videoclip.without_audio()
                            # new_clip.write_videofile(save_path)
                            command = shlex.split(f'ffmpeg -i {file_path} -c copy -an {save_path}')
                            subprocess.call(command, shell=True)
                            data = pd.DataFrame(data={'old_filenames':old_filenames, 'new_filenames':new_filenames})
                            csv_filename = participant + '_' + angle + '_' + exercise + '.csv'
                            csv_path = saving_directory + '/' + participant + '/' + csv_filename
                            data.to_csv(path_or_buf=csv_path, index=False)
                            print(f'{file} done')
                            print(f'{'':-^100}')
                        else:
                            filename_to_list = file.split('_')
                            new_csv_filename = filename_to_list[0] + '_' + participant + '_' + angle + '_' + exercise + '_' + iteration + '_' + filename_to_list[-1]
                            os.rename(file_path, directory + next_directory3 + '/' + iteration + '/' + new_csv_filename)
                    # break
                # break
            # break


if __name__ == '__main__':
    main()