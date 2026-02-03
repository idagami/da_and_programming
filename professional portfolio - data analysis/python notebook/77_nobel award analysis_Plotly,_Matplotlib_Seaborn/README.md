# Nobel Prize Analysis

## Project Overview

An in-depth analysis of Nobel Prize winners from 1901 to present, exploring patterns in laureate demographics, country distributions, prize categories, and historical trends. This project investigates the evolution of Nobel Prize awards and reveals insights about scientific achievement and recognition across different nations and time periods.

## Historical Context

On November 27, 1895, Alfred Nobel signed his last will in Paris, leaving much of his wealth to establish prizes "to those who, during the preceding year, have conferred the greatest benefit to humankind." The Nobel Prize is awarded annually in Chemistry, Physics, Physiology or Medicine, Literature, Peace, and Economic Sciences.

## Dataset

- **Source**: Nobel Prize official records
- **Time Period**: 1901 - Present
- **Categories**: Chemistry, Physics, Physiology or Medicine, Literature, Peace, and Economic Sciences
- **Note**: Birth dates for some laureates (Michael Houghton, Venkatraman Ramakrishnan, Nadia Murad) are estimated as July 2nd (mid-year)

## Key Questions Explored

- How has the distribution of Nobel Prizes changed over time?
- Which countries have produced the most Nobel laureates?
- What are the gender demographics of Nobel Prize winners?
- What is the average age of Nobel Prize recipients in different categories?
- Are there trends in which categories receive more awards over time?
- How long does it take between a discovery and receiving the Nobel Prize?
- What is the distribution of prizes among different fields of study?

## Technologies Used

- **Python 3.13**
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computations
- **Plotly** - Interactive visualizations
- **Seaborn** - Statistical data visualization
- **Matplotlib** - Static plots and charts

## Project Structure

1. **Data Loading & Initial Exploration** - Understanding the dataset
2. **Data Cleaning & Preprocessing** - Handling dates and missing values
3. **Temporal Analysis** - Prize distribution over time
4. **Geographic Analysis** - Country-wise distribution of laureates
5. **Demographic Analysis** - Age and gender patterns
6. **Category Analysis** - Comparing different Nobel Prize categories
7. **Advanced Insights** - Correlations and unique patterns

## Visualizations

The project includes various interactive and static visualizations:

- Time series of prize awards by category
- Geographic distribution maps
- Age distribution histograms
- Gender representation over time
- Country rankings and trends

## How to Run

1. Clone this repository
2. Install required packages: `pip install pandas numpy plotly seaborn matplotlib`
3. Ensure you have the `nobel_prize_data.csv` file
4. Run the Jupyter notebook: `jupyter notebook Nobel_Prize_Analysis__start_.ipynb`

**Note for Google Colab users**: Uncomment and run the plotly upgrade cell at the beginning of the notebook.

## Insights

This analysis reveals fascinating patterns in scientific achievement, including historical biases, geographic concentrations of scientific excellence, and the evolution of Nobel Prize recognition across different fields.

## Author

A data science project exploring the legacy and patterns of Nobel Prize awards

## Acknowledgments

Data based on official Nobel Prize records and historical documentation
