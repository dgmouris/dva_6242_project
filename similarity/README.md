## Similar POIU Calculation

This directory stores the needed files to calculate the similar POIUs based on the situation on the ice and their shot data for a specific season. A CSV file will need to be used in this situation to run this code that could not be uploaded to Github. This CSV file is not available online as we have it calculate in one of our databases, which we then downloaded and used within this folder. The csv "shot_data_with_poiu.csv" stores aggregated shot data for an entire season for each POIU that has any shots for or against during that season. The season we are currently running this code on is the 2023-2024 NHL season. 

All that is needed to do to run the script is to navigate to the current directory and run
"python similarity_calc.py" and then three CSVs will be generated, one being even-strength POIUs, powerplay POIUs, and penalty kill POIUs and their most similar units and their corresponding similarity scores.

### Files:

**similarity_calc.py** (Python Script): Run this python file to save three CSV files (one each for even-strength, powerplay, and penalty kill POIUs) that return the five most similar POIUs based on shot data output. Also prints the silhouette score and Precision@K score for each situation

**shot_data_with_poiu.csv** (CSV file) NOT INCLUDED: data was too large to store in Github, was calculated through our databases and not available online

**similarity_test.ipynb** (Jupyter Notebook): Notebook that was used fore development and testing of the best methodology for calculating the similarity. Other data sources can be seen that were used but are not used in the final iteration of our model due to lower Precision@K values and less interpretable clustering

**requirements.txt** (text file): contains the required libararies for running the similarity_calc script