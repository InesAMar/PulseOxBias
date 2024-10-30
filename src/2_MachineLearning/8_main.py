#Main
##Data split
def xy_split(data, tasks):
    x_data = data.drop(tasks, axis= 1)
    y_data = data[tasks]
    return x_data, y_data

tasks = ['in_hospital_mortality', 'sofa_future_respiratory_24hr', 'sofa_overall_increased']

reference_feature = 'SaO2'
biased_feature = 'SpO2'

all_x_data, all_y_task = xy_split(data.drop(['unique_icustay_id', 'sofa_future_overall_24hr','SaO2_timestamp', 'SpO2_timestamp'], axis= 1), tasks)

##Train + Test
kfold = 10
min_max = [[float('-inf'), -3],
               [-3, 0],
               [0, 3],
               [3, float('inf')]]

for model in models:
    display(str(model.__class__.__name__))
    metrics_ = getModelResults(all_x_data, all_y_task, kfold,
                        model, tasks, reference_feature, biased_feature, min_max)