import os
from tqdm import tqdm

def get_lines(file_dir="NarouData"):
    files = os.listdir(file_dir)
    all_lines = list()
    for file in tqdm(files):
        with open(os.path.join(file_dir, file), 'r', encoding='utf-8') as f:
            lines = f.readlines()
            lines = [l.rstrip('\n').replace('「', '').replace('」', '') for l in lines if l != "\n"]
            all_lines.extend(lines)
    return all_lines

def get_line(file_path):
    with open(os.path.join(file_path), 'r', encoding='utf-8') as f:
        lines = f.readlines()
        lines = [l.rstrip('\n').replace('「', '').replace('」', '') for l in lines if l != "\n"]
    return lines

def get_files(file_dir="NarouData"):
    files = [os.path.join(file_dir, file_name) for file_name in os.listdir(file_dir)]
    return files


#「もし」 「好き/嫌い」
def extract_questions(lines):
    for line in lines:
        if '？' in line:
            # if '好き' in line or '嫌い' in line:
                print(line)

def main():
    # extract_questions(get_lines())
    for file in get_files():
        lines = get_line(file)
        extract_questions(lines)

if __name__=="__main__":
    main()