-------------------

General Approach:

We used the "pickle" utility of Python to "save" our progress throughout the analysis. This allowed us to perform time-intensive
analyses, save the results to a pickle file (serialization method), and then reload those pickled results to proceed
with further steps in the analysis process. We used Pandas dataframes and OOP techniques to manipulate, perform calculations, and organize the data and intermediate
results.

-------------------

Some Details of Objects and Methods:

The "Store" object within the sams_work/oop_objects.py file is used for storing the data of the historical data. A list of 45
of these objects is used to hold the historical store data for all of the stores. Throughout the code, this list is often
referred to as "historicalStores" or just "stores." The "FutureStoreSet" object is used to hold all of the data
for the future store data (i.e. the weeks for which we need to make predictions)

For my particular program, the predictions are performed within the sams_work/time_series_analysis.py file. At the
bottom of this file, you can see segments of code, along with comments that explain the purpose of the code and which
lines should be uncommented/commented to perform various analyses.

The "get_weighted__normalized_sales_value" method on the "WeekSalesAverage" object (sams_work/oop_objects.py) may be of interest
for understanding exactly how the historical sales values are averaged.

Also, the "make_predictions_sequential_methods," and "make_predictions_with_weighted_average_of_methods" may be of interest
for understanding the two primary methods for combining the predicted sales of the various sales prediction methods.

-------------------

Running the Code:

As I mentioned in the report, I don't think you'll be able to run the code, since I ran the code in an Anaconda environment
on my machine that handled all of the package/module dependencies. I wasn't sure how to export the code with all of
its dependencies in a manner such that you would be able to run the program. If you are able to somehow run the program,
you should run the "sams_work/time_series_analysis.py" file as your main, and  make modifications to the code at the bottom
of the file, depending on what you want to run.

-------------------

Running the Code:

Output:

With the current setup, the output will be a "kaggle_predictions.txt" file that is in the format specified by Kaggle
for subbmitting the predictions to the online evaluator. A "missing_holiday_preditions.txt" and a "missing_non_holiday_preditions.txt"
file is also provided to ensure that all predictions were made.