from collections import defaultdict
from utilities import *

adverb_counter = defaultdict(int)
adnomial_counter = defaultdict(int)
will_counter = defaultdict(int)
conjunction_counter = defaultdict(int)

def adverb_count(lines):
    for line in tqdm(lines):
        tokens, positions = mecab_parse(line)
        for token, postion in zip(tokens, positions):
            if postion[0] == '副詞':
                adverb_counter[token] += 1
    return adverb_counter

def adnomial_count(lines):
    for line in tqdm(lines):
        tokens, positions = mecab_parse(line)
        for token, postion in zip(tokens, positions):
            if postion[0] == '連体詞':
                adnomial_counter[token] += 1
    return adnomial_counter

def conjunction_count(lines):
    for line in tqdm(lines):
        tokens, positions = mecab_parse(line)
        for token, postion in zip(tokens, positions):
            if postion[0] == '接続詞':
                conjunction_counter[token] += 1
    return conjunction_counter

def will_count(lines):
    for line in tqdm(lines):
        tokens, positions = mecab_parse(line)
        for i, token, postion in zip(range(len(tokens)), tokens, positions):
            if postion[0] == '助動詞' and i > 0 and token == 'う':
                pre_token = tokens[i-1]
                will_counter[pre_token] += 1
    return will_counter

def total_count(lines):
    for line in tqdm(lines):
        tokens, positions = mecab_parse(line)
        for i, token, postion in zip(range(len(tokens)), tokens, positions):
            if postion[0] == '助動詞' and i > 0 and token == 'う':
                pre_token = tokens[i-1]
                will_counter[pre_token] += 1
            elif postion[0] == '接続詞':
                conjunction_counter[token] += 1
            elif postion[0] == '連体詞':
                adnomial_counter[token] += 1
            elif postion[0] == '副詞':
                adverb_counter[token] += 1
            else:
                pass

def count(name, lines=None):
    save_name = 'Data/' + name + '.txt'
    if lines == None:
        lines = get_all_lines()
    if name == 'adverb':
        res_dict = adverb_count(lines)
    elif name == 'adnomial':
        res_dict = adnomial_count(lines)
    elif name == 'conjunction':
        res_dict = conjunction_count(lines)
    elif name == 'will':
        res_dict = will_count(lines)
    else:
        raise ValueError('Not found name : {}'.format(name))
    save_default_dict(res_dict, save_name)

def count2(lines):
    total_count(lines)
    for name, dict in zip(['adverb', 'adnomial', 'conjunction', 'will'], [adverb_counter, adnomial_counter, conjunction_counter, will_counter]):
        save_name = 'Data/' + name + '.txt'
        save_default_dict(dict, save_name)

if __name__=='__main__':
    dirs = os.listdir('Datasets')
    for dir in dirs:
        files = os.listdir(os.path.join('Datasets', dir))
        total_lines = list()
        for file in tqdm(files):
            lines = read_lines(os.path.join('Datasets', dir, file))
            extend_lines(total_lines, lines)
        print('dir: {} lines are read'.format(dir))
        # for name in  ['adverb', 'adnomial', 'conjunction', 'will']:
        #     count(name, total_lines)
        # print('counter is finished at {}'.format(dir))
        count2(total_lines)
        print('dir: {} is finished.'.format(dir))
