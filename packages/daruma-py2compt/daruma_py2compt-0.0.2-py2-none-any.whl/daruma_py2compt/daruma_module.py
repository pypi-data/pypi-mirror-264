import sys, os
from collections import OrderedDict
import numpy as np
import argparse

dir_name = os.path.dirname(__file__)
sys.path.append(dir_name)

from .models import DARUMA
daruma_model = DARUMA()


def predict(seqence):
    return daruma_model.predict_from_seqence(seqence).tolist()


def predict_fasta(fastafile_path,write_to_file=False,output_path="out",threshold=0.5):
    with open(fastafile_path,"r") as f:
        data = f.read()

    dic = OrderedDict()
    for block in data.strip(">").split(">"):
        ac,seq = block.split("\n",1)
        seq = seq.replace("\n","").replace("U","X")

        print "\r\033[K{}".format(ac)
        pred_prob = daruma_model.predict_from_seqence(seq)
        pred_class = np.where(pred_prob>threshold, 1, 0)

        dic[ac] = {"seq":seq, "probability":pred_prob.tolist(), "class":pred_class.tolist()}
    

    if write_to_file:
        with open(output_path,"w") as f:
            out_str = "\n".join(["{} {} {:.3f} {}".format(i,res,p,c) for i,res,p,c in zip(range(1,len(seq)+1),seq,pred_prob,pred_class)])
            f.write('>{}\n{}\n'.format(ac,out_str))

    return dic


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
            pred_prob = map(lambda p:"{:.3}".format(p),dic[ac]["probability"])
            pred_class = map(str,dic[ac]["class"])
            f.write('>{}\n{}\n{}\n{}\n'.format(ac,",".join(seq),",".join(pred_prob),",".join(pred_class)))

