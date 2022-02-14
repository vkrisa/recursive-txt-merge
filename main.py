from importlib.resources import path
import pathlib
import argparse

parser = argparse.ArgumentParser(description='Merge text files recursive')
parser.add_argument('root', type=pathlib.Path, help="Input directory")
args = parser.parse_args()

def recursive_collect(path: pathlib.Path):
    for entry in path.iterdir():
        if entry.is_file() and entry.suffix == '.txt':
            yield entry
        if entry.is_dir():
            yield from recursive_collect(entry)


def process(files: [str]):
    for file in files:
        f_content = read(file)
        link = f_content[:1]
        text = f_content[1:]
        yield {'source': link, 'text': text}



def read(path: pathlib.Path):
    with open(path) as f:
        return f.readlines()

if __name__ == '__main__':
    files = recursive_collect(args.root)
    data = list(process(files))
    print(data[-1])
