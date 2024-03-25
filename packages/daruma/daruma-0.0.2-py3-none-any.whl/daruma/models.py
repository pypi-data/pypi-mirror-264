import numpy as np
import sys, os

dir_name = os.path.dirname(__file__)
sys.path.append(dir_name)

from .functions import *
from struct import unpack     


class DARUMA:
    def __init__(self):
        self.feature = load_AAindex() #AAindex呼び出し
        self.model = CV5()            #予測モデル

    def predict_from_seqence(self, seq):
        x = np.array([self.feature[res] for res in seq],dtype="float32")
        
        pred_prob = self.model(x)[:,1] #予測確率を出力
        
        return pred_prob
    

class CV5:
    def __init__(self):
        self.params = {}

        weight_parameters_path = os.path.join(os.path.dirname(__file__), 'data', 'CV5.weight')
        with open(weight_parameters_path,"rb") as f:
            binary_data = f.read()
        data = unpack(">7302914f",binary_data)

        self.params["W1"] = np.array(data[0:353920],dtype="float32").reshape(5,553,128)
        self.params["b1"] = np.array(data[353920:354048],dtype="float32")
        self.params["W2"] = np.array(data[354048:435968],dtype="float32").reshape(5,128,128)
        self.params["b2"] = np.array(data[435968:436096],dtype="float32")
        self.params["W3"] = np.array(data[436096:518016],dtype="float32").reshape(5,128,128)
        self.params["b3"] = np.array(data[518016:518144],dtype="float32")
        self.params["W4"] = np.array(data[518144:600064],dtype="float32").reshape(5,128,128)
        self.params["b4"] = np.array(data[600064:600192],dtype="float32")
        self.params["W5"] = np.array(data[600192:682112],dtype="float32").reshape(5,128,128)
        self.params["b5"] = np.array(data[682112:682240],dtype="float32")
        self.params["W6"] = np.array(data[682240:7301376],dtype="float32").reshape(101,128,512)
        self.params["b6"] = np.array(data[7301376:7301888],dtype="float32")
        self.params["W7"] = np.array(data[7301888:7302912],dtype="float32").reshape(512,2)
        self.params["b7"] = np.array(data[7302912:7302914],dtype="float32")

        self.conv1 = D1Conv(self.params["W1"],self.params["b1"],active=relu)
        self.conv2 = D1Conv(self.params["W2"],self.params["b2"],active=relu)
        self.conv3 = D1Conv(self.params["W3"],self.params["b3"],active=relu)
        self.conv4 = D1Conv(self.params["W4"],self.params["b4"],active=relu)
        self.conv5 = D1Conv(self.params["W5"],self.params["b5"],active=relu)
        self.conv6 = D1Conv(self.params["W6"],self.params["b6"],active=relu)
        self.affine0 = Affine(self.params["W7"],self.params["b7"],active=softmax)

        self.layers = [self.conv1,self.conv2,self.conv3,self.conv4,self.conv5,self.conv6,self.affine0]

    def __call__(self,x):
        x = np.pad(x, [(60,60),(0,0)], 'constant')
        for layer in self.layers:
            x = layer.forward(x)

        return x

