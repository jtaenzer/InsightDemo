import numpy as np
from get_data import get_data
from sklearn.preprocessing import scale
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from os import environ
# This will stop tensorflow from spamming unnecessary error messages about its GPU implementation
# Needs to set before we import anything from keras/tensorflow
environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from keras.models import load_model

years = ['2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']

home_str = "game_outcome, pen_min, pen_min_opp, corsi_pct, fenwick_pct, faceoff_percentage, zs_offense_pct, pdo"
visitor_str = "pdo"

model = load_model("./model.h5")
accuracy = list()
for year in years:
    testing_data = get_data([year], home_str, visitor_str)

    test_input = testing_data[:, 1:]
    test_input = scale(test_input)

    true_output = testing_data[:, :1]

    pred_output = model.predict(test_input)
    pred_output = [np.argmax(x) for x in pred_output]
    true_output = [int(x[0]) for x in true_output.tolist()]

    a = accuracy_score(pred_output, true_output)
    accuracy.append(a*100)
    print('%s accuracy is:' % year, a*100)

plt.plot(accuracy, marker='.', markersize=10)
plt.title("Model accuracy by year")
plt.xlabel("Year")
plt.xticks([i for i in range(len(accuracy))], years)
plt.ylabel("Accuracy (%)")
plt.savefig("./plots/accuracy_by_year.png")
plt.show()