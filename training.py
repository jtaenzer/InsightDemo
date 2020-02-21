from sklearn.preprocessing import scale
from os import environ
# This will stop tensorflow from spamming unnecessary error messages about its GPU implementation
# Needs to set before we import anything from keras/tensorflow
environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import np_utils

from get_data import get_data

years = ['2017', '2018']

home_str = "game_outcome, pen_min, pen_min_opp, corsi_pct, fenwick_pct, faceoff_percentage, zs_offense_pct, pdo"
visitor_str = "pdo"

training_data = get_data(years, home_str, visitor_str)

input = training_data[:, 1:]
input = scale(input)

output = training_data[:, :1]
output = np_utils.to_categorical(output)

input_dim = len(input[0])
output_dim = int((3/2)*input_dim)

model = Sequential()
model.add(Dense(output_dim, input_dim=input_dim, activation='relu'))
model.add(Dense(int((2/3)*output_dim), activation='relu'))
model.add(Dense(2, activation='softmax'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(input, output, epochs=500, verbose=2)
model.save("./model.h5")
