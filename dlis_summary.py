import dlisio
from dlisio import dlis
import pandas as pd
import numpy as np

pd.set_option('display.max_rows', 600)
pd.set_option('display.max_colwidth', None)

loc1='/data/NorthernLights/31_5-7 Eos/'

# Run on the LWD files as that is all I have available.
LWDFiles=[loc1+'05.LWD_Log_data/WLC_RAW_CAL-DEN-GR-NEU-REMP_MWD_1.DLIS',
loc1+'05.LWD_Log_data/WLC_RAW_GR-REMP-RLL_MWD_1.DLIS',
loc1+'05.LWD_Log_data/WL_RAW_AAC_MWD_1.DLIS',
loc1+'05.LWD_Log_data/WL_RAW_CAL-DEN-GR-NEU-REMP_MWD_1.DLIS',
loc1+'05.LWD_Log_data/WL_RAW_GR-REMP_MWD_2.DLIS',
loc1+'05.LWD_Log_data/WL_RAW_GR-REMP_MWD_3.DLIS',
loc1+'05.LWD_Log_data/WL_RAW_GR-REMP_MWD_4.DLIS',
loc1+'05.LWD_Log_data/WL_RAW_GR-REMP-RLL_MWD_1.DLIS',
loc1+'05.LWD_Log_data/WL_RAW_GR-REMP-RLL_MWD_2.DLIS',
loc1+'05.LWD_Log_data/WL_RAW_GR-REMP-RLL_MWD_3.DLIS']

def summarize(objs, **kwargs):
    """Create a pd.DataFrame that summarize the content of 'objs', One 
    object pr. row
    
    Taken from: https://github.com/equinor/dlisio-notebooks/blob/master/acoustic.ipynb
    
    Parameters
    ----------
    
    objs : list()
        list of metadata objects
        
    **kwargs
        Keyword arguments 
        Use kwargs to tell summarize() which fields (attributes) of the 
        objects you want to include in the DataFrame. The parameter name 
        must match an attribute on the object in 'objs', while the value 
        of the parameters is used as a column name. Any kwargs are excepted, 
        but if the object does not have the requested attribute, 'KeyError' 
        is used as the value.
        
    Returns
    -------
    
    summary : pd.DataFrame
    """
    summary = []
    for attr, label in kwargs.items():
        column = []
        for obj in objs:
            try:
                value = getattr(obj, attr)
            except AttributeError:
                value = 'KeyError'
    
            column.append(value)
        summary.append(column)

    summary = pd.DataFrame(summary).T
    summary.columns = kwargs.values()
    return summary

def make_summary_file(filename):
    '''Given a DLIS file, make a short human readable summary of it.
    Show things like headers, well parameters and which well curves are available.
    Args:
    filename: A DLIS file.
    
    Returns:
    summaryfile: The DLIS file without the extention and the suffix _summary.txt

    '''
    # To Do:
    # Work out how to get DLISIO to decode the degree unicode symbol
    summaryfile=open (filename.replace('.DLIS','_summary.txt'),'w')
    
    
    f, *f_tail = dlis.load(filename)
    if len(f_tail): print('There are more logical files in tail')
        
    origin, *origin_tail = f.origins
    if len(origin_tail): print(filename+' contains multiple origins')
        
    header= f.fileheader
    #Parameters
    parameter_table = summarize(f.parameters, name='Name', long_name='Long name', values='Value(s)')
    # Hide parameters containing names
    mask = ~parameter_table['Name'].isin(['R8', 'RR1', 'WITN', 'ENGI'])
    parameter_table = parameter_table[mask]
    parameter_table.sort_values('Name')
    
    summaryfile.write(str(f.describe()))
    summaryfile.write(str(origin.describe()))
    summaryfile.write(str(header.describe()))
    summaryfile.write(str(parameter_table))
    
    for frame in f.frames:
        index_channel = next(ch for ch in frame.channels if ch.name == frame.index)
        summaryfile.write(f'\nFrame {frame.name}:\n')
        summaryfile.write(f'Description      : {frame.description}\n')
        summaryfile.write(f'Indexed by       : {frame.index_type}\n')
        summaryfile.write(f'Interval         : [{frame.index_min}, {frame.index_max}] {index_channel.units}\n')
        summaryfile.write(f'Direction        : {frame.direction}\n')
        summaryfile.write(f'Constant spacing : {frame.spacing} {index_channel.units}\n')
        summaryfile.write(f'Index channel    : {index_channel}\n')
        summaryfile.write(f'No. of channels  : {len(frame.channels)}\n')

    channel_table = summarize(f.channels, name='Name', long_name='Long name', units='Units',
                                          dimension='Dimension', frame='Frame')
    channel_table.sort_values('Name')
    summaryfile.write(str(channel_table))

    summaryfile.close()
    return summaryfile

for filename in LWDFiles:
    make_summary_file(filename)
