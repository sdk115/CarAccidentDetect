import tensorflow as tf
from tensorflow.contrib import rnn
import numpy as np
from param import *

X = tf.placeholder(tf.float32, [None, n_step, n_input])
Y = tf.placeholder(tf.float32, [None, n_class])

W1 = tf.Variable(tf.random_normal([n_hidden1, n_hidden2]))
b1 = tf.Variable(tf.random_normal([n_hidden2]))

W2 = tf.Variable(tf.random_normal([n_hidden2, n_class]))
b2 = tf.Variable(tf.random_normal([n_class]))

cell = tf.nn.rnn_cell.LSTMCell(n_hidden1)
outputs, states = tf.nn.dynamic_rnn(cell, X, dtype=tf.float32)

outputs = tf.transpose(outputs, [1, 0, 2])
outputs = outputs[-1]

model1 = tf.matmul(outputs, W1) + b1
model2 = tf.matmul(model1, W2) + b2

cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=model2, labels=Y))
optimizer = tf.train.AdamOptimizer(learning_rate).minimize(cost)

y_pred = tf.argmax(model2, 1)
y_test = tf.argmax(Y, 1)

is_correct = tf.equal(y_pred, y_test)
accuracy = tf.reduce_mean(tf.cast(is_correct, tf.float32))