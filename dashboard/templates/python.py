print ("IMPORTING LIBRARIES...")
import pandas as pd


print ("LOADING DATASETS...")
df_train = pd.read_csv("http://127.0.0.1:8000/media/files/" + "{{ title }}" + "_train.csv")
df_train.head()

df_test = pd.read_csv("http://127.0.0.1:8000/media/files/" + "{{ title }}" + "_test.csv")
df_test.head()

print ("STEP 1: DOING MY TRANSFORMATIONS...")
df_train = df_train.fillna(0)
df_test = df_test.fillna(0)


print ("STEP 2: SELECTING CHARACTERISTICS TO ENTER INTO THE MODEL...")
def get_specific_columns(df, data_types, to_ignore = list(), ignore_target = False):
    columns = df.select_dtypes(include=data_types).columns
    if ignore_target:
        columns = filter(lambda x: x not in to_ignore, list(columns))
    return list(columns)

output_var = df_train.columns[-1]
in_model = get_specific_columns(df_train, ["float64", "int64"], [output_var], ignore_target = True)


print ("STEP 3: DEVELOPING THE MODEL...")
X_train = df_train[in_model]
y_train = df_train[output_var]
X_test = df_test[in_model]

from sklearn.linear_model import LogisticRegression
clf = LogisticRegression(random_state=0, solver='lbfgs')
fitted_model = clf.fit(X_train, y_train)
pred_train = fitted_model.predict_proba(X_train)[:,1]
pred_test  = fitted_model.predict_proba(X_test)[:,1]


print ("STEP 4: GETTING THE RESULTS...")
import requests
from requests.auth import HTTPBasicAuth
df_test['pred'] = pred_test
df_test['id'] = df_test.iloc[:,0]
df_test_to_send = df_test[['id','pred']]

df_test_to_send.to_csv('upload_this.csv', sep=',')
