import pandas as pd

class DateTransforms():
    
    def __init__(self):
        pass 
    
    def get_period_groupby(self, df, period = 'M', date_col = 'date') -> pd.DataFrame:
        '''Inputs: period (str) one of \'M\',\'D\',\'Y\' '''
        allowed_periods = ['D','M','Y']
        if period not in allowed_periods:
            raise ValueError(f'Unrecognized period value {period}. Period should be one of {allowed_periods}')
        if period == 'Y':
            output_col = 'year'
        if period == 'M':
            output_col = 'month_year'
        if period == 'D':
            output_col = 'full_year'
        df[output_col] = df[date_col].dt.to_period('M')
        return df
    
    
    def get_days_of_interest(self, df, period_col = 'month_year', date_col = 'date', agg = 'max'):
        '''Get days specified by agg for periods of interest'''
        days = df.groupby(period_col)[[date_col]].agg({date_col:agg}).reset_index(drop=True)
        days = days.merge(df, how = 'inner', on = date_col)
        return days
    
    
    def get_date_mask(self, df, start_date, end_date, date_col = 'date'):
        return (df[date_col] > start_date) & (df[date_col] <= end_date)
    
    
class NumericalTransforms():
    
    def __init__(self):
        pass 
    
    def get_pct_change(self, series: pd.Series):
        return series.pct_change().fillna(0)
    
    def is_min(self, series, date_val):
        min_val = series.min()
        return min_val == date_val

    def is_max(self, series, date_val):
        max_val = series.max()
        return max_val == date_val
    

class GeneralPreprocessing():

    def remove_missing(self, df: pd.DataFrame, col = 'value', missing_pattern = '.') -> pd.DataFrame:
        return df.loc[df[col] != missing_pattern]




