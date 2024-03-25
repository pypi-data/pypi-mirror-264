import numpy as np
import sys, os

dir_name = os.path.dirname(__file__)

sys.path.append(dir_name)
from struct import unpack

def load_AAindex():
    key = ["A","C","D","E","F","G","H","I","K","L","M","N","P","Q","R","S","T","V","W","Y","X"]

    features_path = os.path.join(os.path.dirname(__file__), 'data', 'AAindex553-Normal-X0.feature')
    with open(features_path,"rb") as f:
        binary_data = f.read()
    data = unpack(">11613f",binary_data)

    Dic = {}
    for a,i in zip(key,range(0,11613,553)):
        Dic[a] = data[i:i+553]
    
    return Dic


def relu(x):
    return np.maximum(0, x)

def softmax(x):
    x = x - np.max(x, axis=-1, keepdims=True)   # オーバーフロー対策
    return np.exp(x) / np.sum(np.exp(x), axis=-1, keepdims=True)


def D1im2col(x, filter_l):
    L, dim = x.shape
    out_h = L - filter_l + 1

    col = np.zeros((filter_l, dim, out_h),dtype="float32")

    for j in range(filter_l):
        j_max = j + out_h
        for i in range(dim):
            col[j, i, :] = x[j:j_max, i]

    col = col.transpose(2, 0, 1).reshape(out_h, -1)
    return col

#layer
class D1Conv:
    def __init__(self,W,b,active):
        FW,_,FN = W.shape #(FW,dim,FN)

        self.FW = FW
        self.FN = FN
        self.W = W.reshape(-1,FN)
        self.b = b
        self.active = active
        
    def forward(self,x):
        
        L,_ = x.shape
        OL = L - self.FW + 1

        col = D1im2col(x,self.FW)
        x = np.dot(col,self.W) + self.b
        x = x.reshape(OL,self.FN)

        return self.active(x)

class Affine:
    def __init__(self,W,b,active):
        self.W = W
        self.b = b
        self.active = active
        
    def forward(self,x):
        return self.active(np.dot(x,self.W) + self.b)
