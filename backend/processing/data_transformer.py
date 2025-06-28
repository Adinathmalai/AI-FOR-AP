import pandas as pd

def filter_call_data(df, number1, number2):
    filtered = df[((df['callerID'] == number1) & (df['calleeID'] == number2)) |
                  ((df['callerID'] == number2) & (df['calleeID'] == number1))]
    return filtered

def calculate_total_duration(filtered_df):
    filtered_df['duration'] = pd.to_datetime(filtered_df['endTime']) - pd.to_datetime(filtered_df['startTime'])
    return filtered_df['duration'].sum()
