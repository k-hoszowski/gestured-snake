#
 #   Copyright 2023 Krzysztof Hoszowski
 #
 #   This file is part of Gestured Snake.
 #
 #   Gestured Snake is free software: you can redistribute it and/or
 #   modify it under the terms of the GNU General Public License as published by
 #   the Free Software Foundation, either version 3 of the License, or
 #   (at your option) any later version.
 #
 #   Gestured Snake is distributed in the hope that it will be useful,
 #   but WITHOUT ANY WARRANTY; without even the implied warranty of
 #   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
 #   Public License for more details.
 #
 #   You should have received a copy of the GNU General Public License along
 #   with Gestured Snake. If not, see <https://www.gnu.org/licenses/>.
 #
#
"""Training and testing the hand gesture detection algorithm."""

# Performance timer
from time import perf_counter

# Data processing
from pandas import concat
from image_to_dataframe import im2df

# Training the AI model
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

# Assessing the quality of the AI model
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

# Saving the classifier
from joblib import dump


tic = perf_counter()  # First reading

# Reading the dataframes
dfn, dfc, dfa = im2df()

# Adding labels to dataframes
d = {"label": 0}
dfn = dfn.assign(**d)

d = {"label": 1}
dfc = dfc.assign(**d)

d = {"label": 2}
dfa = dfa.assign(**d)

# Concatenating the dataframes
df = concat([dfn, dfc, dfa], axis=0)


x = df.iloc[:, 0:3]  # Parameter columns
y = df.iloc[:, -1]  # Label column

# Splitting 75% of data into training set, 25% into test set
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.25, random_state=1
)

tac = perf_counter()  # Second reading


# Training the model using Random Forest Classifier
lr_grid = {"max_depth": [4, 8, 16], "criterion": ["entropy", "gini"]}

clf = RandomForestClassifier(n_estimators=12, max_features="sqrt", random_state=1)

# Fitting the model. Grid Search is used to optimize hyper-parameters
gs = GridSearchCV(estimator=clf, param_grid=lr_grid, cv=5)

gs.fit(x_train, y_train)


# Making the prediction
y_pred = gs.predict(x_test)
gs.best_params_

# Obtaining classification report and confusion matrix
print("\nClassification Report: \n", classification_report(y_test, y_pred))
print("Confusion Matrix: \n", confusion_matrix(y_test, y_pred))

toc = perf_counter()  # Third reading


print(f"\nTime taken preparing data: {tac - tic:0.2f} seconds")
print(f"Time taken training and testing: {toc - tac:0.2f} seconds\n")


##########################
# SAVE using joblib #
##########################

dump(gs, "model.pkl")
