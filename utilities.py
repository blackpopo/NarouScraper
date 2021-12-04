import random
import os
import MeCab
mecab = MeCab.Tagger()
from tqdm import tqdm

def read_lines(file_name): #file_name is already jointed by folder name
    with open(os.path.join(file_name), 'r', encoding="utf-8") as f:
        lines = f.readlines()
    lines = [line.rstrip('\n') for line in lines]
    return lines

def extend_lines(base_lines, extend_lines):
    return base_lines.extend(extend_lines)

def get_all_file_names(folder_name, file_names):
    if os.path.isdir(folder_name):
        folders = os.listdir(folder_name)
        for folder in folders:
            get_all_file_names(os.path.join(folder_name, folder), file_names)
    else:
        return file_names.add(folder_name)

def get_files():
    files = set()
    get_all_file_names('Datasets', files)
    print('All Files Are Gotten')
    return list(files)

def get_all_lines():
    files = get_files()
    res_lines = list()
    for file in tqdm(files):
        extend_lines(res_lines, read_lines(file))
    print('All Lines Are Gotten')
    return res_lines

def save_default_dict(dict, save_file_name, count=-1):
    sorted_dict = reversed(sorted(dict.items(), key= lambda x:x[1]))
    save_list = [key + ',' + str(value) for key, value in sorted_dict]
    if count > 0:
        save_list = save_list[:count]
    with open(save_file_name, 'w', encoding='utf-8') as f:
        f.writelines('\n'.join(save_list))


def mecab_parse(line):
    res_tokens, res_positions = list(), list()
    tokens_positions = mecab.parse(line).splitlines()
    for token_position in tokens_positions[:-1]:
        try:
            token, positions = token_position.split('\t')
            position = positions.split(',')
            res_tokens.append(token)
            res_positions.append(position)
        except:
            print(line)
    return res_tokens, res_positions



if __name__=='__main__':
    print(get_files())
