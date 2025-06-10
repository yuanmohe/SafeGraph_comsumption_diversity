This repository contains codes and data related to the paper "High Socioeconomic Status is Associated with Diverse Consumption across Brands and Price Levels".

# Steps

`01_data_cleaning.ipynb` processes the raw SafeGraph and census data into what we need for the analysis.
- output Appendix Table 1A

`02_cbg_brand.ipynb` filters out brands with fewer than 100 incoming visitors and the CBGs with fewer than 100 outgoing visitors, checks the distribution of median household income of all vs selected CBGs, and uses lasso regression analysis to predict the median household income of the CBGs.
- output Appendix Figure 1A, Appendix B

`03_yelp_data.ipynb` cleans yelp data.

`04_brand_distribution.ipynb` shows the distribution of brands’ SES for different Yelp price levels and the distribution of brand visitors’ CBG income for some typical brands.
- output Figure 2 and Figure 3.



../SafeGraph_new/