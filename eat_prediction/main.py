import argparse
from datetime import datetime, timedelta

import pandas as pd
from pre_process.features import day_of_week, daily_order_frequency, straight_location, gender, has_gender, opted_in
from pre_process.orders import get_client_order_map
from sklearn.metrics import confusion_matrix

from learning.classification_ensemble import get_performance_metrics, probability_classification_ensemble
from pre_process.data_frame import generate_data_frames, get_X, get_y

# Files
order_file = 'data/patrons_1930_1668_gender_optin.csv'

# Time Windows
start_time = datetime(2017, 1, 1)
test_train_split_time = datetime(2017, 10, 1)
end_time = datetime(2017, 11, 1)
time_interval = timedelta(hours=68)

# Each feature corresponds to a column for the data set
features = [
    daily_order_frequency,
    straight_location,
    gender,
    has_gender,
    opted_in
]

# Include a column for each unique client id?
add_client_boolean_columns = False

# Don't include users with monthly ordering frequency below this value
minimum_visits = 3

print "Data Filtering Begin"
data_frame = generate_data_frames(
    client_order_map=get_client_order_map(
        pd.read_csv(order_file),
        minimum_visits,
        end_time
    ),
    start_time=start_time,
    end_time=end_time,
    time_interval=time_interval,
    features=features,
    add_client_boolean_columns=add_client_boolean_columns
)
print "Data Filtering End"


df_train = data_frame[data_frame.apply(lambda df_row: (df_row.time_interval.start_time < test_train_split_time), axis=1)]
df_test = data_frame[data_frame.apply(lambda df_row: (df_row.time_interval.start_time >= test_train_split_time), axis=1)]


X_train = get_X(df_train)
y_train = get_y(df_train)

X_test = get_X(df_test)
y_test = get_y(df_test)


model = probability_classification_ensemble()
print "start fitting"
print X_test
model.fit(X_train,y_train)

y_predicted = model.predict(X_test)
print X_test, y_test
print y_predicted
print "prediction"

print "Data Fitting Begin"
model.fit(X_train,y_train)

y_predicted = model.predict(X_test)
print "Prediction"

print len(y_predicted)
print sum(y_predicted)
print len(y_predicted)-sum(y_predicted)
print "Actuals"
print len(y_test)
print sum(y_test)
print len(y_test)-sum(y_test)
print "Confusion_matrix"
print confusion_matrix(y_test,y_predicted)

print get_performance_metrics(y_test,y_predicted)
