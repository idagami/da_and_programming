# Space Missions Analysis - The Space Race and Beyond

## Project Overview
A comprehensive analysis of all space missions from the dawn of the Space Age in 1957 to the present day. This project explores the history of space exploration, examining mission success rates, launching organizations, rocket technology evolution, and the geopolitical dynamics of the Space Race between the USA and Soviet Union, extending through to modern commercial space ventures.

## Historical Context
The Space Race began in 1957 with the Soviet Union's launch of Sputnik 1, the first artificial satellite. This project chronicles over six decades of human space exploration, from early satellite launches and the Apollo moon landings to modern commercial spaceflight and international cooperation in space.

## Dataset
- **Source**: Scraped from [Next Spaceflight](https://nextspaceflight.com/launches/past/?page=1)
- **Time Period**: 1957 - Present
- **Coverage**: All documented space missions worldwide
- **Features**: 
  - Mission dates and locations
  - Launching organizations and countries
  - Rocket types and specifications
  - Mission status (Success/Failure)
  - Mission costs and details

## Key Questions Explored
- How has the frequency of space launches changed over time?
- Which countries have been most active in space exploration?
- What are the success rates of different space agencies?
- How has rocket technology evolved over the decades?
- What is the relationship between the Cold War and space launch activity?
- Which organizations dominate modern commercial spaceflight?
- What are the trends in space mission costs?
- How do success rates vary by country, organization, and rocket type?
- What patterns exist in launch site locations?
- How has international cooperation in space evolved?

## Technologies Used
- **Python 3.x**
- **Pandas** - Data manipulation and time series analysis
- **NumPy** - Numerical computations
- **Plotly** - Interactive visualizations and geographic maps
- **Matplotlib** - Historical trend visualizations
- **Seaborn** - Statistical plots
- **iso3166** - Country code standardization
- **datetime** - Temporal analysis

## Project Structure
1. **Data Loading & Preparation**
   - Loading mission data
   - Date parsing and conversion
   - Country code standardization

2. **Exploratory Data Analysis**
   - Mission frequency over time
   - Success rate analysis
   - Organization and country statistics

3. **Temporal Analysis**
   - Space Race timeline (USA vs USSR/Russia)
   - Decade-by-decade trends
   - Modern era commercial space activity

4. **Geographic Analysis**
   - Launch sites by country
   - International collaboration patterns
   - Geographic distribution of space activity

5. **Organization Analysis**
   - Government agencies (NASA, Roscosmos, ESA, CNSA, ISRO, etc.)
   - Commercial companies (SpaceX, Blue Origin, Rocket Lab, etc.)
   - Success rates by organization

6. **Technology Analysis**
   - Rocket family evolution
   - Reliability improvements over time
   - Cost trends

7. **Mission Status Analysis**
   - Success vs. failure rates
   - Failure analysis by decade
   - Improvements in reliability

## Key Historical Periods Covered
- **Space Race Era (1957-1991)**: US-Soviet competition
- **Post-Cold War (1991-2000s)**: International cooperation
- **Commercial Space Era (2010s-present)**: Private sector emergence

## Visualizations Include
- Time series of launches by country
- Interactive choropleth maps showing space-faring nations
- Success rate trends over time
- Organization comparison charts
- Rocket family evolution timelines
- Launch site geographic distributions
- Cost analysis visualizations

## Notable Insights
*(Analysis reveals patterns such as)*
- The peak of Space Race activity in the 1960s-70s
- Decline in missions after Cold War
- Recent surge due to commercial spaceflight
- Increasing international participation
- Improving success rates over time
- Emergence of new space-faring nations

## How to Run
1. Clone this repository
2. Install required packages:
   ```
   pip install pandas numpy plotly matplotlib seaborn iso3166
   ```
3. Ensure you have the `mission_launches.csv` file
4. Run the Jupyter notebook: `jupyter notebook Space_Missions_Analysis.ipynb`

**Note for Google Colab users**: Uncomment and run the plotly upgrade cell at the beginning of the notebook.

## Data Considerations
- Data scraped from public sources may have inconsistencies
- Some historical mission details may be incomplete
- Classification of success/failure may vary by source
- Cost data may not be available for all missions, especially historical ones

## Real-World Applications
This analysis demonstrates:
- Historical data analysis techniques
- Geopolitical event impact on technology
- Success rate and reliability metrics
- Time series forecasting potential
- Competitive analysis between organizations

## Future Enhancements
Potential extensions of this project:
- Predictive modeling for future launch trends
- Payload analysis (satellites, crewed missions, cargo)
- Economic impact assessment
- Environmental considerations of launches
- Detailed failure analysis and lessons learned

## Author
A data science project exploring humanity's journey to space

## Acknowledgments
- Data sourced from Next Spaceflight
- Historical context from various space agency archives
- Country standardization using ISO 3166 standards

## References
- NASA Historical Archive
- European Space Agency (ESA)
- Roscosmos
- Commercial space company public data
