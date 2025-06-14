This repository contains code and data related to the paper "High Socioeconomic Status is Associated with Diverse Consumption across Brands and Price Levels".

The data that support the findings of this study are available from [SafeGraph](https://www.safegraph.com/). Restrictions apply to the availability of these data, which were used under license for the current study and are not publicly available. Here, we provide the processed data and codes to reproduce the results in the paper.

# Scripts

`utilities.py` functions for data cleaning.

`diversity_tools.py` functions for calculating and presenting diversity measures.

`01_data_cleaning.ipynb` processes the raw SafeGraph and Census data into what we need for the analysis.
- outputs: Appendix Table A1 and Figure A1
- aggregated data: selected_cbg_brand.csv, selected_brands.csv, brand_cat.csv, selected_cbg_stats.csv, covisit_edgelist.csv

`02_yelp_data.ipynb` cleans Yelp data.
- aggregated data: yelp_labelled.csv

`03_lasso_prediction.ipynb`  uses lasso regression analysis to predict the median household income of the CBGs.
- outputs: Appendix B.

`04_brand_distribution.ipynb` shows the distribution of brands’ SES for different Yelp price levels and the distribution of brand visitors’ CBG income for some typical brands.
- outputs: Figure 2 and Figure 3.
- aggregated data: brand_median.csv

`05_diversity.ipynb` calculates diversity measures and conducts initial analyses.
- outputs: Figure 4, Table 1 and Table 2.
- aggregated data: cbg_diversity.csv, selected_brand_cat3d.csv

`06_availability_mobility.ipynb` calculates the local availability and mobility measures of the selected CBGs.
- aggregated data: availability_matrix.csv, cbg_availability.csv, geo_df.csv, cbg_mobility.csv

`07_diversity_regressions.ipynb` conducts regression analyses predicting consumption diversity using income and confounding variables.
- outputs: Table 3 and Appendix C.

`08_node2vec_present.ipynb` uses brand co-visits and node2vec to have a rough test of niche consumption.
- outputs: Appendix D.

`09_edu_lasso.ipynb` replicates the lasso regression analysis using education (proportion of bachelor's degree or higher) as the outcome variable.
- outputs: Appendix Figure E1.

`10_edu_distribution.ipynb` replicates the brand distribution analysis using education.
- outputs: Appendix Figure E2 and E3.

`11_edu_diversity.ipynb` replicates the diversity analysis using education.
- outputs: Appendix Figure E4, Table E1 and Table E2.

`12_interaction_regressions.ipynb` conducts regression analyses predicting consumption diversity using income, education, their interaction, and confounding variables.
- outputs: Appendix Table E3, E4, E5, and E6; Figure E5.


# Data

`selected_categories.csv`

- 28 NAICS four-digit categories we selected for this paper.

`selected_cbg_brand.csv`
- a matrix of the selected 13,653 CBGs and 924 brands, where the value means the number of visits.

`selected_brands.csv`
- 924 brands selected for this paper.

`brand_cat.csv`

- 1175 brands and their six-digit NAICS code, top_category (4-digit category names), and sub_category (6-digit category names).

`selected_cbg_stats.csv`
- relevant census data for the selected CBGs: income, income margin of error, proportion of bachelor's or higher degree, weighted years of education, median age, proportion of males, proportion of whites.

`covisit_edgelist.csv`
- an edgelist of co-visits between brands, where each row contains a brand, a co-visited brand, and the proportion of visits to the first brand that also visited the second brand in the same month.

`yelp_labelled.csv`
- 924 brands and their labelled Yelp price levels, combining data from the Yelp Open Dataset and manual labelling.
- 148 brands with no data labelled as NA.

`brand_median.csv`
- median household incomes among the visitors of the 924 selected brands.

`cbg_diversity.csv`
- diversity measures for the selected 13,653 CBGs.

`selected_brand_cat3d.csv`
- 924 brands and their 3-digit NAICS code and 3-digit category names. 

`availability_matrix.csv`
- intermediate data for calculating availability measures (a matrix of CBGs and brands, where the value means the number of brands available in the CBG).

`cbg_availability.csv`
- local availability measures for the selected 13,653 CBGs.

`geo_df.csv`
- intermediate data for calculating mobility measures (a dataframe of brands, visitor home CBGs, CBG visitor numbers, and sum distance travelled).

`cbg_mobility.csv`
- mobility measures for the selected 13,653 CBGs.
