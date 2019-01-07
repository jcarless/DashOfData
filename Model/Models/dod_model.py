import os, sys
sys.path.append("Model/PreProcessing")
from posData_preprocessing import posData
import indicies_preprocessing as ind
from econData_preprocessing import econData
import numpy as np
           
#divide into train and test set
train = posData[:int(0.7*(len(posData)))]
test = posData[int(0.7*(len(posData))):]

IYK_train = ind.IYK[:int(0.7*(len(ind.IYK)))]
IYK_test = ind.IYK[int(0.7*(len(ind.IYK))):]

RHS_train = ind.RHS[:int(0.7*(len(ind.RHS)))]
RHS_test = ind.RHS[int(0.7*(len(ind.RHS))):]

FSTA_train = ind.FSTA[:int(0.7*(len(ind.FSTA)))]
FSTA_test = ind.FSTA[int(0.7*(len(ind.FSTA))):]

VDC_train = ind.VDC[:int(0.7*(len(ind.VDC)))]
VDC_test = ind.VDC[int(0.7*(len(ind.VDC))):]

PBJ_train = ind.PBJ[:int(0.7*(len(ind.PBJ)))]
PBJ_test = ind.PBJ[int(0.7*(len(ind.PBJ))):]

XLY_train = ind.XLY[:int(0.7*(len(ind.XLY)))]
XLY_test = ind.XLY[int(0.7*(len(ind.XLY))):]

FXG_train = ind.FXG[:int(0.7*(len(ind.FXG)))]
FXG_test = ind.FXG[int(0.7*(len(ind.FXG))):]

QQQ_train = ind.QQQ[:int(0.7*(len(ind.QQQ)))]
QQQ_test = ind.QQQ[int(0.7*(len(ind.QQQ))):]

econ_train = econData[:int(0.7*(len(econData)))]
econ_test = econData[int(0.7*(len(econData))):]

