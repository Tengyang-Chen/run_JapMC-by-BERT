# knowhow
鈴木さんデータセットここにダウンロード  
http://www.cl.ecei.tohoku.ac.jp/rcqa/  
pip install tensorflow-gpu==1.11  
conda install cudatoolkit=9  
conda install cudnn=7  
google bert https://github.com/google-research/bert  BERT-Base, Multilingual Cased (New, recommended)を使う　　
python run_suzuki.py --vocab_file=./multi_cased_L-12_H-768_A-12/vocab.txt --bert_config_file=./multi_cased_L-12_H-768_A-12/bert_config.json --init_checkpoint=./multi_cased_L-12_H-768_A-12/bert_model.ckpt --do_train=True --train_file=./suzuki/train-v1.1.json --do_predict=True --predict_file=./suzuki/dev-v1.1.json --train_batch_size=8 --learning_rate=3e-5 --num_train_epochs=2.0 --max_seq_length=128 --doc_stride=128 --output_dir=./result/suzuki/ --do_lower_case=False --version_2_with_negative=True


https://github.com/google-research/bert  

1.git clone https://github.com/google-research/bert.git  
2.download BERT-Base, Multilingual Cased and unzip  
3.unzip dataset  
4.run run_suzuki.py  
5.download janome https://drive.google.com/drive/folders/0BynvpNc_r0kSd2NOLU01TG5MWnc  
change requirement.txt make sure to install gpu version  
Directory tree  
- bert/
    - run_suzuki.py
    - multi-cased-L12-..../
    - dataset/
    ...
