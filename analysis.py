# %%
import pandas as pd
import numpy as np
    
arrests_all = pd.read_csv('/Users/franco/Documents/Projects/Real Arrests/Data/arrests.csv')

# %%
# There is a RIDICULOUS amount of data here. Too much for a local machine to take 
# If we are to do anything. Let's be sensible and filter out everything before 2018.

arrests_all['Arrest Date'] = pd.to_datetime(arrests_all['Arrest Date'])
arrests_2018 = arrests_all[arrests_all['Arrest Date'] >= '2018-01-01']

arrests_2018.to_csv('arrests_2018.csv', encoding='utf-8', index=False)

# I will now load this into R (where I personally think it's easier to work with shapefiles)
# and tie in council districts with where the arrests occured.

# %%
# Load in the new dataset with the council districts.
arrests = pd.read_csv('/Users/franco/Documents/Projects/Real Arrests/Data/arrest_filtered.csv')


# %%
# See which district holds the most arrests.
arrests = arrests.drop(columns = ['Unnamed: 0'])
arrests = arrests[arrests.CouncilID != 'numeric(0)']
arrests['CouncilID'] = arrests['CouncilID'].apply(pd.to_numeric)

# %%
arrests['CouncilID'].value_counts()

#%%
import seaborn as sns 
import matplotlib
import matplotlib.pyplot as plt

sns.set_style('white')
plt.rcParams['figure.figsize'] = [8,4]
sns.countplot('CouncilID', data = arrests)
plt.xlabel('Council District')
plt.ylabel('')
plt.title('Number of Arrests for Each Council District')


# %%
# Load in income data.
income = pd.read_csv('/Users/franco/Documents/Projects/Real Arrests/Data/medianincome.csv')

# %%
print(type(income['council_district'][0]))
income = income[income['council_district'] != 'CITY TOTAL']
income['council_district'] = income['council_district'].apply(pd.to_numeric)

# %%
incomeandid = income[['council_district', 'value']]
incomeandid.columns = ['council_district', 'Median Income']
incomeandid = incomeandid.sort_values(by=['council_district']).reset_index(drop = True)
incomeandid

# %%
# Now plot both the income and the number of arrests on top of each other.
fig = plt.figure()
ax = sns.countplot('CouncilID', data = arrests)
ax2 = ax.twinx()
ax2.plot(ax.get_xticks(), incomeandid['Median Income'], marker = 'o')
ax2.set(ylabel = 'Median Income')
ax.set(xlabel = 'Council District', ylabel = 'Arrests', title = 'Number of Arrests per Council District')

# %%
# Look at the number of arrests relative to the population.
population = pd.read_csv('/Users/franco/Documents/Projects/Real Arrests/Data/population.csv')
popandid = population[['council_district', 'value']]

# %%
popandid['council_district'] = popandid['council_district'].apply(pd.to_numeric)
popandid = popandid.sort_values(by=['council_district']).reset_index(drop = True)
popandid

# %%
sns.barplot(x = 'council_district', y = 'value', data = popandid)
plt.xlabel('Council Districts')
plt.ylabel('')
plt.title('Population for the Council Districts')

# %%
# Make Race easier to work with.
ethnicities = {
    'A': 'Asian',
    'B': 'Black',
    'C': 'Asian',
    'D': 'Asian',
    'F': 'Asian',
    'G': 'Pacific Islander',
    'H': 'Hispanic',
    'I': 'Native',
    'J': 'Asian',
    'K': 'Asian',
    'L': 'Asian',
    'O': 'Other',
    'P': 'Pacific Islander',
    'S': 'Pacific Islander',
    'U': 'Pacific Islander',
    'V': 'Asian',
    'W': 'White',
    'X': 'Unknown',
    'Z': 'Asian'
    
}

# So what I did is make groups of ethnicities. For example, Filipino and Cambodian
# are listed separately but both are still technically Asian. 
# Another important note, Hawaiians, Guamanians, and Samoans I also grouped into
# Pacific Islander which may or may not be correct. Indian is also grouped as Asian.

arrests['Descent.Code'].replace(ethnicities, inplace = True)
print(arrests['Descent.Code'])


# %%
arrests['Descent.Code'].value_counts()
# Very low amount of Pacific Islander, unknown, and Native.
# Therefore, I think that it's safe to replace those specific ethnicities with other.

# %%
arrests['Descent.Code'].replace({
    'Pacific Islander': 'Other',
    'Unknown': 'Other',
    'Native': 'Other'}, inplace = True)

arrests['Descent.Code'].value_counts()

# %%
total_race_arrests =  pd.DataFrame(arrests['Descent.Code'].value_counts()).reset_index()
total_race_arrests = total_race_arrests.rename(columns = {'index': 'race', 'Descent.Code': 'total_arrests'})

# %%
total_race_arrests = total_race_arrests.sort_values(by = ['race'])
total_race_arrests

# %%
sns.barplot(x = 'race', y = 'total_arrests', data = total_race_arrests  )
plt.xlabel('Race')
plt.title('Total Number of Arrests')
plt.ylabel('')

# %%
race_prop = pd.read_csv('/Users/franco/Documents/Projects/Real Arrests/Data/popbyrace.csv')
race_prop = race_prop[['sub_indicator', 'council_district', 'value']]
race_prop = race_prop[race_prop['council_district'] == 'CITY TOTAL']

race_prop = race_prop[['sub_indicator', 'value']]

# %%
race_prop = race_prop.rename(columns = {'sub_indicator': 'race'}).reset_index(drop = True)
race_prop

# %%
# Fix the name of the rows to fix, so we can join.
fix_names = {
    'WHITE': 'White',
    'OTHER': 'Other',
    'BLACK OR AFRICAN AMERICAN': 'Black',
    'ASIAN': 'Asian',
    'HISPANIC OR LATINO': 'Hispanic'

}

race_prop['race'].replace(fix_names, inplace = True)

race_prop

# %%
race_with_arrests = pd.merge(race_prop, total_race_arrests, on = 'race', how = 'outer')
race_with_arrests['prop'] = race_with_arrests['total_arrests'] / race_with_arrests['value']

# %%
race_with_arrests = race_with_arrests.sort_values(by = ['race'])

race_with_arrests

# %%
# Now we can plot the proportions. 
sns.barplot(x = 'race', y = 'prop', data = race_with_arrests)
plt.title('Proportion of Arrests Relative to Population')
plt.xlabel('Race')
plt.ylabel('')

# %%
black = arrests[arrests['Descent.Code'] == 'Black']
asian = arrests[arrests['Descent.Code'] == 'Asian']
white = arrests[arrests['Descent.Code'] == 'White']
hispanic = arrests[arrests['Descent.Code'] == 'Hispanic']
other = arrests[arrests['Descent.Code'] == 'Other']

# %%
black['Charge.Group.Description'].value_counts()

# %%
asian['Charge.Group.Description'].value_counts()

# %%
hispanic['Charge.Group.Description'].value_counts()

# %%
other['Charge.Group.Description'].value_counts()

# %%
white['Charge.Group.Description'].value_counts()

# %%
race_with_arrests

# %%
sns.barplot(x = 'race', y = 'value', data = race_with_arrests)
plt.xlabel('Race')
plt.ylabel('')
plt.title('Population by Race')

# %%
