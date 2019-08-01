import json
input_file = './all-v1.0.json'
train_output_file = './train-v1.1.json'
dev_output_file = './dev-v1.1.json'

with open(input_file, 'r', encoding='utf-8') as f:
    #  length = len(f.readlines()) 12591
    length, count = 12591 // 10 * 9, 0
    # print(length,count)
    examples_train, examples_dev = [], []
    for line in f.readlines():
        # line = f.readline()
        temp = json.loads(line)
        # print(temp)
        # examples_train, examples_dev = [], []
        question = temp['question']
        i = 0
        for instance in temp['documents']:
            title = instance['title']
            context = instance['text']
            is_impossible = False if instance['score'] > 0 else True
            answer = "" if is_impossible else temp['answer']
            qid = temp['qid']*10 + i
            answer_start = context.find(answer)
            example = {'title': title, 'context': context, 'is_impossible': is_impossible, 'qid': qid, 'question': question, 'answer': answer, 'answer_start': answer_start}
            # example = json.dumps(example)
            if count < length:
                examples_train.append(example)
            else:
                examples_dev.append(example)
            i += 1
        count += 1
    result_train = {'dataset': "train", 'data':examples_train}
    result_dev = {'dataset': "dev", 'data':examples_dev}
    # result = json.dumps(examples, ensure_ascii=False)
    # print(example)
    with open(train_output_file, 'w', encoding='utf-8') as fo:
        # fo.write(result)
        json.dump(result_train, fo, ensure_ascii=False)

    with open(dev_output_file, 'w', encoding='utf-8') as fo:
        # fo.write(result)
        json.dump(result_dev, fo, ensure_ascii=False)
         

    