# Dr. Semmelweis and the Discovery of Handwashing

## Project Overview

A data-driven investigation into Dr. Ignaz Semmelweis's groundbreaking discovery in the 1840s that handwashing could dramatically reduce maternal mortality rates in childbirth. This project recreates the statistical analysis that led to one of the most important medical discoveries in history, demonstrating the power of data in challenging established medical practices.

## Historical Context

Dr. Ignaz Semmelweis (1818-1865) was a Hungarian physician working at the Vienna General Hospital. In the mid-1800s, many women were dying from childbed fever (puerperal fever) after giving birth. At the time, illness was thought to be caused by "bad air" or evil spirits. Dr. Semmelweis noticed that the mortality rate was much higher in the clinic staffed by doctors and medical students compared to the clinic staffed by midwives. Through careful observation and data analysis, he discovered that handwashing with chlorinated lime solution could prevent these deaths.

## Dataset

- **Source**: Dr. Semmelweis's original research published in 1861
- **Original Text**: [German version](http://www.deutschestextarchiv.de/book/show/semmelweis_kindbettfieber_1861)
- **English Translation**: [Full text available](http://graphics8.nytimes.com/images/blogs/freakonomics/pdf/the%20etiology,%20concept%20and%20prophylaxis%20of%20childbed%20fever.pdf)
- **Files**:
  - `annual_deaths_by_clinic.csv` - Yearly death statistics by clinic
  - `monthly_deaths.csv` - Monthly death rates with temporal data

## Key Questions Explored

- What was the mortality rate difference between the two clinics?
- When did Dr. Semmelweis introduce handwashing, and what was the immediate impact?
- How significant was the reduction in mortality rates after handwashing was introduced?
- Are the results statistically significant?
- What can we learn about the importance of data-driven medical practices?
- How does this historical data analysis demonstrate the scientific method?

## Technologies Used

- **Python 3.13**
- **Pandas** - Data manipulation and time series analysis
- **NumPy** - Numerical computations
- **Plotly** - Interactive visualizations
- **Seaborn** - Statistical visualizations
- **Matplotlib** - Time series plots with date formatting
- **SciPy** - Statistical hypothesis testing

## Project Structure

1. **Historical Context** - Understanding the problem
2. **Data Loading** - Reading annual and monthly death records
3. **Exploratory Analysis** - Initial investigation of mortality rates
4. **Clinic Comparison** - Analyzing differences between clinics
5. **Temporal Analysis** - Identifying when handwashing was introduced
6. **Impact Analysis** - Measuring the effect of handwashing intervention
7. **Statistical Testing** - Confirming the significance of findings
8. **Visualization** - Creating compelling time series visualizations

## Key Findings

This analysis reveals:

- The dramatic difference in mortality rates between the two clinics
- The precise moment when handwashing was introduced (1847)
- The immediate and substantial reduction in deaths after the intervention
- Statistical evidence proving the effectiveness of handwashing
- A tragic historical lesson about resistance to evidence-based medicine

## Statistical Analysis

The project includes:

- Mortality rate calculations by clinic and time period
- Before/after comparison of handwashing intervention
- Statistical hypothesis testing (t-tests)
- Time series analysis with proper date formatting
- Confidence intervals and significance levels

## How to Run

1. Clone this repository
2. Install required packages: `pip install pandas numpy plotly seaborn matplotlib scipy`
3. Ensure you have both CSV files: `annual_deaths_by_clinic.csv` and `monthly_deaths.csv`
4. Run the Jupyter notebook: `jupyter notebook Dr_Semmelweis_Handwashing_Discovery__start_.ipynb`

**Note for Google Colab users**: Uncomment and run the plotly upgrade cell at the beginning of the notebook.

## Historical Significance

Despite overwhelming evidence, Dr. Semmelweis's findings were largely rejected by the medical community during his lifetime. He died in 1865 at age 47, ironically from an infection. Today, he is recognized as a pioneer of antiseptic procedures and evidence-based medicine. His story reminds us of the importance of data analysis in medical science and the challenges of changing established practices.

## Author

A data science project recreating one of medicine's most important statistical analyses

## References

- Semmelweis, I. (1861). Die Aetiologie, der Begriff und die Prophylaxis des Kindbettfiebers.
- Historical data from Vienna General Hospital records
