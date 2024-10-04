import matplotlib.pyplot as plt
import pandas as pd

import numpy as np
from datetime import datetime

from google.colab import drive
drive.mount('/content/drive')

import warnings
warnings.filterwarnings('ignore')

import xgboost as xgb
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedGroupKFold

from sklearn.metrics import roc_auc_score, f1_score, recall_score, accuracy_score
import scipy.stats as st

from sklearn.utils.class_weight import compute_sample_weight

##Import csv
folder_path = '/content/drive/My Drive/'
filename = folder_path + 'O2_data.csv'
data = pd.read_csv(filename)