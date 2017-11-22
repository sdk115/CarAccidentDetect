
# coding: utf-8

# In[6]:


import numpy as np
import tensorflow as tf
from tensorflow.contrib import rnn
import numpy as np
from pprint import pprint
import csv

from param import *
from preprocess import *
from model import *


# In[7]:


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
        
    


# In[8]:


with tf.Session() as sess :
    saver = tf.train.Saver()
    sess.run(tf.global_variables_initializer())
    
    for epoch in range(total_epoch):
        _, cost_val = sess.run([optimizer, cost],
                               feed_dict={X: train_x, Y: train_y})
        

        print('Epoch:', '%04d' % (epoch + 1), 'Avg. cost =', '{:.7f}'.format(cost_val))
        
        print(sess.run(accuracy, feed_dict={X: train_x, Y: train_y}))
        print(sess.run(accuracy, feed_dict={X: test_x, Y: test_y}))
        
        print('사고 test:', sess.run(accuracy, feed_dict={X: test_accident_x, Y: test_accident_y}))
        print('안전 test:', sess.run(accuracy, feed_dict={X: test_normal_x, Y: test_normal_y}))



    print('최적화 완료!')
    print('정확도:', sess.run(accuracy, feed_dict={X: test_x, Y: test_y}))
    ckpt_path = saver.save(sess, "./saved/train1")

    
    


# In[ ]:





# In[ ]:




