import argparse
import json
from janome.tokenizer import Tokenizer

def load_data(filename, datatype):
    with open(filename, "r") as reader:
        input_data = json.load(reader)["data"]
    
    t = Tokenizer(mmap=True)
    for example in input_data:
        example['context'] = ' '.join(t.tokenize(example['context'], wakati=True))
        example['answer'] = ' '.join(t.tokenize(example['answer'], wakati=True))
        example['question'] = ' '.join(t.tokenize(example['question'], wakati=True))
        example['answer_start'] = 0 if example['is_impossible'] else example['context'].find(example['answer'])
    
    input_data = {'dataset':datatype, 'data':input_data}
    return input_data

def write2json(data, filename):
    with open(filename, 'w', encoding='utf-8') as fo:
        json.dump(data, fo, ensure_ascii=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str)
    parser.add_argument('--output', type=str)
    parser.add_argument('--datatype', type=str)

    args = parser.parse_args()
    data = load_data(args.input, args.datatype)
    write2json(data, args.output)