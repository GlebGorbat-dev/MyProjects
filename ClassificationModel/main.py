import random

import numpy as np

#dataset
features = np.array([[1, 0], [0, 2], [1, 1], [1, 2], [1, 3], [2, 2], [2, 3], [3, 2]])
labels = np.array([0, 0, 0, 0, 1, 1, 1, 1])

#score func
def score(weights, bias, feature):
    return np.dot(feature, weights) + bias

#pred function
def step(x):
    if x >= 0:
        return 1
    else:
        return 0

def prediction(weights, bias, feature):
    return step(score(weights, bias, feature))

#loss func
def loss(weights, bias, feature, label):
    pred = prediction(weights, bias, feature)
    if pred == label:
        return 0
    else:
        return np.abs(score(weights, bias, feature))

#perceptron method
def perceptron_trick(weights, bias, feature, label, learning_rate = 0.01):
    pred = prediction(weights, bias, feature)
    for i in range(len(weights)):
        weights[i] += (label - pred) * feature[i] * learning_rate
        bias += (label - pred) * learning_rate

    return weights, bias

#perceptron algorithm
def perceptron_algorithm(feature, label, learning_rate = 0.01, epochs = 170):
    weights = [1.0 for i in range(len(feature[0]))]
    bias = 0.0
    losses = []
    for epoch in range(epochs):
        total_loss = 0
        for i in range(len(features)):
            total_loss += loss(weights, bias, features[i], labels[i])
        losses.append(total_loss / len(features))
        i = random.randint(0, len(features) - 1)
        weights, bias = perceptron_trick(weights, bias, features[i], labels[i])
    return weights, bias, losses

if __name__ == "__main__":
   weights, bias, losses =  perceptron_algorithm(features, labels)

   print("Weights:", weights)
   print("Bias:", bias)
   print("Losses:", losses)