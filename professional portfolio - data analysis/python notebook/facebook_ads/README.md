# Facebook Ads Campaign Performance Analysis

## Project Overview

A comprehensive analysis of Facebook advertising campaign performance, examining key metrics such as Cost Per Click (CPC), Cost Per Mille/Thousand Impressions (CPM), Click-Through Rate (CTR), and Return on Marketing Investment (ROMI). This project demonstrates how to evaluate digital marketing effectiveness using data-driven insights to optimize ad spend and campaign strategy.

## Business Context

Digital advertising requires careful monitoring and analysis to maximize ROI. This project analyzes Facebook ad campaign data to understand what drives successful campaigns, identify underperforming ads, and provide actionable recommendations for improving marketing effectiveness.

## Dataset

- **Source**: Facebook Ads campaign data
- **File**: `facebook_ads_data (2.0).csv`
- **Period**: Custom date range with daily campaign performance
- **Features**:
  - Campaign names and identifiers
  - Ad dates
  - Total spend per campaign
  - Total value (conversions/revenue)
  - Total impressions
  - Total clicks
  - Calculated metrics (CPC, CPM, CTR, ROMI)

## Key Metrics Analyzed

### Primary KPIs

- **CPC (Cost Per Click)**: Total spend ÷ Total clicks
- **CPM (Cost Per Mille)**: (Total spend × 1000) ÷ Total impressions
- **CTR (Click-Through Rate)**: Total clicks ÷ Total impressions
- **ROMI (Return on Marketing Investment)**: (Total value - Total spend) ÷ Total spend

### Analysis Dimensions

- Campaign-level performance
- Daily performance trends
- Time-based patterns
- Cross-metric correlations

## Key Questions Explored

- Which campaigns deliver the best ROI?
- How do different campaigns compare in terms of cost efficiency?
- What is the relationship between spend and conversion value?
- Are there temporal patterns in campaign performance?
- Which campaigns have the highest engagement (CTR)?
- How does spending correlate with impressions and clicks?
- What is the optimal campaign strategy based on performance data?
- Are there diminishing returns as spend increases?

## Technologies Used

- **Python 3.x**
- **Pandas** - Data manipulation and aggregation
- **NumPy** - Numerical computations
- **Matplotlib** - Data visualization
- **Seaborn** - Statistical visualizations and correlation analysis

## Project Structure

1. **Data Loading & Preparation**
   - Loading campaign data
   - Date parsing and conversion
   - Initial data inspection

2. **Data Cleaning**
   - Handling missing values
   - Data type conversions
   - Outlier detection

3. **Metric Calculation**
   - Computing CPC, CPM, CTR, ROMI
   - Campaign-level aggregations
   - Daily performance metrics

4. **Exploratory Data Analysis**
   - Descriptive statistics
   - Distribution analysis
   - Campaign comparisons

5. **Temporal Analysis**
   - Daily performance trends
   - Time-based patterns
   - Performance over campaign duration

6. **Campaign Performance Analysis**
   - Grouping by campaign name
   - Comparative performance metrics
   - Identifying top and bottom performers

7. **Correlation Analysis**
   - Correlation matrix creation
   - Heatmap visualization
   - Relationship identification between metrics

8. **Regression Analysis**
   - Scatter plots with trend lines
   - Spend vs. value relationship
   - Linear regression modeling (using Seaborn's lmplot)

9. **Insights & Recommendations**
   - Best performing campaigns
   - Optimization opportunities
   - Budget allocation suggestions

## Analytical Techniques

### Aggregation Strategies

- Grouping by campaign name
- Daily aggregation (grouped_days_21)
- Multi-level grouping for detailed analysis

### Statistical Methods

- Correlation analysis (excluding self-correlations)
- Linear regression for spend-value relationships
- Distribution analysis
- Comparative statistics

### Visualization Methods

- Correlation heatmaps (with coolwarm color scheme)
- Scatter plots with regression lines
- Time series plots
- Campaign comparison charts

## Code Highlights

### Metric Calculations

```python
grouped_camp["cpc"] = grouped_camp["total_spend"] / grouped_camp["total_clicks"]
grouped_camp["cpm"] = (grouped_camp["total_spend"] * 1000) / grouped_camp["total_impressions"]
grouped_camp["ctr"] = grouped_camp["total_clicks"] / grouped_camp["total_impressions"]
grouped_camp["romi"] = (grouped_camp["total_value"] - grouped_camp["total_spend"]) / grouped_camp["total_spend"]
```

### Correlation Analysis

```python
# Remove self-correlations for clearer heatmap
corr_matrix = fb_camp.corr(numeric_only=True)
corr_no_self = corr_matrix.copy()
for col in corr_no_self.columns:
    corr_no_self.loc[col, col] = np.nan
```

## How to Run

1. Clone this repository
2. Install required packages:
   ```
   pip install pandas numpy matplotlib seaborn
   ```
3. Update file path in the notebook to your local path or use relative path
4. Ensure you have the `facebook_ads_data (2.0).csv` file
5. Run the Jupyter notebook: `jupyter notebook HW_4-6_B_corrected.ipynb`

## Expected Outputs

- Campaign performance summary tables
- Correlation heatmaps showing metric relationships
- Regression plots showing spend vs. value
- Comparative analysis of campaign effectiveness
- Recommendations for campaign optimization

## Key Insights

_(Based on your specific analysis, typical findings might include)_

- High-performing vs. low-performing campaigns
- Optimal CPC and CPM ranges
- CTR benchmarks
- ROMI leaders
- Spend efficiency patterns
- Best times/days for ad performance

## Business Applications

This analysis framework can be used for:

- **Campaign Optimization**: Identifying which campaigns to scale or pause
- **Budget Allocation**: Directing spend to highest-performing campaigns
- **A/B Testing Analysis**: Comparing campaign variants
- **Performance Benchmarking**: Setting KPI targets
- **ROI Forecasting**: Predicting returns based on spend
- **Strategic Planning**: Data-driven marketing decisions

## Best Practices Demonstrated

- Systematic metric calculation
- Multi-level data aggregation
- Correlation analysis without redundancy
- Visual regression analysis
- Time-based performance tracking
- Campaign-level comparative analysis

## Limitations & Considerations

- Analysis based on historical data (may not predict future performance)
- External factors (seasonality, market conditions) not included
- Attribution models may vary
- Facebook's algorithm changes over time
- Audience targeting details not included in this dataset

## Future Enhancements

Potential extensions:

- Audience segmentation analysis
- Creative performance analysis (ad copy, images)
- Predictive modeling for campaign success
- Budget optimization algorithms
- Multi-platform comparison (Facebook vs. other channels)
- Lifetime value (LTV) integration

## Author

A digital marketing analytics project demonstrating Facebook Ads campaign optimization

## Tools & Libraries

- Jupyter Notebook for interactive analysis
- Pandas for data manipulation
- Seaborn for advanced visualizations
- NumPy for numerical operations
- Matplotlib for custom plots
