#Upload csv file
data_filled.to_csv(folder_path+'O2_data.csv', index=False)
files.download(folder_path+'O2_data.csv')