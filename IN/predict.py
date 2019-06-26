# Simple Linear Regression

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('data.csv')
X = dataset.iloc[:, 1].values
y = dataset.iloc[:, 2].values


X=X.reshape(-1,1)
y=y.reshape(-1,1)
# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

X_train= X_train.reshape(-1, 1)
y_train= y_train.reshape(-1, 1)
X_test = X_test.reshape(-1, 1)


# Fitting Simple Linear Regression to the Training set
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X, y)

sample=np.array([[3]],dtype=float)
# Predicting the Test set results
y_pred = regressor.predict(sample)
print('ytest=',y_test)
print('ypred=',y_pred)

# Visualising the Training set results
plt.scatter(X_train, y_train, color = 'red')
plt.plot(X_train, regressor.predict(X_train), color = 'blue')
plt.title('week no vs sunday count (Training set)')
plt.xlabel('weekno')
plt.ylabel('sunday count')
plt.show()

# Visualising the Test set results
plt.scatter(X_test, y_test, color = 'red')
plt.plot(X_train, regressor.predict(X_train), color = 'blue')
plt.title('week no vs sunday count (Test set)')
plt.xlabel('week no')
plt.ylabel('sunday count')
plt.show()