# -*- coding: utf-8 -*-
"""Untitled.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LlyV4N6q_wMWSuV7MhokCbWMJjV6gyJX

# <center>Preventive Analysis of Car Accident Severity </center>

# Table of contents
* [Introduction: Business Problem](#introduction)
* [Data](#data)
* [Methodology](#methodology)
* [Analysis](#analysis)
* [Results and Discussion](#result)
* [Conclusion](#conclusion)

# Problem Statement <a name="introduction"></a>

In this project,we will try to develope a system for **purpose of preventing Accidents** and Other Traffic related disasters.Specifically,this report will target people who commute or travel more often in order to make commute safer for everyone.

Normally when we commute or travel for work or other activites,we are usually not aware of situation that one could encounter.One could face a disaster on his way or could face a severe accident.

  This would allow user to **plan journey in order to make travel more feasible and safe**.This would be dependent upon several different variables.e.g, weather,humidity and so on.
  
  We will use our dataset to study the relationship between various variable in accordance with accident severity.We will use various statistical tests such as **pearsonr,z test,t test** etc in order to study correlation between accident severity and Accident severity.

# Data <a name="data"></a>

Based upon our problem statement the factors having an impact on our decision are,
 - Junction Type i.e Intersection,Highway etc
 - Weather will play a huge role
 - ROAD CONDITION indicates wether road is slippery or not.Bad Road Condition leads to greater risk of accident
 - LIGHT CONDITION implies the visibility.If visibility is hampered we wont be able to respond well to events. 
 
Above mentioned are some obvious factors invovled in accidents.In order to determine the relationship between other variables with respect to data we will perform multiple tests to calculate correlation. 

Following data sources will be needed to generate the required information.
- **Seatle SPD** Dataset that is open sourced.This Dataset is from 2004 till peresent.
- [Link to the Dataset](https://s3.us.cloud-object-storage.appdomain.cloud/cf-courses-data/CognitiveClass/DP0701EN/version-2/Data-Collisions.csv)
"""

import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt 
import matplotlib.patches as mpatches

!cd ..

!ls

data=pd.read_csv('/content/drive/My Drive/Colab Notebooks/Data-Collisions.csv')

from google.colab import drive
drive.mount('/content/drive')

"""# Methodology <a name='methodology'></a>

In this project,we will direct our effort to check the factors that impact accident severity and try to form a hypothesis model in order to prevent such events from occurring in future.

In the first step,we will gather **Data provided by SPD Seatle**.we will analyze this Data via meta data provided by SPD and check for redundant things like registration number,accident ID Incident ID etc.Such things dont have any impact on outcome of our analysis.

In the second step,we will try to figure out what features impact severity of accident.We will use Z-test and one way ANOVA to calculate correlation and statistical significance of our outcome.Then we will plot data using bar plot to check where most accidents have occurred and what was severity of accident.

In the third step,we will try and explore various statistical methods to form a statistical relationship between independent variables(features) and dependent variables(target variable).We will try various classification techniques such as KNN,Decision Tree Classifier,SVM.
"""

data.head()

data.info()

"""As shown from above description,some features contain way too many missing values.If we try to impute them we may end up messing up entire data minning process.So after dropping columns with too much missing values we can now start using Feature Engineering to find out which features are important.

# Analysis <a name='analysis'></a>

# Feature Engineering

- ST_COLCODEText : code provided by the state that describes the collision.
- ST_COLDESCText : description that corresponds to the state’s coding designation. 
- SDOTCOLNUM : A number given to the collision by SDOT.
- SDOT_COLDESC : A description of the collision corresponding to the collision code
- SDOT_COLCODE : A code given to the collision by SDOT.
- EXCEPTRSNCODE 
- EXCEPTRSNDESC 
- LOCATION : Description of the general location of the collision 
- SEVERITYDESC : detailed description of the severity of the collision.
- COLLISIONTYPE : Collision type 
- INJURIES : The number of total injuries in the collision. Thisis entered by the state. 
- SERIOUSINJURIES : The number of serious injuries in the collision. This is entered by the state.
- FATALITIES : The number of fatalities in the collision. This is entered by the state.

Features mentioned above are not of that much value to us.Since most of them are registration ID issued by states and remaining indicate aftermeth of accident which goes against our planned agenda which is to prevent any such incident from occurring.So they are not of that much usage in our case scenrio.
"""

