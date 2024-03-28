def remove_missing_values(df):
    return df.dropna()

def fill_missing_values(df, value=0):
    return df.fillna(value)
