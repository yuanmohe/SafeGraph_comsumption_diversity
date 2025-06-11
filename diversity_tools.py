import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_palette("colorblind")


brand_median = pd.read_csv('brand_median.csv')
yelp_labelled = pd.read_csv('yelp_labelled.csv', dtype = {'yelp_dollar' : str})

def get_cbg_brand_count(selected_cbg_brand):
    """
    input the matrix of cbg and brands as pd.dataframe,
    return cbg, brands, and count as edgelist (delete rows with 0 values)
    """
    cbg_brand_count = selected_cbg_brand.stack().reset_index()
    cbg_brand_count.columns = ['cbg', 'brands', 'count']
    cbg_brand_count = cbg_brand_count[cbg_brand_count['count'] > 0].reset_index(drop = True)

    return cbg_brand_count


def get_nbrands(selected_cbg_brand):
    """
    input the matrix of cbg and brands as pd.dataframe,
    return the number of brands each cbg visits as a pd.series
    """

    nbrands = selected_cbg_brand.astype(bool).sum(axis=1)

    return nbrands

def get_range(cbg_brand_count):
    """
    input a edgelist of cbg, brands, and count as pd.dataframe,
    return the range of brand SES(median income of brand visiters) a pd.series
    """

    get_range = pd.merge(cbg_brand_count, brand_median, on = 'brands')
    get_range = get_range.groupby('cbg').agg({'median': (max, min)})
    get_range.columns = get_range.columns.droplevel(0)
    brand_range = get_range['max'] - get_range['min']

    return brand_range

def get_std(cbg_brand_count):
    """
    input a edgelist of cbg, brands, and count as pd.dataframe,
    return the std of brand SES(median income of brand visiters) a pd.series
    """

    get_std = pd.merge(cbg_brand_count, brand_median, on = 'brands')
    # repeating index to get the right std
    get_std = get_std.loc[get_std.index.repeat(get_std['count'])]
    brand_std = get_std.groupby('cbg')['median'].std()

    return brand_std

def get_entropy_brand(cbg_brand_count):
    """
    input a edgelist of cbg, brands, and count as pd.dataframe,
    return the entropy by brand visits
    """

    get_entropy = cbg_brand_count[:]
    cbg_visitors = get_entropy.groupby('cbg')['count'].transform('sum')
    get_entropy = get_entropy.assign(cbg_visitors = cbg_visitors)
    get_entropy = get_entropy.assign(pk = get_entropy['count'] / get_entropy['cbg_visitors'])
    get_entropy = get_entropy.groupby('cbg').agg({'pk': stats.entropy})
    entropy_brand = get_entropy['pk'] / np.log(len(cbg_brand_count['brands'].unique()))

    return entropy_brand

def get_nlevels(cbg_brand_count):
    """
    input a edgelist of cbg, brands, and count as pd.dataframe,
    return the number of price levels each cbg visits as pd.series
    """
    # get edgelist of cbg, yelp, count
    cbg_yelp = pd.merge(cbg_brand_count, yelp_labelled, on = 'brands')
    cbg_yelp = cbg_yelp[['cbg', 'yelp_dollar', 'count']]
    cbg_yelp = cbg_yelp.groupby(['cbg', 'yelp_dollar']).sum().reset_index()

    # get number of levels
    nlevels = cbg_yelp.groupby("cbg")['yelp_dollar'].size()

    return nlevels

def get_entropy_price(cbg_brand_count):
    """
    input a edgelist of cbg, brands, and count as pd.dataframe,
    return the number of price levels each cbg visits as pd.series
    """
    # get edgelist of cbg, yelp, count
    cbg_yelp = pd.merge(cbg_brand_count, yelp_labelled, on = 'brands')
    cbg_yelp = cbg_yelp[['cbg', 'yelp_dollar', 'count']]
    cbg_yelp = cbg_yelp.groupby(['cbg', 'yelp_dollar']).sum().reset_index()

    # get entropy
    cbg_visitors_yelp = cbg_yelp.groupby('cbg')['count'].transform('sum')
    cbg_yelp = cbg_yelp.assign(cbg_visitors = cbg_visitors_yelp)
    cbg_yelp = cbg_yelp.assign(pk = cbg_yelp['count'] / cbg_yelp['cbg_visitors'] )
    cbg_yelp = cbg_yelp.groupby('cbg').agg({'pk': stats.entropy})
    entropy_price = cbg_yelp['pk'] / np.log(4)

    return entropy_price

