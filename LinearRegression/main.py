# from matplotlib import pyplot as plt
# import numpy as np
# import random
# import utils
#
# features = np.array([1,2,3,5,6,7])
# labels = np.array([155, 197, 244, 356,407,448])
#
# print(features)
# print(labels)
#
# utils.plot_points(features, labels)
#
# def simple_trick(base_price, price_per_room, num_rooms, price):
#     small_random_1 = random.random()*0.1
#     small_random_2 = random.random()*0.1
#     predicted_price = base_price + price_per_room*num_rooms
#     if price > predicted_price and num_rooms > 0:
#         price_per_room += small_random_1
#         base_price += small_random_2
#     if price > predicted_price and num_rooms < 0:
#         price_per_room -= small_random_1
#         base_price += small_random_2
#     if price < predicted_price and num_rooms > 0:
#         price_per_room -= small_random_1
#         base_price -= small_random_2
#     if price < predicted_price and num_rooms < 0:
#         price_per_room -= small_random_1
#         base_price += small_random_2
#     return price_per_room, base_price
#
# def absolute_trick(base_price, price_per_room, num_rooms, price, learning_rate):
#     predicted_price = base_price + price_per_room*num_rooms
#     if price > predicted_price:
#         price_per_room += learning_rate*num_rooms
#         base_price += learning_rate
#     else:
#         price_per_room -= learning_rate*num_rooms
#         base_price -= learning_rate
#     return price_per_room, base_price
#
# def square_trick(base_price, price_per_room, num_rooms, price, learning_rate):
#     predicted_price = base_price + price_per_room*num_rooms
#     price_per_room += learning_rate*num_rooms*(price-predicted_price)
#     base_price += learning_rate*(price-predicted_price)
#     return price_per_room, base_price
#
# random.seed(0)
#
# def linear_regression(features, labels, learning_rate=0.01, epochs = 1000):
#     price_per_room = random.random()
#     base_price = random.random()
#     errors = []
#     for i in range(epochs):
#         predictions = features[0]*price_per_room+base_price
#         errors.append(rmse(labels, predictions))
#         i = random.randint(0, len(features)-1)
#         num_rooms = features[i]
#         price = labels[i]
#         # Uncomment one of the following 3 lines to use the simple, the absolute, or the square trick
#         #price_per_room, base_price = simple_trick(base_price,
#         #price_per_room, base_price = absolute_trick(base_price,
#         price_per_room, base_price = square_trick(base_price,
#                                                   price_per_room,
#                                                   num_rooms,
#                                                   price,
#                                                   learning_rate=learning_rate)
#     utils.draw_line(price_per_room, base_price, 'black', starting=0, ending=9)
#     utils.plot_points(features, labels)
#     print('Price per room:', price_per_room)
#     print('Base price:', base_price)
#     plt.show()
#     plt.scatter(range(len(errors)), errors)
#     plt.show()
#     return price_per_room, base_price
#
# linear_regression(features, labels, learning_rate = 0.01, epochs = 10000)
#
# # This line is for the x-axis to appear in the figure
# plt.ylim(0,500)
#
# linear_regression(features, labels, learning_rate = 0.01, epochs = 1000)
#
# # The root-mean-square error function
# def rmse(labels, predictions):
#     n = len(labels)
#     differences = np.subtract(labels, predictions)
#     return np.sqrt(1.0/n * (np.dot(differences, differences)))
#


import turicreate as tc

datadict = {
    'features': features,
    'labels'  : labels,
}

data = tc.SFrame(datadict)

print(data)

model = tc.linear_regression.create(data, target='labels')

print(model.coefficients)

new_point = tc.SFrame({'features': [4]})
model.predict(new_point)
