# IIC_CRP
Code for 3rd year of the Conservation International and W&amp;M Institute for Integrative Conservation collaborative Conservation Research Project concerning turbidity monitoring around Lake Alaotra, Madagascar.

Includes code for the turbidity sensors, as well as code for data analysis and graphing.

## Analysis

### is_significant.py

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
    
kruskal_wallace() can be called on its own from another file, but the program can also be run from
the command line. To do this, use the format: 
    
    py is_difference_significant.py [1st/file.txt] [2nd/file.txt] ... (--normalize) var1 val1 var2 val2 ...
    
For example:
    
	py is_difference_significant.py "../../data/Tinkling Rill (6_17 - 6_23)/comp.txt" "../../data/Chickahominy (6_6 - 6_7)/comp.txt"  "10min_rainfall 0"
    
This will look at the data from Tinkling Rill and Chickahominy, comparing data without rainfall
(10min_rainfall <= 0) and with rainfall. You could also do "10min_rainfall <= 0" or 
"10min_rainfall = 0", which will do exactly the same thing. Adding "normalize" or "--normalize"
after the files but before the conditions will normalize the turbidity data. Adding no conditions
will have the program perform the test on all the data from all the samples together.    
    
For specifying weather conditions, the following formats all do the same thing: "variable value",
"variable=value", "variable<=value", "variable<value", "variable-value". The variable names aren't
case-sensitive, and spaces, periods, and underscores are interchangeable.
    
Input data files should be in a tab-separated values format.