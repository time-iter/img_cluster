#-*- coding=utf-8 -*-
import easygui as gui
import sys
import os
from PIL import Image
from matplotlib.pyplot import *
from numpy import *
import hcluster

    
#以下为主程序

redo = 1
gui.msgbox('\t\t\t\t   图像聚类','图像聚类程序','开始',image='hello.gif')

#使用redo标记是否再次执行
while redo:
    #dir获取值为"c:\windows\system32\"样式，修改dir为python可识别的"c:/windows/system32/"样式
    dir=gui.diropenbox('请选择要聚类图片的文件夹','文件选择')
    path=os.path.abspath(dir)
    path=path.split('\\')
    path='/'.join(path)
    path=path+'/'
    
    #获取处理维度数据
    dim=gui.enterbox('\t请输入图片RGB处理维度','RGB维度输入',default='8')
    #因获取维度数据gui库存在bug(默认在首部添加'\x08')，使用以下处理解决问题
    if dim.startswith('\x08'):
        dim=dim.strip('\x08')
    dim=int(dim)
    
    if path:
        
        #path获取成功则进入图片处理
        imlist1 = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]
        imlist2 = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.png')]
        imlist3 = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.bmp')]
        imlist = imlist1 + imlist2 + imlist3
       #生成图片的向量特征值
        features = zeros([len(imlist),dim*dim*dim])
        for i, f in enumerate(imlist):
            im = array(Image.open(f))
            #形成图像直方图
            h, edges = histogramdd(im.reshape(-1, 3),dim, normed=True, range=[(0, 255), (0, 255), (0, 255)])
            features[i] = h.flatten()
        #调用层次聚类算法进行聚类处理
        tree = hcluster.hcluster(features)

    msg='\t\t\t\t    请选择操作'
    choices=['查看聚类树','提取聚类结果']
    title='功能选择'
    
    #cycle标记查看
    cycle=1
    while cycle:
        choice=gui.buttonbox(msg,title,choices)
        if choice=='查看聚类树':
            fname=gui.enterbox('\t\t\t请命名聚类树','查看聚类树')
            #展示聚类生成树
            hcluster.draw_dendrogram(tree,imlist,filename=fname+'.pdf')
            closet=gui.msgbox('\t\t\t\t聚类树已生成','提示')
            if closet==None:
                exit()
        elif choice=='提取聚类结果':
            dis,num=gui.multenterbox('\t\t请输入聚类结果提取参数','提取聚类结果',['间距','聚类簇数'],[0.25,1])
            dis = float(dis)
            num = int(num)
            
            clusters = tree.extract_clusters(dis * tree.distance)
           
            for c in clusters:
                elements = c.get_cluster_elements()
                nbr_elements = len(elements)
                if nbr_elements > num:
                    figure()
                    for p in range(minimum(nbr_elements,20)):
                        subplot(4, 5, p + 1)
                        im = array(Image.open(imlist[elements[p]]))
                        imshow(im)
                        axis('off')
            show()
            closev=gui.msgbox('\t\t\t\t聚类结果提取完成','提示')
            if closev==None:
                exit()
        else:
            cycle=0

    closea=gui.buttonbox('\t\t\t\t 是否进行下一次聚类？','提示',['再次聚类','退出'])
    if closea=='退出':
        gui.msgbox('',image='goodbye.gif')
        redo =0
