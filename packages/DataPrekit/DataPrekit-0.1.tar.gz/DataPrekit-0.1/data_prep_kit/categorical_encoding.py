from sklearn.preprocessing import LabelEncoder

def encode_categorical_data(df, column_name):
    le = LabelEncoder()
    df[column_name] = le.fit_transform(df[column_name])
    return df
