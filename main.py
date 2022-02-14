import pathlib
import argparse
import json

parser = argparse.ArgumentParser(description='Merge text files recursive')
parser.add_argument('root', type=pathlib.Path, help="Input directory")
args = parser.parse_args()


def recursive_collect(path: pathlib.Path):
    for entry in path.iterdir():
        if entry.is_file() and entry.suffix == '.txt':
            yield entry
        if entry.is_dir():
            yield from recursive_collect(entry)


def merge_lines(lines: [str]):
    return ''.join(lines).strip().replace('\n', '')


def process(files: [str]):
    meta = list()
    data = list()
    for file in files:
        f_content = read(file)
        link = merge_lines(f_content[:1])
        text = merge_lines(f_content[1:])
        meta.append({'source': link, 'text': text})
        data.append(text)
    return meta, data


def read(path: pathlib.Path):
    with open(path) as f:
        return f.readlines()


def write_json(path: str, data):
    with open(path, 'w') as f:
        f.write(json.dumps(data))


def write_txt(path: str, data):
    with open(path, 'w') as f:
        f.write('\n'.join(data))


if __name__ == '__main__':
    files = recursive_collect(args.root)
    meta, data = process(files)
    write_json('url2text.json', meta)
    write_txt('texts.txt', data)
