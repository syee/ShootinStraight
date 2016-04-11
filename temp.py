import matplotlib.pyplot as plt
import pickle

ax = pickle.load(open('myplot.pickle','rb'))
ax.show()