# Boston Housing Price Prediction - Multivariable Regression Model

## Project Overview

A comprehensive machine learning project that builds a multivariable regression model to predict residential property prices in Boston, Massachusetts (1970s). This project demonstrates the application of linear regression and statistical analysis to real estate valuation, using various property characteristics to estimate home values.

## Business Context

Imagine working for a real estate development company in 1970s Boston. Before starting any residential project, the company needs accurate price estimates based on property characteristics. This model provides data-driven valuations using features such as number of rooms, proximity to employment centers, neighborhood socioeconomic factors, and local school quality.

## Dataset - Boston Housing Data

The classic Boston Housing dataset includes various features:

- **CRIM**: Per capita crime rate by town
- **ZN**: Proportion of residential land zoned for large lots
- **INDUS**: Proportion of non-retail business acres
- **CHAS**: Charles River proximity (1 if tract bounds river, 0 otherwise)
- **NOX**: Nitric oxides concentration (air quality)
- **RM**: Average number of rooms per dwelling
- **AGE**: Proportion of owner-occupied units built before 1940
- **DIS**: Weighted distances to employment centers
- **RAD**: Accessibility to radial highways
- **TAX**: Property tax rate per $10,000
- **PTRATIO**: Pupil-teacher ratio by town
- **B**: Proportion of residents of African American descent
- **LSTAT**: Percentage of lower status population
- **MEDV**: Median value of owner-occupied homes (TARGET)

## Key Questions Explored

- Which features have the strongest correlation with housing prices?
- Can we build an accurate model to predict home values?
- What is the relative importance of different property characteristics?
- Are there multicollinearity issues among features?
- How well does the model perform on test data?
- What are the model's limitations and assumptions?
- Which features contribute most to price predictions?

## Technologies Used

- **Python 3.14**
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computations
- **Scikit-learn** - Machine learning (Linear Regression, train-test split)
- **Seaborn** - Statistical visualizations and heatmaps
- **Plotly** - Interactive visualizations
- **Matplotlib** - Static plots and charts
- **SciPy** - Statistical analysis

## Project Structure

1. **Data Loading & Exploration**
   - Loading the Boston housing dataset
   - Initial data inspection and summary statistics
   - Understanding variable distributions

2. **Exploratory Data Analysis (EDA)**
   - Descriptive statistics
   - Distribution analysis of features
   - Identifying outliers

3. **Data Visualization**
   - Correlation heatmaps
   - Scatter plots and relationship analysis
   - Feature distribution plots

4. **Feature Analysis**
   - Correlation analysis
   - Multicollinearity detection
   - Feature importance assessment

5. **Data Preprocessing**
   - Train-test split
   - Feature scaling (if needed)
   - Handling any data quality issues

6. **Model Building**
   - Linear regression model construction
   - Multivariable regression implementation
   - Coefficient interpretation

7. **Model Evaluation**
   - R-squared score
   - Mean Squared Error (MSE)
   - Residual analysis
   - Model assumptions testing

8. **Results & Insights**
   - Feature importance rankings
   - Price predictions
   - Model limitations and recommendations

## Key Machine Learning Concepts

- **Multivariable Linear Regression**: Using multiple features to predict a continuous target
- **Feature Correlation**: Understanding relationships between variables
- **Model Evaluation**: Assessing prediction accuracy
- **Overfitting/Underfitting**: Balancing model complexity
- **Residual Analysis**: Validating model assumptions

## Statistical Analysis Includes

- Pearson correlation coefficients
- Variance Inflation Factor (VIF) for multicollinearity
- Regression diagnostics
- Confidence intervals
- Hypothesis testing for coefficients

## How to Run

1. Clone this repository
2. Install required packages:
   ```
   pip install pandas numpy scikit-learn seaborn plotly matplotlib scipy
   ```
3. Ensure you have the `boston.csv` file
4. Run the Jupyter notebook: `jupyter notebook Multivariable_Regression_and_Valuation_Model.ipynb`

**Note for Google Colab users**: Uncomment and run the plotly upgrade cell at the beginning of the notebook.

## Model Performance

_(Results will be based on your specific implementation)_

- Training R² Score: [To be determined]
- Testing R² Score: [To be determined]
- RMSE: [To be determined]
- Most Important Features: [To be determined]

## Real-World Applications

This project demonstrates skills applicable to:

- Real estate price prediction
- Property valuation models
- Investment analysis
- Urban planning and development
- Risk assessment for mortgages and loans

## Limitations & Considerations

- Data is from 1970s Boston - may not generalize to modern markets
- Linear assumptions may not capture all relationships
- Some features (like racial composition) reflect historical biases
- External factors (economic conditions, market sentiment) not included

## Author

A machine learning project demonstrating regression modeling for real estate valuation