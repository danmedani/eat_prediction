import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import namedtuple

from sklearn.metrics import *
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis, LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import TimeSeriesSplit

performance_metrics = namedtuple("accuracy_metrics", "accuracy precision recall")
#should I include f1 score? 

def get_performance_metrics(y_true,y_pred):
    return performance_metrics(accuracy_score(y_true,y_pred), recall_score(y_true,y_pred), precision_score(y_true,y_pred))

#ignore grid searching for hyper parameters for now - incorporate later. 
#Maybe have settings for runtime vs. tunability? 
#Maybe you can high level grid search for all models, and then hone in the most promising model
class classification_ensemble(object):
    
    """Ensemble of classification models."""
    
    def __init__(self, classification_models_params):
        self.best_model = None
        self.trained_models = list()
        #self.performance_metrics_by_model = None -- this is done either on training or test data.. 
        #Doesn't seem is unique to the model and needed to be stored in the class
        #self.top_performance_metrics = None -- same as above
        self.classification_models_params = classification_models_params
    
    def train_singel_model(self, model, params, X, y):
        grid = GridSearchCV(estimator=model, param_grid=params, cv=TimeSeriesSplit(n_splits=2))
        grid.fit(X,y)
        model = grid.best_estimator_
        model.predict(X)
        return model

    def fit(self, X, y, metric_to_optimize="accuracy"):
        """
        fits all models to train data
        """
        if metric_to_optimize not in performance_metrics._fields:
            raise Exception("invalid metric to optimize") 
        print "fitting"
        self.trained_models = [self.train_singel_model(model, params, X, y) for model, params in self.classification_models_params.iteritems() ]
        best_model, best_metrics = self.get_best_model_and_metrics(X,y,metric_to_optimize)
        self.best_model = best_model 
    
    
    def predict_all_models(self, X):
        """returns a dictionary with key=model, value=prediction"""
        print self.classification_models_params.keys()
        return {model: model.predict(X) for model in self.trained_models}
        
    def score_all_models(self, all_y_predictions, y_actual):
        """returns a dictionary with key=model, value=performance_metrics"""
        return {model: get_performance_metrics(all_y_predictions[model],y_actual) for model in self.trained_models}
    
    def get_best_model_and_metrics(self,X,y,metric_to_optimize):
        """
        assumes self.classification_models have been trained. 
        returns (model, score) with the highest metric_to_optimize
        """
        all_y_predictions = self.predict_all_models(X)
        all_model_metrics = self.score_all_models(all_y_predictions, y)
        best_model_and_metrics = max(all_model_metrics.iteritems(), key=lambda model_metrics : model_metrics[1]._asdict()[metric_to_optimize])
        return best_model_and_metrics
    
    def predict(self, X):
        """returns the prediction for X_test using the best model found during training"""
        return self.best_model.predict(X)
        
class probability_classification_ensemble(classification_ensemble):
    
    def __init__(self):
        # classification_models = [
        #     KNeighborsClassifier(2),
        #     LinearDiscriminantAnalysis(),
        #     QuadraticDiscriminantAnalysis(),
        #     LogisticRegression()   
        #     ]

        classification_models_params = {
            KNeighborsClassifier(2):
            {
                'weights':['uniform']
            },
            LinearDiscriminantAnalysis():
            {
                'shrinkage':[None]
            },
            QuadraticDiscriminantAnalysis():
            {
                'priors':[None]
            },
            LogisticRegression():
            {
                'C': [1]
            }
            }

        super(probability_classification_ensemble, self).__init__(classification_models_params=classification_models_params)
        
    #should training be different?? I am pickup the best model off of metrics gathered when judging off of binary predictions
    #I could easily change this by creating an alternate predict_all_models method that used predict_proba
    
    def predict_probability(self, X):
        """returns the prediction for X_test using the best model found during training"""
        return self.best_model.predict_proba(X)
   
    def predict_specified_threshold(self, X, threshold):
        """returns the prediction for X_test using the best model found during training
        Returns true if predicted probability is greater than threshold
        """
        return [prob>=threshold for prob in self.best_model.predict_proba(X)]

class binary_classification_ensemble(classification_ensemble):
    
    def __init__(self):
        classification_models = [
            KNeighborsClassifier(2),
            SVC(),
            RandomForestClassifier(max_depth=5, n_estimators=10),
            AdaBoostClassifier(),
            LinearDiscriminantAnalysis(),
            QuadraticDiscriminantAnalysis(),
            LogisticRegression()]
        print "initializing"
        super(binary_classification_ensemble, self).__init__(classification_models)
