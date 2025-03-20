import pandas as pd

filesToMerge = ['lines.csv',
                'lines(1).csv',
                'lines(2).csv',
                'lines(3).csv',
                'lines(4).csv',
                'lines(5).csv',
                'lines(6).csv',
                'lines(7).csv',
                'lines(8).csv',
                'lines(9).csv',
                'lines(10).csv',
                'lines(11).csv',
                'lines(12).csv',
                'lines(13).csv',
                'lines(14).csv',
                'lines(16).csv',
                'lines(15).csv']

df = pd.concat(map(pd.read_csv, filesToMerge), ignore_index=True)
colsToAvg  = [
    "xGoalsPercentage", "corsiPercentage", "fenwickPercentage", "xOnGoalFor",
    "xGoalsFor", "shotsOnGoalFor", "blockedShotAttemptsFor", "hitsFor",
    "takeawaysFor", "giveawaysFor"
]

newDF = df.groupby(["name", "situation"])[colsToAvg].mean()
newDF = newDF.reset_index()

filteredDF = newDF[newDF['situation'] == "5on5"]
filteredDF.drop("situation", inplace=True, axis=1)
filteredDF.to_csv('linesMerged.csv', index=False)
