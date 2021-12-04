import os


def remove_duplicates():
    src_file_name = 'Maya_Voices.csv'
    dst_file_name = 'Maya_Voices_Filtered.csv'
    with open(src_file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    lines = [line.rstrip('\n') for line in lines]
    res_indices = list()
    res_lines = list()
    for line in lines:
        if (line.split(',')[0] in res_indices):
            continue
        else:
            res_lines.append(line)
            res_indices.append(line.split(',')[0])
    with open(dst_file_name, 'w', encoding='utf-8') as f:
        f.write('\n'.join(res_lines))

def check():
    file_name = 'Maya_Voices_Filtered.csv'
    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    lines = [line.rstrip('\n') for line in lines]
    for line in lines:
        row = line.split(',')
        if len(row) == 1:
            pass
        else:
            row = [row[0]] + [float(r) for r in row[1:]]
        if len(row) == 1 or len(row) == 8:
            if len(row) == 8:
                assert row[1] == 1.0, ValueError('{}'.format(line))
                assert 0.85 <= row[2] <= 1.0, ValueError('{}'.format(line))
                assert 1.0 <= row[3] <= 1.2, ValueError('{}'.format(line))
                assert 1.0 <= row[4] <= 1.4, ValueError('{}'.format(line))
                assert 0.0 <= row[5] <= 0.5, ValueError('{}'.format(line))
                assert 0.0 <= row[6] <= 0.5, ValueError('{}'.format(line))
                assert 0.0 <= row[7] <= 0.5, ValueError('{}'.format(line))
        else:
            assert ValueError('Invalid Format at {}'.format(line))
    print('finished...')

def check_action():
    src_file = 'Maya_Voices_Filtered.csv'
    tgt_file = 'Maya_Voices_Filtered_Action.csv'
    with open(src_file, 'r', encoding='utf-8') as f:
        src_lines = f.readlines()
    src_lines = [line.rstrip('\n').split(',')[0] for line in src_lines ]
    src_lines  = [line for line in src_lines if not line.startswith('#')and not line.startswith('%')]
    print(len(src_lines), len(list(set(src_lines))))
    if len(src_lines) != len(list(set(src_lines))): raise ValueError('Not Much Source File...')
    
    with open(tgt_file, 'r', encoding='utf-8') as f:
        tgt_lines = f.readlines()
    tgt_lines = [line.rstrip('\n').split(',')[0] for line in tgt_lines]
    tgt_lines  = [line for line in tgt_lines if not ( line.startswith('#') or line.startswith('%'))]
    print(len(tgt_lines) ,len(list(set(tgt_lines))))
    if len(tgt_lines) != len(list(set(tgt_lines))): raise ValueError('Not Much Target File...')

    for word in tgt_lines:
        if word in src_lines:
            pass
        else:
            raise ValueError('SOURCE and TARGET does not much...{}'.format(word))

    for word in src_lines:
        if word in tgt_lines:
            pass
        else:
            raise ValueError('SOURCE and TARGET does not much...{}'.format(word))

    print('ALL GREEN!!!!!!!!!!!!')

def paramCheck():
    tgt_file = 'Maya_Voices_Filtered_Action.csv'
    with open(tgt_file, 'r', encoding='utf-8') as f:
        tgt_lines = f.readlines()
    tgt_lines = [line.rstrip('\n').split(',')for line in tgt_lines if line.startswith('%')]
    for line in tgt_lines:
        if line[0] in ['%Lookingup', '%Question', '%Waiting', '%Goodby']:
            pass
        else:
            raise ValueError('Invalid Mode at {}'.format(','.join(line)))

        print(line)
        if line[1] in ['Surprised', 'Normal', 'Null', 'Embarrassed', 'Sad', 'Happy', 'Fear', 'Fun', 'Anger', 'EyeClose', 'Disgust']:
            pass
        else:
            raise ValueError('Invalid Face at {}'.format(','.join(line)))

def WMF():
    mode = None
    face = None
    res_lines = list()
    tgt_file = 'Maya_Voices_Filtered_Action.csv'

    save_file = 'Maya_WMF.csv'
    with open(tgt_file, 'r', encoding='utf-8') as f:
        tgt_lines = f.readlines()
    tgt_lines = [line.rstrip('\n').split(',')for line in tgt_lines]
    for line in tgt_lines:
        if line[0].startswith('%'):
            mode = line[0][1]
            face = line[1]
        elif line[0].startswith('#'):
            pass
        else:
            assert mode != None and face != None
            res_lines.append(line[0] + ',' + mode + ',' + face)

    with open(save_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(res_lines))

def voice_check():
    remove_duplicates()
    check()

def action_check():
    check_action()
    paramCheck()
    WMF()

def check_action_audio():
    action_file = r"Maya_WMF.csv"
    with open(action_file, 'r', encoding='utf-8') as f:
        actions = f.readlines()
    actions = [action.split(',')[0] for action in actions]

    audio_dir = r"C:\Users\Atsuya\Music\Maya_Live2D"
    files = os.listdir(audio_dir)
    audios = [file.split('.')[0] for file in files]

    for ac in actions:
        print(ac)
        if ac in audios:
            pass
        else:
            assert ValueError('Not found action :{}'.format(ac))

    for au in audios:
        print(au)
        if  au in actions:
            pass
        else:
            assert ValueError('Not found audio : {}'.format(au))


    print("ALL GREEEEEEEEEEEEEEEEEEEEEEN!")


if __name__=='__main__':
    # voice_check()
    action_check()
    check_action_audio()