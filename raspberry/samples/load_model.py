
# coding: utf-8

# In[2]:


import numpy as np
import tensorflow as tf
from tensorflow.contrib import rnn
import numpy as np
from pprint import pprint
import csv

from param import *
from preprocess import *
from model import *


# In[3]:


x_data, y_data = preprocess('sensor8.csv')

train_rate = 0.7
partition = int(len(x_data)*train_rate)

train_x, test_x = x_data[:partition] , x_data[partition:]
train_y, test_y = y_data[:partition] , y_data[partition:]

test_accident_x = []
test_accident_y = []
test_normal_x = []
test_normal_y = []

for i in range(len(test_x)):
    if np.argmax(test_y[i]) == 1:
        test_accident_x.append(test_x[i])
        test_accident_y.append(test_y[i])
    else :
        test_normal_x.append(test_x[i])
        test_normal_y.append(test_y[i])

print(len(test_normal_x),len(test_accident_x))
        
    


# In[5]:


with tf.Session() as sess :
    saver = tf.train.Saver()
    sess.run(tf.global_variables_initializer())
    saver.restore(sess, "./saved/train1")

    print('최적화 완료!')
    print('정확도:', sess.run(accuracy, feed_dict={X: test_x, Y: test_y}))

    
    


# In[ ]:





# In[ ]:




