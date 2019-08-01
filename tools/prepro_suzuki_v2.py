import csv
import json
from sklearn.model_selection import train_test_split
from janome.tokenizer import Tokenizer

'''
    load_data():
    loading suzuki's dataset
    input : path of all-v1.0.json
    return: examples[] 
'''
def load_data(input_file):
    examples_temp = []
    t = Tokenizer(mmap=True)
    with open(input_file, 'r', encoding='utf-8') as fi:
        for line in fi.readlines():
            temp = json.loads(line)
            question = ' '.join(t.tokenize(temp['question'].strip(), wakati=True))
            i = 0
            for instance in temp['documents']:
                title = instance['title']
                context = ' '.join(t.tokenize(instance['text'].strip(), wakati=True))
                # if instance['score'] < 2:
                #     continue
                is_impossible = False if instance['score'] > 1 else True
                answer = "" if is_impossible else ' '.join(t.tokenize(temp['answer'].strip(), wakati=True))
                qid = temp['qid']*10 + i
                answer_start = 0 if is_impossible else context.find(answer)
                example = {'title': title, 'context': context, 'is_impossible': is_impossible, 'qid': qid, 'question': question, 'answer': answer, 'answer_start': answer_start}
                i += 1
                examples_temp.append(example)
    examples_train, examples_dev = train_test_split(examples_temp, shuffle=False, test_size=0.1)

    result_train = {'dataset': "train", 'data':examples_train}
    result_dev = {'dataset': "dev", 'data':examples_dev}

    return result_train, result_dev

def write2json(data, filename):
    with open(filename, 'w', encoding='utf-8') as fo:
        json.dump(data, fo, ensure_ascii=False)
         
if __name__ == '__main__':
    input_file = './all-v1.0.json'
    train_output_file = './train-v2.0_neo.json'
    dev_output_file = './dev-v2.0_neo.json'

    result_train, result_dev = load_data(input_file)

    write2json(result_train, train_output_file)
    write2json(result_dev, dev_output_file)
    