def get_diversity(selected_cbg_brand):
    """
    input the matrix of cbg and brands as pd.dataframe,
    return all measures of diversity as as dataframe
    """

    cbg_brand_count = get_cbg_brand_count(selected_cbg_brand)
    cbg_diversity = pd.DataFrame(index = selected_cbg_brand.index)
    cbg_diversity.index.names = ['cbg']
    cbg_diversity = cbg_diversity.assign(nbrands = get_nbrands(selected_cbg_brand),
                                         entropy_brand = get_entropy_brand(cbg_brand_count),
                                         brand_range = get_range(cbg_brand_count),
                                         brand_std = get_std(cbg_brand_count),
                                         nlevels = get_nlevels(cbg_brand_count),
                                         entropy_price = get_entropy_price(cbg_brand_count))
    return cbg_diversity

def get_3diversity(selected_cbg_brand):
    """
    input the matrix of cbg and brands as pd.dataframe,
    return income and the three measures of diversity to report
    """

    cbg_brand_count = get_cbg_brand_count(selected_cbg_brand)
    cbg_diversity = pd.DataFrame(index = selected_cbg_brand.index)
    cbg_diversity.index.names = ['cbg']
    cbg_diversity = cbg_diversity.assign(entropy_brand = get_entropy_brand(cbg_brand_count),
                                         brand_std = get_std(cbg_brand_count),
                                         entropy_price = get_entropy_price(cbg_brand_count))
    return cbg_diversity

def get_mobility(geo_df):
    """
    get mobility as mean distance travelled from geo_df
    """
    mobility = geo_df.groupby('visitor_home_cbgs').sum(numeric_only = True)
    # mobility measured as the mean distance travelled
    mobility = mobility.assign(mobility = mobility['sum_dist'] / mobility['cbg_visitor_count'])
    mobility = mobility['mobility']
    mobility.index.names = ['cbg']
    return mobility

def corr_table(df):
    """
    input a pandas dataframe
    output a correlation table of the dataframe with p-values as asterisks
    source: https://stackoverflow.com/a/49040342/12148092
    """
    rho = df.corr()
    pval = df.corr(method=lambda x, y: stats.pearsonr(x, y)[1]) - np.eye(*rho.shape)
    p = pval.applymap(lambda x: ''.join(['*' for t in [.05, .01, .001] if x<=t]))
    output = rho.round(3).astype(str) + p
    return output

def plot_income_diversity(income_diversity):
    """
    income-diversity plots
    """    

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharex = True, constrained_layout = True, figsize=(9.5, 3))
    axs = [ax1,ax2,ax3]
    x = income_diversity["income"]
    y = [income_diversity['entropy_brand'], income_diversity['brand_std'], income_diversity['entropy_price']]
    xlabels = ["income", "income", "income"]
    ylabels = ["entropy by brand visits", "standard deviation of brand SES", "entropy by price levels"]
    titles = ["a", "b", "c"]
    

    for i in range(len(axs)):
        axs[i].scatter(x, y[i], s = 5, alpha = 0.3)
        b, e = np.polyfit(x, y[i], 1)
        axs[i].plot(x, b*x + e, color="black", linewidth = 1.5)
        axs[i].set_xlabel(xlabels[i])
        axs[i].set_ylabel(ylabels[i])
        axs[i].set_title(titles[i])
        axs[i].xaxis.set_ticks(range(0, 300000, 50000))
        axs[i].set_xticklabels(["0", "50k", "100k", "150k", "200k", "250k"])

def plot_edu_diversity(edu_diversity):
    """
    education-diversity plots
    """    

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharex = True, constrained_layout = True, figsize=(9.5, 3))
    axs = [ax1,ax2,ax3]
    x = edu_diversity["bachelor_or_higher"]
    y = [edu_diversity['entropy_brand'], edu_diversity['brand_std'], edu_diversity['entropy_price']]
    xlabels = ["proportion of bachelor or higher", "proportion of bachelor or higher", "proportion of bachelor or higher"]
    ylabels = ["entropy by brand visits", "standard deviation of brand SES", "entropy by price levels"]
    titles = ["a", "b", "c"]
    

    for i in range(len(axs)):
        axs[i].scatter(x, y[i], s = 5, alpha = 0.3)
        b, e = np.polyfit(x, y[i], 1)
        axs[i].plot(x, b*x + e, color="black", linewidth = 1.5)
        axs[i].set_xlabel(xlabels[i])
        axs[i].set_ylabel(ylabels[i])
        axs[i].set_title(titles[i])
        axs[i].xaxis.set_ticks([0, 0.2, 0.4, 0.6, 0.8, 1])
        axs[i].set_xticklabels(["0", "0.2", "0.4", "0.6", "0.8", "1"])
