import pandas as pd
import numpy as np
import json

selected_categories = pd.read_csv("selected_categories.csv")['category']

def read_raw_data(timefile, state, n_files):
    """
    Read in the raw compression files and concat to pandas dataframes
    timefile: file folder name of the time period e.g. '07-13Oct_weekly', '07-13Oct_weekly'
    state: state variable in the dataset e.g. 'NY', 'CA'
    n_files: number of .csv.gz files in the folder
    """
    
    df_lst = [] # create an empty list and read in the files one by one

    for i in range(1, n_files + 1): 
        filepath = f'../SafeGraph_data/{timefile}/core_poi-geometry-patterns-part{i}.csv.gz'
        data = pd.read_csv(filepath, compression='gzip')
        data = data[(data['top_category'].isin(selected_categories)) & (data['region'] == state)]
        df_lst.append(data)
        print(filepath)
        
    df = pd.concat(df_lst)
    return df

def unpack_home_cbgs(df):
    """
    Input the SafeGraph dataframe, 
    unpack the json column ''visitor_home_cbgs'',
    return a dataframe with each row as a visitor home CBG and the corresponding placekey and brand.
    The output dataframe will have the following columns:
    - placekey: the unique identifier for the POI
    - brands: the brand of the place
    - visitor_home_cbgs: the CBG of the visitor's home
    - cbg_visitor_count: the number of visitors from that CBG
    """
    
    # convert jsons to dicts
    df = df.assign(dicts = [json.loads(cbg_json) for cbg_json in df.visitor_home_cbgs])

    # extract each key:value inside each related_same_month_brand dict (2 nested loops) 
    lst = []
    for index, row in df.iterrows():
        lst.extend([ {'placekey': row['placekey'],
                    'brands': row['brands'],
                        'visitor_home_cbgs' : key, 
                        'cbg_visitor_count' : value} 
                                for key,value in row['dicts'].items() ])
    
    cbg_unpack = pd.DataFrame(lst)
    return cbg_unpack

def unpack_related_brand(df, var_name):
    """
    This function is used to unpack the json columns 'related_same_month_brand', 'related_same_week_brand'.
    Input the SafeGraph dataframe,
    var_name: the name of the json column to unpack, e.g. 'related_same_month_brand', 'related_same_week_brand'
    Output a dataframe with each row as a related brand and the corresponding visitor counts.      
    """

    # convert jsons to dicts
    df = df.assign(dicts = [json.loads(brand_json) for brand_json in df[var_name]])

    # extract each key:value inside each dict (2 nested loops) 
    lst = []
    for index, row in df.iterrows():
        lst.extend([ {'brands': row['brands'],
                    'raw_visitor_counts': row['raw_visitor_counts'],
                        var_name : key, 
                        'visitor_percent' : value} 
                                for key,value in row['dicts'].items() ])
        
    unpack = pd.DataFrame(lst)
    return unpack

def get_covisit_edgelist(df, var_name):
    """
    Get the covisit edgelist from the dataframe.
    """

    # unpack json column
    related_unpack = unpack_related_brand(df, var_name)
    # get the covisitor count for each poi to aggregate at the brand level
    related_unpack['covisitor_counts'] = related_unpack['raw_visitor_counts'] * related_unpack['visitor_percent'] *0.01
    # number of visitors for each brand
    brand_visitors = df[['brands', 'raw_visitor_counts']].groupby('brands', as_index = False).sum()

    covisit_edgelist = related_unpack[['brands', var_name, 'covisitor_counts']]
    covisit_edgelist = covisit_edgelist.groupby(['brands', var_name], as_index = False).sum()
    covisit_edgelist = covisit_edgelist.merge(brand_visitors, on = 'brands')
    covisit_edgelist['weight'] = covisit_edgelist['covisitor_counts'] * 100 / covisit_edgelist['raw_visitor_counts']
    covisit_edgelist = covisit_edgelist[['brands', var_name, 'weight']]
    covisit_edgelist = covisit_edgelist[covisit_edgelist[var_name].isin(covisit_edgelist['brands'])]
    covisit_edgelist = covisit_edgelist.reset_index(drop = True)

    return covisit_edgelist


def get_covisit_matrix(covisit_edgelist, var_name):
    """
    Transfer the covisit network from edgelist to matrix.
    """
    # groupby and unstack to get the matrix
    covisit_matrix = covisit_edgelist.groupby(['brands', var_name]).agg({'weight': np.mean}).unstack()
    # drop the 'weight' column index
    covisit_matrix.columns = covisit_matrix.columns.droplevel(0)
    # replace NaN as 0
    covisit_matrix = covisit_matrix.fillna(0)
    # fill the self loop as 100 percent
    for i in covisit_matrix.index.values[:]:
        if i in covisit_matrix.columns:
            covisit_matrix.loc[i, i] = 100            
    # normalise with 100
    covisit_matrix = covisit_matrix / 100

    return covisit_matrix


def get_brand_cat(df):
    """
    Get the brand and category info from the dataframe.
    """
    brand_cat = df[['brands', 'naics_code', 'top_category', 'sub_category']]
    brand_cat = brand_cat.groupby(['brands', 'naics_code', 'top_category', 'sub_category']).sum().reset_index()
    brand_cat['naics_code'] = brand_cat['naics_code'].astype('int')
    brand_cat['naics_code'] = brand_cat['naics_code'].astype('str')
    return brand_cat

