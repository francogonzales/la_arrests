# La Arrest Analysis

Using the LA City Data found [here](https://data.lacity.org/browse), I tried to see if minority groups were unfairly targeted by police using various R and Python Libraries.

Links:
* [Report](https://github.com/francogonzales/la_arrests/blob/master/LA%20Arrests.pdf)
* [Code](https://github.com/francogonzales/la_arrests/blob/master/findcouncilID.R) for matching arrests with council districts, done in R.
* [Code](https://github.com/francogonzales/la_arrests/blob/master/analysis.py) for the actual analysis. Making plots, fixing up and cleaning the data.


Important notes:
* The arrest data is not available as the file is HUGE. Instead it could be found in the link above from the LA City website.
* I use Visual Studio Code instead of the traditional Jupyter Notebook
  * This is why .py are the formats of the code
  * The reason for the ## in the code is due to how the Jupyter package works in VScode (works as separate chunks)
  * Plots were saved using the built-in feature, hence why they weren't saved via a line of code.

