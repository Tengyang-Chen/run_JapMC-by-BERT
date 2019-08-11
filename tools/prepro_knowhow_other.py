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
def load_data(filename):
    with open(filename, "r") as reader:
        input_data = json.load(reader)["data"]
    
    return input_data
'''
    shuffle_QAC():
    shuffle all knowhow (train, dev, test)set, make it unanswerable.
    input : example_mixed[]
    return: example_mixed[], check_list[], origin[]
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

    examples_data, drop = train_test_split(examples_mixed, shuffle=False, test_size=0)#1/7
    # print("len(train):%d" % (len(examples_train))) #len(train):613
    # print("len(dev):%d" % (len(examples_dev))) #len(dev):103
    print("answerable:%d" % (answerable_count)) #answerable:1

    # result_train= {'dataset': "train", 'data':examples_train}
    # result_dev= {'dataset': "dev", 'data':examples_dev}
    result_checklist= {'dataset': "checklist", 'data':check_list}
    result_origin =  {'dataset': "origin", 'data':examples_origin}
    result_test= {'dataset': "test", 'data':examples_data}
    return result_test, result_checklist, result_origin

    # return result_train, result_dev, result_checklist, result_origin

def write2json(data, filename):
    with open(filename, 'w', encoding='utf-8') as fo:
        json.dump(data, fo, ensure_ascii=False)


if __name__ == '__main__':

    # files = ['../QAC_short_cv1_noconnect/knowhowQA_train.csv',
    #         '../QAC_short_cv1_noconnect/knowhowQA_dev.csv',
    #         '../QAC_short_cv1_noconnect/knowhowQA_test.csv']
    files = '../../test/dataset/other/marriage/test-v2.2_neo.json'

    examples_mixed = load_data(files)
    result_data, result_checklist, result_origin = shuffle_QAC(examples_mixed)

    #wirte into file

    # write2json(result_train, './train_v2.0_neo.json')
    # write2json(result_dev, './dev_v2.0_neo.json')
    # write2json(result_checklist, './checklist.json')
    # write2json(result_origin, './origin_v2.0_neo.json')

    write2json(result_data, '../../test/dataset/other/marriage/test-v2.3_neo.json')
    write2json(result_checklist,  '../../test/dataset/other/marriage/checklist.json')


    