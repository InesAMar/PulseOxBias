import matplotlib.pyplot as plt
import pandas as pd
from google.colab import files
import missingno as msno

from google.colab import drive
drive.mount('/content/drive')

import warnings
warnings.filterwarnings('ignore')

#Import csv
folder_path = '/content/drive/My Drive/'
filename = folder_path + 'final_df_multiple_ABG.csv'
data = pd.read_csv(filename)