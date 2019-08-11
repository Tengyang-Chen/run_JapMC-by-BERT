import csv
import json
from sklearn.model_selection import train_test_split
import copy
from janome.tokenizer import Tokenizer

'''
    load_data():
    loading all knowhow (train, dev, test)set
    input : files[]:[train.csv, dev.csv, test.csv]
    return: mixed_dataset[] 
'''
def load_data(files):
    i = 0
    examples_temp = []
    t = Tokenizer(mmap=True)
    ##loading train_set
    for f in files:
        with open(f, newline='', encoding='utf-8') as fi:
            reader = csv.reader(fi)
            for row in reader:
                title = 'knowhow_v2'
                context = ' '.join(t.tokenize(row[2].strip(), wakati=True))
                answer = ' '.join(t.tokenize(row[1].strip(), wakati=True))
                is_impossible = False if len(answer)>0 else True
                question = ' '.join(t.tokenize(row[0].strip(), wakati=True))
                answer_start = 0 if is_impossible else context.find(answer)
                qid = i
                example = {'title': title, 'context': context, 'is_impossible': is_impossible, 'qid': qid, 'question': question, 'answer': answer, 'answer_start': answer_start}
                i += 1
                examples_temp.append(example)
    
    return examples_temp
'''
    shuffle_QAC():
    shuffle all knowhow (train, dev, test)set, make it unanswerable.
    input : example_mixed[]
    return: example_train[], example_dev[], check_list[], origin[]
'''
def shuffle_QAC(examples_mixed):
    # print(len(examples_mixed)) #716
    examples_origin = copy.deepcopy(examples_mixed)
    examples_mixed, drop = train_test_split(examples_mixed, shuffle=True, test_size=0, random_state=42)
    answerable_count = 0
    check_list = []
    for i in range(0, len(examples_mixed)):
        if examples_mixed[i]['qid'] == examples_origin[i]['qid']:
            answerable_count += 1
            check_list.append({'qid': examples_mixed[i]['qid'], 'comt': 'answerable'})
            continue
        else:
            answer_a = examples_mixed[i]['answer']
            answer_b = examples_origin[i]['answer']
            flag = answer_b.find(answer_a) if len(answer_b) >= len(answer_a) else answer_a.find(answer_b)
            if flag<0:
                examples_mixed[i]['answer'] = ''
                examples_mixed[i]['is_impossible'] = True
                examples_mixed[i]['answer_start'] = 0
                examples_mixed[i]['question'] = examples_origin[i]['question']
            else:
                check_list.append({'qid': [examples_mixed[i]['qid'], examples_origin[i]['qid']], 'comt': 'check'})
        # print(answer_a, answer_b, flag)
        # break

    examples_train, examples_dev = train_test_split(examples_mixed, shuffle=False, test_size=1/7)#1/7
    # print("len(train):%d" % (len(examples_train))) #len(train):613
    # print("len(dev):%d" % (len(examples_dev))) #len(dev):103
    # print("answerable:%d" % (answerable_count)) #answerable:1

    result_train= {'dataset': "train", 'data':examples_train}
    result_dev= {'dataset': "dev", 'data':examples_dev}
    result_checklist= {'dataset': "checklist", 'data':check_list}
    result_origin =  {'dataset': "origin", 'data':examples_origin}
    # result_test= {'dataset': "test", 'data':examples_train}
    # return result_train, result_checklist, result_origin

    return result_train, result_dev, result_checklist, result_origin

def write2json(data, filename):
    with open(filename, 'w', encoding='utf-8') as fo:
        json.dump(data, fo, ensure_ascii=False)


if __name__ == '__main__':

    files = ['../QAC_short_cv1_noconnect/knowhowQA_train.csv',
            '../QAC_short_cv1_noconnect/knowhowQA_dev.csv',
            '../QAC_short_cv1_noconnect/knowhowQA_test.csv']
    # files = ['~/vscode/test/dataset/other/apartment/test-v2.2_neo.json']

    examples_mixed = load_data(files)
    result_train, result_checklist, result_origin = shuffle_QAC(examples_mixed)

    #wirte into file

    write2json(result_train, './train_v2.0_neo.json')
    write2json(result_dev, './dev_v2.0_neo.json')
    write2json(result_checklist, './checklist.json')
    write2json(result_origin, './origin_v2.0_neo.json')

    # write2json(result_train, '~/vscode/test/dataset/other/apartment/test-v2.3_neo.json')
    # write2json(result_checklist,  '~/vscode/test/dataset/other/apartment/checklist.json')


    