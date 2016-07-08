from pandas import DataFrame, Series
from audtools import time2ms, calc_gap_length
from argh import arg
import pandas as pd

OUTCOLS = ['name', 'start', 'end', 'length', 'order']

def parse_splits(fname_or_df, outname=None):
    """From csv with columns name, break, yield a df with start, end and length.

    Parameters:
        fname_or_df:    filename. If df is given, recalculate length.

    Returns: df with name, start, end, length. Units are in milliseconds.
    """
    if type(fname_or_df) == str: log = DataFrame.from_csv(fname_or_df, index_col=None)
    else: log = fname_or_df
    
    if 'break' in log:
        df = DataFrame({'name':  log['name'][0:-1].values,
                        'start': log['break'][0:-1].values,
                        'end':   log['break'][1:].values,
                        'order': range(len(log) - 1)})
    elif 'start' in log: df = log
    else: raise Exception('needs to either have break, or start and end columns')

    # if splits are given in time, convert to millisecond
    if ':' in str(df['start'][0]): 
        for col in ['start', 'end']: df[col] = df[col].apply(time2ms)

    # calculate length
    df['length'] = df['end'] - df['start']
    assert all(col in df for col in OUTCOLS)

    if outname:
        df.to_csv(outname, index=None)
    
    return df.reindex_axis(OUTCOLS, axis=1)

def parse_old_logs(log_file, order_file=None, name=None):
    """Parse logs that have a single column of timepoints for each event"""
    df = DataFrame.from_csv(log_file, index_col=None, header=None)
    df = df.rename(columns={0:'break'})
    if name: df['name'] = name
    elif not 'name' in df: raise Exception('log needs a name column')

    log = parse_splits(df)
    if order_file:
        order = Series.from_csv(order_file, header=None, index_col=None)
        log['order'] = order
    else:
        log['order'] = range(len(log))

    return log

def update_splits(df):
    """Takes dataframe with length column, adds (or replaces) start, end"""
    df['end'] = df['length'].cumsum()
    df['start'] = df['end'].shift()
    df['start'].iloc[0] = 0

def align_blueprints(src, ref, src_on=('old_name', 'order'), ref_on=('name', 'order')):
    """Matches old_name, order cols of src to name, order cols on ref.
    
    parameters:
        src:    blueprint df to reorder to ref
        ref:    blueprint df with name and order columns
    """

    ref = ref[list(ref_on)]
    aligned = pd.merge(src, ref, how='right', left_on=src_on, right_on=ref_on)
    return aligned.rename(columns={'name_x':'name'})

def aud_from_log(df, **kwargs):
    """
    Parameters:
        df: dataframe with start, end, and name columns
        kwargs: audio files corresponding to entries in name column
        
    """
    out = []
    for ii, row in df.iterrows():
        crnt_aud = kwargs[row['name']]
        seg = crnt_aud[row['start']:row['end']]
        out.append(seg)

    return reduce(lambda x,y: x + y, out)


import numpy as np
@arg('--dt', type=int, help='time delta to down/upsample to')
def expand_data(df, dt=1, outname=None):
    """Takes data with events as rows and expands it to have a row for each time unit.

    """
    print type(dt)
    cols = [col for col in df.columns if col != 'ms']
    max_index = df['end'].iloc[-1] / dt
    index = np.arange(max_index)
    exp = DataFrame({'event_num': pd.np.nan, 'ms': index * dt}, index=index)
    for col in cols: exp[col] = pd.np.nan
    for ii, row in df.iterrows():
        indx = (row['start'] / dt <= exp.index) & (exp.index < row['end'] / dt)
        exp['event_num'][indx] = ii
        # copy over columns from df
        for col in cols: exp[col][indx] = row[col]
    if outname:
        exp.to_csv(outname)
    return exp

##############################################################################
# Manipulate Blueprints
##############################################################################

def gap_dict(row, mingap, TRdur):
    """Returns dictionary with fields for gap row. Assumes all rows will have
    gaps ending on a TR
    """
    length = calc_gap_length(row['length'], mingap, TRdur)
    return {'name': 'gap',
            'length': length,
            'start': 0,
            'end': length,
            'order':-1}

def insert_gaps(bp, mingap=1000, TRdur=1500, outname=None):
    """Insert gap row after each entry.
    
    Parameters:
        bp: blueprint filename or dataframe
        mingap: minimum time (in ms) between segment ending and next TR
        TRdur:  length of each TR

    Note: 
        this procedure assumes that the audio begins on a TR, so that only the
        length of each segment may be used to calculate the gap length.
    """
    bp = pd.read_csv(bp) if type(bp) == str else bp
    new_rows = []
    for ii, row in bp.iterrows():
        new_rows.append(row.to_dict())
        new_rows.append(gap_dict(row, mingap, TRdur))
    new = fix_col_order(DataFrame(new_rows))

    if outname:
        new.to_csv(outname, index=None)
    return new

def scramble(df, cond=lambda x: x):
    """Shuffle rows of dataframe"""
    pass

def fix_col_order(df):
    other = [col for col in df.columns if col not in OUTCOLS]
    return df[OUTCOLS + other]
