#!/usr/bin/env python
# -*-coding: utf-8-*-

import numpy as np
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET

#xml中の各種キーネーム
_RES_SHELL_GRAPH="Resolution shell"
_WAVELENGTH_RANGE_GRAPH="Wavelength range"
_TWOTHETA_RANGE_GRAPH="2Theta range"
_DETECTOR_GRAPH="Detector"
_RUN_GRAPH= "Run"

_TITLE = "Title"
_X_AXIS = "Xaxis"
_REF = "Reflection"
_INDEP_REF = "Unique reflection"
_I_OV_SIG ="I/sigma"
_RED = "Redundancy"
_R_PIM="Rpim"
_R_INT="Rint"
_R_SIG="Rsig"
_COMP ="Completeness"


## グラフの設定
X_labels =[]
X_labels_value =[]
X_data_value = []
plot_data_value = []
Y_data_value = []
Z_data_value= []
P_data_value= []
I_data_value= []
S_data_value= []
C_data_value= []


#分解能シェルグラフ用数値の"辞書"を作成
valuesForResolutionShellGraph = {
    _TITLE : "",
    _X_AXIS : [],
    _REF : [],
    _INDEP_REF : [],
    _I_OV_SIG : [],
    _RED : [],
    _R_PIM :[],
    _R_INT :[],
    _R_SIG :[],
    _COMP :[],
}
#その他のグラフ用の辞書を、オブジェクトのコピーで作成
valuesForWaveLengthGraph = dict( valuesForResolutionShellGraph )
valuesForTwoThetaGraph = dict( valuesForResolutionShellGraph )
valuesForDetectorGraph = dict( valuesForResolutionShellGraph )
valuesForRunGraph = dict( valuesForResolutionShellGraph )

#xmlファイルの読み込み
tree=ET.parse('./valuesForGraphs.xml')

#親要素取得
elem = tree.getroot()

