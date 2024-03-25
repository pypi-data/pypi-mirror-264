import sys, os
from collections import OrderedDict
import numpy as np
import argparse

dir_name = os.path.dirname(__file__)
sys.path.append(dir_name)

from .models import DARUMA
daruma_model = DARUMA() #モデル呼び出し


#アミノ酸配列から予測
def predict(seqence):
    return daruma_model.predict_from_seqence(seqence).tolist()

#ファスタファイルから予測
def predict_fasta(fastafile_path,write_to_file=False,output_path="out",threshold=0.5):
    #ファスタファイル読み込み
    with open(fastafile_path,"r") as f:
        data = f.read()

    dic = OrderedDict()
    for block in data.strip(">").split(">"):
        ac,seq = block.split("\n",1)
        seq = seq.replace("\n","").replace("U","X")

        print(f"\r\033[K{ac}") #確認用
        pred_prob = daruma_model.predict_from_seqence(seq) #予測
        pred_class = np.where(pred_prob>threshold, 1, 0)

        dic[ac] = {"seq":seq, "probability":pred_prob.tolist(), "class":pred_class.tolist()}
    
    #ファイルへの出力
    if write_to_file:
        with open(output_path,"w") as f:
            out_str = "\n".join([f"{i} {res} {p:.3f} {c}" for i,res,p,c in zip(range(1,len(seq)+1),seq,pred_prob,pred_class)])
            f.write(f'>{ac}\n{out_str}\n')

    """ 戻り値
    dic={ac1:{"seq":配列1, "probability":予測確率1, "class":予測クラス1},
         ac2:{"seq":配列2, "probability":予測確率2, "class":予測クラス2},
         }
    """
    return dic


#コマンドライン実行用
def main():

    parser = argparse.ArgumentParser(description='Process input and output files.')
    parser.add_argument('input_file', help='Path to input file')
    parser.add_argument('-o', '--output', dest='output_file', default='daruma.out', help='Path to output file')
    args = parser.parse_args()

    input_path = args.input_file
    output_path = args.output_file
    
    dic = predict_fasta(input_path,output_path=output_path)

    with open(output_path,"w") as f:
        for ac in dic:
            seq = dic[ac]["seq"]
            pred_prob = map(lambda p:f"{p:.3}",dic[ac]["probability"])
            pred_class = map(str,dic[ac]["class"])
            f.write(f'>{ac}\n{",".join(seq)}\n{",".join(pred_prob)}\n{",".join(pred_class)}\n')

