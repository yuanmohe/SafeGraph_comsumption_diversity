This repository contains codes and data related to the paper "High Socioeconomic Status is Associated with Diverse Consumption across Brands and Price Levels".

# Data

`selected_categories.csv`

- 28 NAICS four-digit categories we selected for this paper.

`selected_cbg_brand.csv`
- a matrix of the selected 13,653 CBGs and 924 brands, where the value means number of visits.

`brand_cat.csv`

- 1175 brands and their six-digit NAICS code, top_category (4-digit category names), and sub_category (6-digit category names).

`selected_cbg_stats.csv`
- relevant census data for the selected CBGs: income, income margine of error, proportion of bachelor or higher degree, weighted years of education, median age, proportion of male, proportion of white.

`yelp_labelled.csv`
- 924 brands and their labelled yelp price levels, combining data from Yelp Open Dataset and manual labelling.
- 148 brands with no data labelled as NA.

`brand_median.csv`
- median household incomes among the visitors of the 924 selected brands.

`cbg_diversity.csv`
- diversity measures for the selected 13,653 CBGs.

# Scripts

`utilities.py` functions for data cleaning.

`diversity_tools.py` functions for calculating and presenting diversity measures.

`01_data_cleaning.ipynb` processes the raw SafeGraph and Census data into what we need for the analysis.
- outputs: Appendix Table A1 and Figure A1
- aggregated data: `selected_cbg_brand.csv`, `brand_cat.csv`, `selected_cbg_stats.csv`

`02_yelp_data.ipynb` cleans yelp data.
- aggregated data: `yelp_labelled.csv`

`03_lasso_prediction.ipynb`  uses lasso regression analysis to predict the median household income of the CBGs.
- outputs: Appendix B.

`04_brand_distribution.ipynb` shows the distribution of brands’ SES for different Yelp price levels and the distribution of brand visitors’ CBG income for some typical brands.
- outputs: Figure 2 and Figure 3.
- aggregated data: brand_median.csv

`05_diversity.ipynb` calculates diversity measures and conduct initial analyses.
- outputs: Figure 4, Table 1 and Table 2.
- aggregated data: `cbg_diversity.csv`

`06_availability_mobility.ipynb` calculates the localavailability and mobility measures of the selected CBGs.
- aggregated data: `cbg_availability.csv`, `cbg_mobility.csv`
