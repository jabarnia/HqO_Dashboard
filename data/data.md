# DATA SOURCE

## Step 1
Raw data is a sql table with attributes such as location (lat/long), a code
representing the city, building population, area, number of each type of tennant 
(type of business), type and number of amenities, and a code for each building which is our foreign key.

A second table including data gathered from user input (tennant satisfaction and 
important factors), and data collected from the application (user engagemnet per
building, etc) will be pulled from the same data base, updated periodically 
and synced with the base.

These two tables should be inner-merged to create our df_building - First step is to drop any buidlings that are test data, along with those that are 
not activated yet or are missing location information.

## Step 2
With the "Location_API" function, a new data frame should be created for each
building, tied to the building code. Summary of this data base will be added to
the df_buildings - new columns are: number of each business (restaurant/ cafe/ 
bar/ gym), their average price point (scale is 1-4) and average rating (scale is 
0 to 5)

## Step 3
- user forecasts for this month: average users per day in the current month, and 
multiply by length of this month in days to add the column 'this_month_forecast' 
to the df_buildings
- A Kmeans model shall be applied to a normalized version of df_buildings to 
cluster our buildings. Number of groups should be tested out to find a grouping 
that makes sense both intuitively and per model score. The label from this model 
should be added to df_buildings.
- A regression model shall be applied to a normalized version of some of the 
columns df_buildings with the target being "tennant satisfaction". Selected 
columns should be the ones that represent the amenities that *can* be updated or 
changed by the landlord. Coefficients from this model should be recorded.

## Final Step
This dataframe is what we are going to use for our dashboard. Ref app.py for next steps.
