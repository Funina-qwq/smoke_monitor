import os
import sys
import time
import torch
from threading import Thread,current_thread
from multiprocessing import Process
import cv2
from testplus import get_age,set_age
from collections import deque
from multiprocessing.pool import Pool
import numpy as np
def test(num):
    print(num)
    return num*num

if __name__ ==  '__main__':
   print(np.array((2,0)))
  

#程序停止print就会停止
#追加json文件用dict同一个键值对加进去,json外层不能写列表！dump会自动取列表第一个元素
#判断不能以=0为依据，有的时候可能多层循环的会越界
#Pyside和PYQT
#Dataloader和对象成员细究
#字典update方法
#查看复杂的数据结构要会用type判断类型然后一步一步查看子属性（keys(),...）
#路径连接主要中间的连接斜杠不能少
#三种警告屏蔽
#logging调试法而不是print
#无法屏蔽的代码段，内部强制更换到控制台标准输出/logging
#cfg匿名对象的作用，静态类代替匿名对象
#路径的正反斜杠作用对比\\ 等价/，混排,反斜杠路径必须要两个完成转义
#进程线程别忘了start测试的时候
#理解空数组的维度计算
#num_work的不可行性
#与其加入后剔除不如当初就不加
#np.array不能和None比较   
#nan列表去除和None
#闭包返回多函数公用变量？
#numpy的random生成数据用于测试  
#列表pop顺序
#闭包的外对象会一直存在，可以用来编写多线程的线程池函数
#比较复杂的构造函数，先把属性在前面初始化方便查阅，再到后面一个一个处理
#脚本测试单元的路径直接写在脚本上面
#同时线程卡住要看一下队列有没有去掉阻塞，不一定是死锁！！！,block=False取消阻塞但是不一定会写报错
#大量刷屏未输出不一定没扫描到，可能在中间有，不要人眼看要用程序给他选出来
#多线程程序有问题要多试几下/有的时候会出一些问题比如摄像头真的过热暂时失灵打不开
#线程中间可能会有明显的执行速度差异尤其是没有工作中的主线程最快
#python有很多比较鸡肋的语言特性，如GIL，解释性，线程进程继承DEBUFF等，所以没必要用它做高性能开发，只要做近似的开发就行，其他做做脚本
#基础python线程类会把其他属性方法全部删掉当start的时候,但是队列却可以保留
#dqeue maxlen
#锁释放不能写在有可能异常的语句后面    
#生产者消费者模型（两者通信一个队列参数，链式通信，每个两个参数，图通信，每个N个）-》优化设计模式todo
#进程是最高级业务，不应该让外部进程能够与内部进程交互，所以进程设计通信队列参数在同级来制定封装，不会影响到其他层
#三种队列，优先队列的优先级
#引用对象即使是其他对象的属性依然会保留引用性质
#32位与64位对比
#python打包exe
#多线程的队列是简单的生产消费模型，用于处理不重复数据的同步处理（阻塞下无遗漏，这里同步指的是快者等待慢者而不越位） 
#多个cap可以读一个摄像头？警告
#cv2.DSHOW尽量不要加进去除非暂时无法解决报错
#python可空返回
#signal的alarm不可用写timeout
#timeout可附加callback方法与默认打印方法lambda
#列表的引用传递设计
#list为空简化判断
#timeout装饰器函数不可返回
#对象构造函数初始化顺序
#print的连续性输出，不满足逗号运算符
#queue写满将阻塞线程，多线程重点！block方法
#主进程或者主线程阻塞将无法接受到控制台终端的输入，从而无法终止其结束以结束子进程或者子线程
#构造函数可调用自身函数，但是不可以互相调用，互调直接栈溢出
#对于部分函数打包同类参数防止函数参数列表过长
#构造函数的属性引用？？
#process的run直接传args而不传入target
#公用写target在外面，否则写run加args
#装饰器/类方法/函数的单例模式
#进程名线程们重复性与pid
#单例模式和多例模式要定死，避免二意设计
#子进程的run内队列进程内线程共享
#子进程与主进程的通信共享机制
#线程池
#全局/进程/线程变量
#自定义线程的额外信息可以用来区分子线程
#进程通信采用传参模式（打包（queue,barrier）封装性）,遵从生产消费模型，采用self.target传入queue等参数。不可省略queue参数因为，多文件全局变量不能传递，新文件要交互两个进程类要传入中间参数
#自定义线程不把target写在外面因为想要整体封装不污染外面环境，外面target用于通用方法
#多种不同类型进程线程，进程线程分离，多例线程传参，单例线程全局变量（不同的单例进程（或者不同线程）写在一个文件夹时，使用的队列应当名称不一）
#跨文件变量不可写
#不需要通信的进程线程直接重写run，要通信的用target
#python类型限定
#多线程的数据竞争本质，读写同时才会出问题
#进程信息不共享显著区别-》引用将无法传递信息，而线程依然可以
#线程虽然共享，但是依然需要传递参数（没有引用类型的参数怎么共享啊）（子线程交互+子父交互）
#如果参数再外面用不到就要避免对象引用传参而是传递配置文件
#线程传入的参数中，如果是公用的用打包引用对象传递，独立的一定要隔离开传递不能打包，否则其他线程可能会影响到其他线程的独立参数
#外层配置文件可以过余参数为了高效编码，内层只取有效参数即可
#配置文件类的统一性（都是简单的结构体，不使用循环赋值）,很长的可以采用循环属性赋值,处理的代码不需要按次序
#注释写简单点，自己模块的总结，不需要写很详细，除非这里逻辑很难写一个段落注释
#自定义线程进程，队列写在里面queue，如果要和外面交互，构造函数也要有queue等参数（更多交互内容加上去），target参数不支持queue等不可迭代对象
#用run方法想要传入更多参数全部通过构造函数属性来实现传递
#barrier不可作为process属性（包括其包装），也可能由于process的不稳定性，但是可以作为线程的属性
#进程交互属性只有queue之类的，线程可以打包barrier在内的
#一般项目设计的原则，对于已经规划好的项目，按照既定框架开发第一版，中间不能大幅变动。随后根据业务增加，进行模块为单元重构，下上阶层调试
#文件全局首行设置DEBUG全局变量，然后测试时用True，测试全部完毕用脚本全部设成False关闭调试输出
#常量不可修改
#字典列表引用类型，有copy函数处理引用
#字典pop删除键值对
#cv2 IO读取速度，开摄像头花费2.7s，读取第一张图片0.28s，后面的0.03s
#批次显卡优化性能
#超线程/查看逻辑处理器与原理/
#队列内置锁
#GIL机制
#多线程本身是调度算法，有基础执行的单元操作，粒度并不是无限,如汇编字节码
#数据库实现百万级线程调度，那你读写数据库也是多线程请求对应服务器多线程响应（期间则会调用多核处理与读写），所以起到若干倍加速，
# 同时网络传输也是类似IO，发送过去就是闲置等待服务器响应回来，期间可以再次发送，多个网络需求连续发出，可做到同时网络传输
#with lock
#线程池在多次使用短小线程时使用（小型不同任务队列），而且可以获得返回值；map和submit
#并发，Flask框架
#多进程池main下加pool来沟通进程
#IO定义
#只有单线程的操作进一步优化可以考虑协程，异步IO信号量
#死锁例
#—__new__(cls,...)方法与单例模式instance*2+lock，object，cls
#...缩写
#lock影响性能（协程解决）Rlock一般在调用子函数导致多次acquire同一个锁导致死锁
#__enter__/__exit__方法
#多线程读没有竞争，因为多线程本质粒度，不写累计性的一般也不会有竞争（理解本质具体分析）
#queue
#condition/event/sm.../
#跨文件的值类型全局变量用函数会销毁，但是对象不会，利用此写多线程
#collections导入双端队列