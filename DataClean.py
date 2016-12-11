import pandas as pd
from pandas import DataFrame, Series
import numpy as np

### Remove cases with missing name or missing ethnicity information
def DecisionTreeClean():
    data = pd.read_csv("AdultCensus.csv")
    frame = DataFrame(data)
    frame.columns = ["age",
                     "workclass",
                     "education",
                     "educationnum",
                     "maritalstatus",
                     "occupation",
                     "relationship",
                     "race",
                     "sex",
                     "capitalgain",
                     "capitalloss",
                     "hoursperweek",
                     "nativecountry",
                     "income"]

    frame = frame[frame.workclass != "?"]
    frame = frame[frame.education != "?"]
    frame = frame[frame.maritalstatus != "?"]
    frame = frame[frame.occupation != "?"]
    frame = frame[frame.relationship != "?"]
    frame = frame[frame.race != "?"]
    frame = frame[frame.sex != "?"]

    frame = frame[frame.nativecountry != "?"]
    frame = frame[frame.income != "?"]
    labels = ["{0} - {1}".format(i, i + 9) for i in range(0, 100, 10)]

    frame['capitalgain'] = pd.cut(frame.age, range(0, 105, 10), right=False, labels=labels)

    frame['capitalloss'] = pd.cut(frame.hoursperweek, range(0, 105, 10), right=False, labels=labels)

    frame.to_csv("AdultCensus_cleaned.csv")
DecisionTreeClean()