#tagが"graph"の要素でループを回す
for graph_dict in elem.getiterator("graph"):

    whichGraph = graph_dict.items()[0][1]
    #print "Parent element's keyname = " + whichGraph


    #whichGraphの値によって、以下で読み取る子要素の値を詰める辞書を切り替える
    valuesToPut = dict()
    if whichGraph == _RES_SHELL_GRAPH:
        valuesToPut = valuesForResolutionShellGraph
    elif whichGraph == _WAVELENGTH_RANGE_GRAPH:
        valuesToPut = valuesForWaveLengthGraph

    valuesToPut[_TITLE] = whichGraph


    es = graph_dict.findall('.//params[@key="Xaxis"]')
    for e in es:
        X_labels = np.arange(len( e.text.split(",") ))
        X_labels_value =  e.text.split(",")

    #"graph"の子要素でループを回す
    for graph_dict_Child in graph_dict:
        #子要素のキーネームで、何の値かを識別する。
        whichValue = graph_dict_Child.items()[0][1]

        if whichValue == _REF:
            #list中の要素をint型にパースして、辞書に詰める
            valuesToPut[whichValue] = map( int, graph_dict_Child.text.split(",") )
            X_data_value = valuesToPut[whichValue]

        elif whichValue == _INDEP_REF:
            #list中の要素をfloat型にパースして、辞書に詰める
            valuesToPut[whichValue] = map( float, graph_dict_Child.text.split(",") )
            plot_data_value = valuesToPut[whichValue]

        elif whichValue == _I_OV_SIG:
            #list中の要素をfloat型にパースして、辞書に詰める
            valuesToPut[whichValue] = map( float, graph_dict_Child.text.split(",") )
            Y_data_value = valuesToPut[whichValue]

        elif whichValue == _RED:
            #list中の要素をfloat型にパースして、辞書に詰める
            valuesToPut[whichValue] = map( float, graph_dict_Child.text.split(",") )
            Z_data_value = valuesToPut[whichValue]

        elif whichValue == _R_PIM:
            #list中の要素をfloat型にパースして、辞書に詰める
            valuesToPut[whichValue] = map( float, graph_dict_Child.text.split(",") )
            P_data_value = valuesToPut[whichValue]

        elif whichValue == _R_INT:
            #list中の要素をfloat型にパースして、辞書に詰める
            valuesToPut[whichValue] = map( float, graph_dict_Child.text.split(",") )
            I_data_value = valuesToPut[whichValue]

        elif whichValue == _R_SIG:
            #list中の要素をfloat型にパースして、辞書に詰める
            valuesToPut[whichValue] = map( float, graph_dict_Child.text.split(",") )
            S_data_value = valuesToPut[whichValue]

        elif whichValue == _COMP:
            #list中の要素をfloat型にパースして、辞書に詰める
            valuesToPut[whichValue] = map( float, graph_dict_Child.text.split(",") )
            C_data_value = valuesToPut[whichValue]

    bar_width = 0.6
    plt.subplots_adjust(left=0.04, bottom=0.3, right=0.95, wspace=0.5, hspace=0.3)
    plt.rcParams['font.size'] = 9

    plt.suptitle('Reflection statstics on each resolution shells. (I/sigma > 0.0, excl. dets = 4.14)', size=15)


    plt.subplot(371)
    plt.xlabel(graph_dict.items()[0][1])
    plt.ylabel('Number of reflection')
    plt.bar(X_labels, X_data_value, bar_width, color='lime',label="all")
    plt.plot(plot_data_value, color='k', marker='o',label="uniq.",markersize=4)
    plt.xticks(X_labels,X_labels_value,rotation=65,size=9)
    plt.margins(0.01,0)
    lgnd = plt.legend(loc="best", bbox_to_anchor=(0.58,1.41), ncol=1)
    plt.grid()


    plt.subplot(372)
    plt.xlabel(r"Resolution shell")
    plt.ylabel('Rint')
    plt.bar(X_labels, P_data_value, bar_width, color='purple',label="Rint")
    plt.xticks(X_labels,X_labels_value,rotation=90,size=10)
    plt.margins(0.01,0)
    lgnd = plt.legend(loc="best", bbox_to_anchor=(0.55,1.26,0,0), ncol=2)
    plt.grid()

    plt.subplot(373)
    plt.xlabel(r"Resolution shell")
    plt.ylabel('Rpim')
    plt.bar(X_labels, I_data_value, bar_width, color='yellow', label="Rpim")
    plt.xticks(X_labels,X_labels_value,rotation=65,size=10)
    plt.margins(0.01,0)
    lgnd = plt.legend(loc="best", bbox_to_anchor=(0.6,1.26,0,0), ncol=2)
    plt.grid()

    plt.subplot(374)
    plt.xlabel(r"Resolution shell")
    plt.ylabel('Rsig')
    plt.bar(X_labels, S_data_value, bar_width, color='orange', label="Rsig")
    plt.xticks(X_labels,X_labels_value,rotation=65,size=10)
    plt.margins(0.01,0)
    lgnd = plt.legend(loc="best", bbox_to_anchor=(0.58,1.26,0,0), ncol=2)
    plt.grid()

    plt.subplot(375)
    plt.xlabel(r"Resolution shell")
    plt.ylabel('I /sigma')
    plt.bar(X_labels, Y_data_value, bar_width, color='blue',label="I/sigma")
    plt.xticks(X_labels,X_labels_value,rotation=65,size=10)
    plt.margins(0.01,0)
    lgnd = plt.legend(loc="best", bbox_to_anchor=(0.7,1.26,0,0), ncol=2)
    plt.grid()

    plt.subplot(376)
    plt.xlabel(r"Resolution shell")
    plt.ylabel('Redundancy')
    plt.bar(X_labels, Z_data_value, bar_width, color='green',label="Redundancy")
    plt.xticks(X_labels,X_labels_value,rotation=65,size=10)
    plt.margins(0.01,0)
    lgnd = plt.legend(loc="best", bbox_to_anchor=(0.93,1.26,0,0), ncol=2)
    plt.grid()

    plt.subplot(377)
    plt.xlabel(r"Resolution shell")
    plt.ylabel('Completeness')
    plt.bar(X_labels, C_data_value, bar_width, color='pink', label="Completeness")
    plt.xticks(X_labels,X_labels_value,rotation=65,size=10)
    plt.margins(0.01,0)
    lgnd = plt.legend(loc="best", bbox_to_anchor=(1.05,1.26,0,0), ncol=2)
    plt.grid()

    plt.show()


