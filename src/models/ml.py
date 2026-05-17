import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


def distribute_cumulative(df, interval='1min'):
    end_dates = df.get('endDate', df['startDate'] + pd.Timedelta(minutes=1))

    times = [pd.date_range(s.floor('min'), e.ceil('min'), freq=interval, inclusive='left')
             for s, e in zip(df['startDate'], end_dates)]

    df_exp = pd.DataFrame({'time': times, 'value': df['value']}).explode('time')
    df_exp['value'] /= df_exp.groupby(df_exp.index)['time'].transform('count').replace(0, 1)

    return df_exp.groupby('time')['value'].sum()


def prepare_multivariate(records_df, metrics, interval='1min'):
    if records_df is None or records_df.empty:
        return pd.DataFrame()

    cumulative = {'steps', 'dist'}
    processed = {}

    for m in metrics:
        df_m = records_df[records_df['type'] == m]
        if df_m.empty:
            continue

        df_m['startDate'] = pd.to_datetime(df_m['startDate'], utc=True).dt.tz_localize(None)
        if 'endDate' in df_m.columns:
            df_m['endDate'] = pd.to_datetime(df_m['endDate'], utc=True).dt.tz_localize(None)

        if m in cumulative and 'endDate' in df_m.columns:
            processed[m] = distribute_cumulative(df_m, interval)
        else:
            processed[m] = df_m.set_index('startDate').resample(interval)['value'].mean()

    if not processed:
        return pd.DataFrame()

    df = pd.DataFrame(processed)

    for col in df.columns:
        if col in cumulative:
            df[col] = df[col].fillna(0)
        else:
            df[col] = df[col].interpolate(method='time', limit=15)

    return df.dropna()

def find_anomaly_multivariate(df, contamination=0.05):

    if df.empty or len(df) < 2:
        return pd.DataFrame()

    original_index = df.index
    features = df.columns
    
    if len(features) == 0:
        return pd.DataFrame()

    df_filled = df.fillna(0)

    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df_filled)

    model = IsolationForest(contamination=contamination, random_state=42)
    model.fit(scaled_features)

    predictions = model.predict(scaled_features)
    
    result_df = pd.DataFrame(index=original_index)
    result_df['anomaly'] = predictions
    result_df = result_df.join(df)
    
    return result_df
