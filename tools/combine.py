import argparse
import json
from sklearn.model_selection import train_test_split

def load_data(args):
    files = [args.input_file1, args.input_file2]
    input_data = []
    for f in files:
        with open(f, "r") as reader:
            input_data.append(json.load(reader)["data"])

    return input_data[0], input_data[1]

def combine(set_A, set_B, args):
    i = len(set_A)
    for example in set_B:
        example['qid'] = i
        i += 1
    result = set_A + set_B
    result, drop = train_test_split(result, test_size=0, random_state=args.random_state, shuffle=args.shuffle) 
    result = {'dataset': args.datatype, 'data':result}
    return result

def write2json(data, filename):
    with open(filename, 'w', encoding='utf-8') as fo:
        json.dump(data, fo, ensure_ascii=False)
    
if  __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file1', type=str)
    parser.add_argument('--input_file2', type=str)
    parser.add_argument('--output', type=str)
    parser.add_argument('--shuffle', type=bool, default=True)
    parser.add_argument('--random_state', type=int, default=42)
    parser.add_argument('--datatype', type=str, help='train/dev/test', default='train')

    args = parser.parse_args()
    

    set_A, set_B = load_data(args)
    set_mix = combine(set_A, set_B, args)
    # print(len(set_A), len(set_B), len(set_mix))
    write2json(set_mix, args.output)