modified_data=data.drop(['ST_COLCODE','ST_COLDESC','SDOTCOLNUM','SDOT_COLDESC','SDOT_COLCODE','EXCEPTRSNCODE',
          'EXCEPTRSNDESC','LOCATION','COLLISIONTYPE'
          ,'INCKEY','COLDETKEY','OBJECTID','REPORTNO','INTKEY','HITPARKEDCAR','INCDTTM','SEVERITYDESC',
                        'SEGLANEKEY','CROSSWALKKEY','SEVERITYCODE.1'],axis=1)
modified_data.head()

"""# Data preprocessing"""

modified_data.ROADCOND.fillna(method='bfill',inplace=True)

modified_data.UNDERINFL=modified_data.UNDERINFL.map({'Y':1,'N':0})

modified_data.UNDERINFL.value_counts()

modified_data.STATUS=modified_data.STATUS.map({'Matched':1,'Unmatched':0})

modified_data.STATUS.dtype

modified_data.JUNCTIONTYPE.value_counts()

modified_data.ROADCOND.value_counts()

pd.get_dummies(modified_data.LIGHTCOND)

modified_data.shape

modified_data=pd.concat([modified_data,pd.get_dummies(modified_data['WEATHER'])],axis=1)
modified_data.drop(['WEATHER','Unknown'],inplace=True,axis=1)
modified_data.Clear.dtype

modified_data=pd.concat([modified_data,pd.get_dummies(modified_data['ADDRTYPE'])],axis=1)
modified_data.drop('ADDRTYPE',axis=1,inplace=True)
modified_data.Alley.dtype

modified_data=pd.concat([modified_data,pd.get_dummies(modified_data['JUNCTIONTYPE'])],axis=1)
modified_data.drop('JUNCTIONTYPE',axis=1,inplace=True)

modified_data=pd.concat([modified_data,pd.get_dummies(modified_data['ROADCOND'])],axis=1)
modified_data.drop('ROADCOND',axis=1,inplace=True)

modified_data=pd.concat([modified_data,pd.get_dummies(modified_data['LIGHTCOND'])],axis=1)
modified_data.drop(['LIGHTCOND','Unknown'],axis=1,inplace=True)
modified_data.Daylight.dtype

modified_data.head()

modified_data.columns

modified_data.drop('Other',inplace=True,axis=1)
modified_data.columns

modified_data.isnull().sum()

"""## Exploratory Data Analysis

# Checking for imbalance
"""

modified_data.SEVERITYCODE.value_counts()

"""### Correlation"""

modified_data.corr()

"""### ANOVA

#### Correlation of ADDRTYPE
"""

grouped_test2=data[['ADDRTYPE', 'SEVERITYCODE']].groupby(['ADDRTYPE'])
grouped_test2.head(2)

f_val,p_val=stats.f_oneway(grouped_test2.get_group('Intersection')['SEVERITYCODE'],
                           grouped_test2.get_group('Block')['SEVERITYCODE'],
                          grouped_test2.get_group('Alley')['SEVERITYCODE'])
f_val,p_val

f_val,p_val=stats.f_oneway(grouped_test2.get_group('Intersection')['SEVERITYCODE'],
                           grouped_test2.get_group('Block')['SEVERITYCODE'])
f_val,p_val

f_val,p_val=stats.f_oneway(grouped_test2.get_group('Intersection')['SEVERITYCODE'],
                           grouped_test2.get_group('Alley')['SEVERITYCODE'])
f_val,p_val

f_val,p_val=stats.f_oneway(grouped_test2.get_group('Alley')['SEVERITYCODE'],
                           grouped_test2.get_group('Block')['SEVERITYCODE'])
f_val,p_val

"""##  Relation between ADDRTYPE and Severity of Accident"""

combined=data.groupby(['ADDRTYPE','SEVERITYCODE']).size().to_frame()
combined.columns=['NUMBER_OF_INCIDENTS']
combined.reset_index(inplace=True)

plt.figure(figsize=(8,5))

