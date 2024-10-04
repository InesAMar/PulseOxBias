##getModelResults
def getModelResults(x, y, k_fold, modelName, tasks, reference_feature, biased_feature, bias_bins):
    groups = np.array(x['unique_subject_id'])
    skf = StratifiedGroupKFold(n_splits=k_fold)

    race_ethnicity_columns = ['race_ethnicity_Asian',
                            'race_ethnicity_Black',
                            'race_ethnicity_HispanicLatino',
                            'race_ethnicity_Other',
                            'race_ethnicity_White']
    O2_column = [reference_feature, biased_feature]
    all_metrics = {}
    delta_test = {}
    metrics_Statistics = {}
    pvalue = {}

    # Evaluation Metrics and Variables to record data
    for t in ['train', 'test']:
        all_metrics[t] = {}
        metrics_Statistics[t] = {}
        for task in tasks:
            all_metrics[t][task] = {}
            delta_test[task] = {}
            metrics_Statistics[t][task] = {}
            pvalue[task] = {}
            for ft in O2_column:
                all_metrics[t][task][ft] = []
                delta_test[task][ft] = []
                metrics_Statistics[t][task][ft] = []
                pvalue[task][ft] = []

    feat_sel_model = 'mySelection'
    selected_features = getSelectedFeatures(feat_sel_model)
    x = x[selected_features]

    for task in tasks:
        print('task: ', task)
        y_task = y[task]

        for fold, (train_index, test_index) in enumerate(skf.split(x, y_task, groups)):
            print('fold: ', fold)
            X_train, Y_train = x.iloc[train_index], y_task.iloc[train_index]
            X_test, Y_test = x.iloc[test_index], y_task.iloc[test_index]

            for feature in O2_column:
                print('Feature: ', feature)
                if feature != reference_feature:
                    x_data_train = X_train.drop(race_ethnicity_columns + [reference_feature, 'unique_hospital_admission_id'], axis=1)
                    x_data_test = X_test.drop(race_ethnicity_columns + [reference_feature, 'unique_hospital_admission_id'], axis=1)
                else:
                    x_data_train = X_train.drop(race_ethnicity_columns + [biased_feature, 'unique_hospital_admission_id'], axis=1)
                    x_data_test = X_test.drop(race_ethnicity_columns + [biased_feature, 'unique_hospital_admission_id'], axis=1)

                # for task in tasks:
                modelName.fit(x_data_train, Y_train, sample_weight = compute_sample_weight(class_weight="balanced", y=Y_train))
                #Train
                all_metrics['train'][task][feature].append(calculateMetrics(modelName, x_data_train, X_train, Y_train, reference_feature, biased_feature, bias_bins))
                #Test
                all_metrics['test'][task][feature].append(calculateMetrics(modelName, x_data_test, X_test, Y_test, reference_feature, biased_feature, bias_bins))

    for task in tasks:
        for ft in O2_column:
            if (ft != reference_feature):
            # Calculate difference between metrics
                delta_test[task][ft] = np.reshape(all_metrics['test'][task][ft], (k_fold,-1)) - np.reshape(all_metrics['test'][task][reference_feature], (k_fold,-1))

    total_metrics = 4*6 + 4*4 + 4*2
    for t in ['train', 'test']:
        for task in tasks:
            for ft in O2_column:
                for metric in range(total_metrics):
                    metrics_Statistics[t][task][ft].append(calculateStatistics(np.reshape(all_metrics[t][task][ft], (k_fold,-1))[:,metric]))
                    if (ft != reference_feature) & (t == 'test'):
                        # Compute p-value
                        pvalue[task][ft].append(getPValue(np.reshape(all_metrics[t][task][reference_feature], (k_fold,-1))[:,metric],
                                                            np.reshape(all_metrics[t][task][ft], (k_fold,-1))[:,metric]))

    # save model's results
    save_results(folder_path + 'ModelResults.xlsx', modelName.__class__.__name__, [metrics_Statistics, pvalue], O2_column, tasks, reference_feature)

    for ft in O2_column:
        if ft != reference_feature:
            fig1, ax1 = plt.subplots(4, len(tasks), figsize=(15,10), sharex=True, sharey=True, layout="constrained")
            fig2, ax2 = plt.subplots(4, len(tasks), figsize=(15,10), sharex=True, sharey=True, layout="constrained")
            fig2_1, ax2_1 = plt.subplots(4, len(tasks), figsize=(10,10), sharex=True, sharey=True, layout="constrained")

            fig3, ax3 = plt.subplots(4, len(tasks), figsize=(15,10), sharex=True, sharey='row', layout="constrained")
            fig4, ax4 = plt.subplots(4, len(tasks), figsize=(15,10), sharex=True, sharey='row', layout="constrained")
            fig4_1, ax4_1 = plt.subplots(4, len(tasks), figsize=(15,10), sharex=True, sharey='row', layout="constrained")

            for task in tasks:
                # Plots
                plotBarChart([fig1, fig2, fig2_1], [ax1, ax2, ax2_1], [metrics_Statistics['test'][task], pvalue[task]], str(modelName.__class__.__name__), task, tasks, reference_feature, ft, bias_bins=bias_bins)
                plotDeltaMetric([fig3, fig4, fig4_1], [ax3, ax4, ax4_1], delta_test[task], str(modelName.__class__.__name__), task, tasks, ft, bias_bins=bias_bins)