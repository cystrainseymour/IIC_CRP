# IIC_CRP
Code for 3rd year of the Conservation International and W&amp;M Institute for Integrative Conservation collaborative Conservation Research Project concerning turbidity monitoring around Lake Alaotra, Madagascar.

Includes code for the turbidity sensors, as well as code for data analysis and graphing.

## Analysis

### divided_kruskall.py

Given data from two or more different samples (e.g. one stream from a restored area and one from a non-restored area, or two samples of the same stream before and after restoration),
and optionally different weather conditions, this program will split each sample into groups 
based on the conditions (e.g. high-rain and low-rain groups) and then perform the Kruskal-Wallace
H-test on each group between the samples (e.g. comparing low-rain from Sample A with low-rain from
Sample B), and then for each group, it returns the probability that both come from the same 
distribution. A low p-value/probability means it's less likely the difference is due to chance,
and a higher probability there is something actually different between the sites the samples
came from.
    
A p-value is computed between all the samples on each combination of weather conditions (e.g. one
p-value for low-rain but high-temperature conditions in Samples A, B, and C). This hopefully 
eliminates the effect of confounding weather variables -- if it happens to rain a lot during
the sampling period at Site A, but not at Site B, then given the appropriate conditions, 
the program will compare rainy conditions at Site A only with rainy conditions at Site B, and
non-rainy conditions at Site A only with non-rainy conditions at Site B, returning different
probabilities for each.
    
The user is free to choose the weather conditions they want to use to divide the samples. The goal is
to eliminate any counfounding variables, so that if there is a difference between the samples, we
can be sure it's due to the restoration. But if one sample has no datapoints matching one set of 
conditions, the p-value for that set/group will be NaN (not a number). Beyond that, overfitting is a 
possibility. Because of this, using too many restrictions/conditions could be counterproductive.
    
divided_kruskall() can be called on its own from another file, but the program can also be run from
the command line. To do this, use the format: 
    
    py divided_kruskall.py [1st/file.txt] [2nd/file.txt] ... (--normalize) var1 val1 var2 val2 ...
    
For example:
    
	py divided_kruskall.py "../../data/Tinkling Rill (6_17 - 6_23)/comp.txt" "../../data/Chickahominy (6_6 - 6_7)/comp.txt"  "10min_rainfall 0"
    
This will look at the data from Tinkling Rill and Chickahominy, comparing data without rainfall
(10min_rainfall <= 0) and with rainfall. You could also do "10min_rainfall <= 0" or 
"10min_rainfall = 0", which will do exactly the same thing. Adding "normalize" or "--normalize"
after the files but before the conditions will normalize the turbidity data. Adding no conditions
will have the program perform the test on all the data from all the samples together.    
    
For specifying weather conditions, the following formats all do the same thing: "variable value",
"variable=value", "variable<=value", "variable<value", "variable-value". The variable names aren't
case-sensitive, and spaces, periods, and underscores are interchangeable.
    
Input data files should be in a tab-separated values (TSV) format.

### linear_regression.py

Given a single data file (formatted as TSV), estimates the intercept and coefficients for a predictive 
model, which predicts the turbidity as the dependent variable based on the other variables in the data
(not including time, which is ignored). It uses a simple linear regression with a least-squared 
estimator, as well as Lasso and Ridge regression. The default alpha value for these is 0.001, but it can
be changed by the user. All data series are normalized before all of the regressions. For each 
regression, the program returns the intercept, the coefficients for each variable, and the r-squared value.
It also performs an F-statistic test to evaluate if the regression models are significantly better than
the intercept model, and outputs the p-value for each.

This can be useful for estimating the importance of different factors in affecting the turbidity. The 
r-squared value is also useful for understanding how much variation can be explained from the factors 
provided. The p-value from the F-test is useful for understanding how significant and definitive the results
are, as well as how useful the independent variables are in explaining the behavior of the dependent 
variable. A low p-value means that a model incorporating these factors performs much better than one that 
doesn't take any of them into account.

The program returns summary statistics for each dependent and independent variable,and then the results 
from each regression. If the keyword "--summary" is used, it will only print the summary statistics, without
running any regression.

To run the program from the command line, use the following format:

	py linear_regression.py [file/path.txt] (-date datetime_col1 (datetime_col2)) (lasso_alpha (ridge_alpha)) (--summary)
	
The default assumption is that the time and date information is in the very first column (index 0). If 
that's not true, or the time and date are split across multiple columns, you can use "-date" (or just "-d")
after the path to the input file to specify. If only one number is included (e.g. "-d 2"), then that column
will be used as the date and excluded from analysis. If there are two, the first will be treated
as the first date/time column, and every column until the second number will be excluded (So "-d 2 4" 
would exclude columns 2 and 3; "-d 2 5" would exclude 2, 3, and 4). The columns are numbered starting at 0,
so the very leftmost column is 0, the next to the right is 1, the third from the left is 2, etc.

If only one value is provided for alpha, it will be used for both the Lasso and Ridge regressions. If two 
are provided, the first will be used for Lasso and the second for Ridge. If none are provided, 0.001 is 
used for both.

Using --summary anywhere after the file path will have the regression not be run, and summary statistics 
will be printed instead.

### Synthetic Control

Synthetic control is an econometric method for estimating or predicting the effects of a policy or 
treatment, and it can be applied to conservation. By gathering data on dependent and independent variables
from multiple sites, some receiving a treatment (e.g. restoration) and some not (the control), both before
and after the treatment is applied to the treatment site, we can create a synthetic control -- a 
hypothetical site with conditions similar to the treatment site, both in dependent and independent 
variables. Based on the pre-treatment data from the control sites, and the post-treatment independent 
variables from the treatment site, we can estimate the predicted values of the dependent variable
(turbidity) in the post-treatment period. We then compare this to the actual post-treatment values from the 
treatment site. Any difference we see can't be explained by the independent variables -- so, ideally, it
must be due to the treatment. More difference (in the right direction) means the treatment is more 
effective.

This is a useful method, but it does require gathering data over a period of time, since for each site, 
or at least the treatment site, you need data from before and after the treatment is applied.