combined.plot(kind='bar',
             x='ADDRTYPE',
             y='NUMBER_OF_INCIDENTS',
             figsize=(12,8),
             color=['Yellow','Red'],
             alpha=0.7)

red_patch = mpatches.Patch(color='Yellow', label='Property Damage')
yellow_patch = mpatches.Patch(color='Red', label='Injured')

plt.legend(handles=[red_patch,yellow_patch])

"""## Relation b/w Weather and Severity of Accident"""

group2=data.groupby(['WEATHER','SEVERITYCODE']).size().to_frame()
group2.columns=['Number of Incidents']
group2.reset_index(inplace=True)
group2

group2.plot(kind='bar',
           x='WEATHER',
           y='Number of Incidents',
           figsize=(10,6),
           color=['Yellow','Red'],
           alpha=0.6)
red_patch = mpatches.Patch(color='Red', label='Property Damage')
yellow_patch = mpatches.Patch(color='Yellow', label='Injured')

plt.legend(handles=[red_patch,yellow_patch])

"""## Relation between weather and Road Condition"""

group3=data.groupby(['ROADCOND','SEVERITYCODE']).size().to_frame()
group3.columns=['Number of Incidents']
group3.reset_index(inplace=True)
group3

group3.plot(kind='bar',
           x='ROADCOND',
           y='Number of Incidents',
           figsize=(12,6),
           color=['Yellow','Red'],
           alpha=0.7)
red_patch=mpatches.Patch(color='Yellow',label='Property Damage')
yellow_patch=mpatches.Patch(color='Red',label='Injured')
plt.legend(handles=[red_patch,yellow_patch])

group3=data.groupby(['LIGHTCOND','SEVERITYCODE']).size().to_frame()
group3.columns=['Number of Incidents']
group3.reset_index(inplace=True)
group3

group3.plot(kind='bar',
           x='LIGHTCOND',
           y='Number of Incidents',
           figsize=(12,6),
           color=['Red','Yellow'],
           alpha=0.7)

"""## One hot encoding
Now we will transform our categorical variables to numerical values in order to be able to apply various statistics technique and eventually perform machine learning technique to get insight of data.
"""

modified_data.SPEEDING=modified_data.SPEEDING.map({'Y':1,'N':0})
modified_data.head()

modified_data.UNDERINFL=modified_data.UNDERINFL.map({'Y':1,'N':0})
modified_data.UNDERINFL.replace(np.nan,0,inplace=True)
modified_data.head()

modified_data.shape

modified_data.UNDERINFL=modified_data.UNDERINFL.map({'Y':1,'N':0})
modified_data.UNDERINFL.replace(np.nan,0,inplace=True)
modified_data.head()

"""## Dealing with missing values"""

modified_data.isnull().sum()

"""Statistical guidance articles have stated that bias is likely in analyses with more than 10% missingness and that if more than 40% data are missing in important variables then results should only be considered as hypothesis generating.As a rule of thumb, when the data goes missing on 60–70 percent of the variable, dropping the variable should be considered."""

data.PEDROWNOTGRNT.value_counts()

modified_data.drop(['INATTENTIONIND','SPEEDING','PEDROWNOTGRNT'],axis=1,inplace=True)

modified_data.drop(['X','Y'],axis=1,inplace=True)
modified_data.isnull().sum()

modified_data.head()

modified_data.INCDATE=modified_data.INCDATE.map(lambda x:x[:10])
modified_data.INCDATE=pd.to_datetime(modified_data.INCDATE,format='%Y/%m/%d')
modified_data.INCDATE.dtype

modified_data['DATE']=modified_data.INCDATE.dt.day
modified_data['MONTH']=modified_data.INCDATE.dt.month
modified_data.drop('INCDATE',axis=1,inplace=True)
modified_data.head()

modified_data.shape

import xgboost as xgb
from sklearn import model_selection,ensemble
from sklearn import svm,tree,neighbors
from sklearn import metrics,preprocessing

target='SEVERITYCODE'

"""## Balancing and Splitting data"""

min_class_len=len(modified_data[modified_data[target]==2])
maj_class_indices=modified_data[modified_data[target]==1].index
random_majority_indices=np.random.choice(maj_class_indices,
                                        min_class_len+1000,
                                        replace=False)
