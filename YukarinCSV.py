import os

from AutoYukarin import AutoYukarin, mouse
from tqdm import tqdm
from time import sleep

# def test():
#     yukarin.yukarin("いらっしゃいました", joy=0.3, sad=1.0)

def audio_files():
    audio_dir = r"C:\Users\Atsuya\Music\Maya_Live2D"
    files = os.listdir(audio_dir)
    files = [name.split('.')[0] for name in files]
    return files

def yukarin_maya_voices():
    yukarin = AutoYukarin()
    print("Start Program...")
    file_name = 'Maya_Voices_Filtered.csv'
    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    lines = [line.rstrip('\n') for line in lines]
    volume, speed, height, intonation, happy, anger, sad = 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0
    pre_volume, pre_speed, pre_height, pre_intonation, pre_happy, pre_anger, pre_sad = 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0
    faulted_lines = list()
    already_files = audio_files()
    for line in tqdm(lines):
        row = line.split(',')
        voice = row[0]
        if len(row) == 8:
            volume, speed, height, intonation, happy, anger, sad = [float(f) for f in row[1:]]
        if voice.startswith('#'):
            pass
        else:
            if (voice not in already_files):
                print(voice)
                try:
                    if (pre_volume == volume and pre_speed == speed and pre_height == height and pre_happy == happy and pre_anger == anger and pre_sad == sad and pre_intonation == intonation):
                        yukarin.yukarin(voice, is_set_param=False)
                    else:
                        yukarin.yukarin(voice, volume, speed, height, intonation, happy, anger, sad)
                    sleep(1.0)
                except:
                    faulted_lines.append(line)
                    sleep(2.0)
                    mouse.click(coords=(1050, 600))
                    sleep(1.0)
                    mouse.click(coords=(1050, 600))
                    sleep(1.0)
            pre_volume, pre_speed, pre_height, pre_intonation, pre_happy, pre_anger, pre_sad =  volume, speed, height, intonation, happy, anger, sad
            # print(voice, volume, speed, height, intonation, happy, anger, sad)
    print("Finish Program...")
    if len(faulted_lines) > 0:
        with open('Faulted.log', 'w', encoding='utf-8') as f:
            f.write('\n'.join(faulted_lines))

if __name__=="__main__":
    # test()
    # check()
    yukarin_maya_voices()