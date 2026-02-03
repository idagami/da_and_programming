# Fatal Force - Analysis of Police Shootings in the United States

## Project Overview

A comprehensive data analysis of fatal police shootings in the United States, examining patterns in demographics, geography, socioeconomic factors, and trends over time. This project uses The Washington Post's database to understand the circumstances and patterns surrounding police use of deadly force, exploring correlations with poverty rates, education levels, and racial demographics.

## Dataset Source

Since January 1, 2015, [The Washington Post](https://www.washingtonpost.com/) has been compiling a database of every fatal shooting in the US by a police officer in the line of duty. The database tracks more than a dozen details about each incident, including:

- Race, age, and gender of the deceased
- Whether the person was armed (and with what type of weapon)
- Location of the incident
- Whether the person showed signs of mental illness
- Whether body cameras or other recording devices were present
- Date and circumstances of the shooting

## Additional Datasets

The analysis incorporates socioeconomic data to provide context:

- **Median Household Income by City (2015)**
- **Percentage of People Below Poverty Level**
- **Percentage Over 25 Who Completed High School**
- **Racial Demographics by City**

## Key Questions Explored

- How many fatal police shootings occur annually in the US?
- What are the demographic characteristics of people killed by police?
- Is there a correlation between fatal shootings and poverty rates?
- How does education level relate to police shooting rates?
- Are there racial disparities in police shooting victims?
- What geographic patterns exist (by state, city, region)?
- What proportion of victims were armed, and with what weapons?
- How do mental health factors correlate with fatal encounters?
- Are there temporal trends or patterns over time?
- What is the relationship between median income and shooting rates?

## Technologies Used

- **Python 3.x**
- **Pandas** - Data manipulation and merging multiple datasets
- **NumPy** - Numerical analysis
- **Plotly** - Interactive visualizations and choropleth maps
- **Matplotlib** - Statistical plots and time series
- **Seaborn** - Correlation heatmaps and distribution plots
- **Scikit-learn** - Linear regression for correlation analysis
- **SciPy** - Statistical testing
- **Collections (Counter)** - Frequency analysis

## Project Structure

1. **Data Loading & Cleaning**
   - Loading police shooting data
   - Loading socioeconomic datasets
   - Data cleaning and standardization
   - Handling missing values

2. **Exploratory Data Analysis**
   - Victim demographics (age, race, gender)
   - Temporal patterns and trends
   - Armed vs. unarmed incidents
   - Mental illness indicators

3. **Geographic Analysis**
   - State-by-state comparison
   - Urban vs. rural patterns
   - Regional variations
   - Interactive mapping

4. **Socioeconomic Correlation Analysis**
   - Poverty rate correlations
   - Education level relationships
   - Income disparities
   - Racial demographic patterns

5. **Statistical Analysis**
   - Regression modeling
   - Correlation coefficients
   - Hypothesis testing
   - Confidence intervals

6. **Trend Analysis**
   - Year-over-year changes
   - Monthly and seasonal patterns
   - Long-term trends

7. **Comprehensive Reporting**
   - Key findings summary
   - Data limitations discussion
   - Contextual interpretation

## Analytical Techniques

- **Regression Analysis**: Examining relationships between shootings and socioeconomic factors
- **Correlation Studies**: Understanding variable relationships
- **Time Series Analysis**: Identifying temporal patterns
- **Demographic Analysis**: Breaking down by race, age, gender
- **Geographic Visualization**: Mapping incident distributions
- **Statistical Significance Testing**: Validating findings

## How to Run

1. Clone this repository
2. Install required packages:
   ```
   pip install pandas numpy plotly matplotlib seaborn scikit-learn scipy
   ```
3. Ensure you have all required CSV files:
   - Fatal shooting data
   - `Median_Household_Income_2015.csv`
   - `Pct_People_Below_Poverty_Level.csv`
   - `Pct_Over_25_Completed_High_School.csv`
   - Racial demographic data

4. Run the Jupyter notebook: `jupyter notebook Fatal_Force.ipynb`

**Note for Google Colab users**: Uncomment and run the plotly upgrade cell at the beginning of the notebook.

## Important Considerations

### Data Limitations

- Reporting may be incomplete or inconsistent across jurisdictions
- Not all police departments report data uniformly
- Definitions of "armed" or "signs of mental illness" may vary
- Socioeconomic data may not align perfectly with incident locations
- Causation cannot be inferred from correlation

### Ethical Considerations

This analysis deals with sensitive subject matter involving loss of life. The goal is to:

- Understand patterns objectively using data
- Identify systemic issues that may need addressing
- Inform evidence-based policy discussions
- Honor the lives lost by seeking meaningful insights

This is not meant to:

- Make political statements
- Assign blame to individuals or groups
- Oversimplify complex social issues
- Draw definitive causal conclusions from correlational data

### Context Matters

Raw numbers and statistics require careful interpretation within broader social, historical, and systemic contexts. This analysis aims to contribute to informed discussion while acknowledging the complexity of the issues involved.

## Key Findings

_(Results based on your specific analysis)_

The analysis may reveal:

- Demographic patterns in police shooting victims
- Geographic hotspots or variations
- Correlations with poverty and education
- Trends over time
- Armed vs. unarmed incident proportions

## Real-World Impact

Understanding these patterns can inform:

- Police training and policy reforms
- Community-police relations initiatives
- Mental health crisis intervention programs
- Evidence-based policy discussions
- Resource allocation for prevention

## Author

A data science project examining police use of deadly force in the United States

## Data Sources & Acknowledgments

- **The Washington Post**: Fatal Force database
- **US Census Bureau**: Socioeconomic data
- Various civic data sources for demographic information

## References

- The Washington Post Fatal Force Database
- Academic research on police use of force
- Criminal justice statistics
- Public health literature on violence prevention