min_class_indices=modified_data[modified_data[target]==2].index
under_sampled=np.concatenate([min_class_indices,random_majority_indices])
undersampled_data=modified_data.loc[under_sampled]
undersampled_data.head()

X=undersampled_data.loc[:,undersampled_data.columns!=target]
y=undersampled_data.loc[:,undersampled_data.columns==target]

X_train,X_test,y_train,y_test=model_selection.train_test_split(X,y,test_size=0.3,random_state=1)

X_train.DATE=(X_train.DATE)/X_train.DATE.std()
X_test.DATE=(X_test.DATE)/X_test.DATE.std()
X_train.MONTH=(X_train.DATE)/X_train.MONTH.std()
X_test.MONTH=(X_test.DATE)/X_test.MONTH.std()
#X_train.MONTH=preprocessing.StandardScaler().fit_transform(X_train.MONTH)
#X_test.DATE=preprocessing.StandardScaler().fit_transform(X_test.DATE)
#X_test.MONTH=preprocessing.StandardScaler().fit_transform(X_test.MONTH)
X_test.DATE.dtype

"""# Machine Learning"""

dt=tree.DecisionTreeClassifier(criterion='gini',min_samples_leaf=2,
                               min_samples_split=4,max_depth=10
                              )
dt.fit(X_train[:40000],y_train[:40000])

yhat=dt.predict(X_train[:40000])
metrics.accuracy_score(y_train[:40000],yhat)

yhat=dt.predict(X_test)
metrics.accuracy_score(y_test,yhat)

print(metrics.classification_report(y_test,yhat))

SVM=svm.SVC()
SVM.fit(X_train[:40000],y_train[:40000])

yhat=SVM.predict(X_train[:40000])
metrics.accuracy_score(y_train[:40000],yhat)

yhat=SVM.predict(X_test)
metrics.accuracy_score(y_test,yhat)

print(metrics.classification_report(y_test,yhat))

model=ensemble.RandomForestClassifier(min_samples_leaf=1,
                               min_samples_split=2,max_depth=15)
model.fit(X_train,y_train)

yhat=model.predict(X_train[:10000])
metrics.accuracy_score(y_train[:10000],yhat)

yhat=model.predict(X_test)
metrics.accuracy_score(y_test,yhat)

print(metrics.classification_report(y_test,yhat))

model=ensemble.AdaBoostClassifier()
model.fit(X_train,y_train)
yhat=model.predict(X_test)
metrics.accuracy_score(y_test,yhat)

print(metrics.classification_report(y_test,yhat))

model=xgb.XGBClassifier()
model.fit(X_train,y_train)
yhat=model.predict(X_test)
metrics.accuracy_score(y_test,yhat)

print(metrics.classification_report(y_test,yhat))

"""# Result and discussion <a name = "result"></a>

Although,all the models gave similar results and were interpretable but there were certain differences.So In the end,we decided to use XGBoost model as it provided best accuracy,f1 score,precision and recall.All in all it was the all in one package we had.
After performing complex statistical techniques,we had to analyze which factor impact road accident more then other.This is major objective of this course as mentioned in the introduction.
Outcome was that greater number of persons,vehicles,pedestrians involved,greater the severity of accident and vice versa.
This was expected from beginning but thing that was surprising is that on some day accidents occur more then the other.On these dates there is usually either start of work week or end of work week.Mainly either Monday or Friday.
Precautions can help us avoid these situations from occurring in the first place.More caution needs to be advised on normal days as travelers become careless when situation is normal and this leads to a disaster.
Further more we need to lower the number of vehicles of street to prevent other traffic related issues.
On alley,there needs to be more strict speed control laws and drivers should be penalized more,
"""

xgb.plot_importance(model)
plt.rcParams['figure.figsize'] = [8, 8]
plt.show()

"""# Conclusion <a name = 'conclusion'></a>

Although we got 67% accuracy using classification models using XG Boost,however it can be further improvised.Many important features had to be dropped to due the fact that they has 75-90% missing data.Had we tried to fill them up using something we might have biased our dataset and eventually we would have had biased our dataset.If Dataset had all the variables in place then it would have been much more accurate.
"""