##metricsByRace
def metricsByRace(x_test, y_test, prob, prob_bin):
    race_ethnicity_columns = ['race_ethnicity_Asian',
                            'race_ethnicity_Black',
                            'race_ethnicity_HispanicLatino',
                            'race_ethnicity_Other',
                            'race_ethnicity_White']
    #AUC ROC
    roc_aucByRace = []
    #Recall
    recall_byRace = []
    #F1
    f1Scores_byRace = []
    #Accuracy
    accuracy_byRace = []

    for race_ethn in race_ethnicity_columns:
        try:
            rocAuc = roc_auc_score(y_test[x_test[race_ethn] == 1], prob[x_test[race_ethn] == 1])
        except:
            rocAuc = np.nan
        roc_aucByRace.append(rocAuc)
        recall_byRace.append(recall_score(y_test[x_test[race_ethn] == 1], prob_bin[x_test[race_ethn] == 1], average = 'binary'))
        f1Scores_byRace.append(f1_score(y_test[x_test[race_ethn] == 1], prob_bin[x_test[race_ethn] == 1], average = 'binary'))
        accuracy_byRace.append(accuracy_score(y_test[x_test[race_ethn] == 1], prob_bin[x_test[race_ethn] == 1]))

    return [round(k, 3) for k in roc_aucByRace], [round(y, 3) for y in recall_byRace], [round(x, 3) for x in f1Scores_byRace], [round(z, 3) for z in accuracy_byRace]

##metricsByBiasBin
def metricsByBiasBin(x_test, y_test, prob, prob_bin, bias_bins):
    #AUC ROC
    roc_auc = []
    #Recall
    recall = []
    #F1
    f1Score = []
    #Accuracy
    accuracy = []

    for min, max in bias_bins:
        try:
            rocAuc = roc_auc_score(y_test[(x_test['SpO2-SaO2'] >= min) & (x_test['SpO2-SaO2'] < max)], prob[(x_test['SpO2-SaO2'] >= min) & (x_test['SpO2-SaO2'] < max)])
        except:
            rocAuc = np.nan
        roc_auc.append(rocAuc)
        recall.append(recall_score(y_test[(x_test['SpO2-SaO2'] >= min) & (x_test['SpO2-SaO2'] < max)], prob_bin[(x_test['SpO2-SaO2'] >= min) & (x_test['SpO2-SaO2'] < max)], average = 'binary'))
        f1Score.append(f1_score(y_test[(x_test['SpO2-SaO2'] >= min) & (x_test['SpO2-SaO2'] < max)], prob_bin[(x_test['SpO2-SaO2'] >= min) & (x_test['SpO2-SaO2'] < max)], average = 'binary'))
        accuracy.append(accuracy_score(y_test[(x_test['SpO2-SaO2'] >= min) & (x_test['SpO2-SaO2'] < max)], prob_bin[(x_test['SpO2-SaO2'] >= min) & (x_test['SpO2-SaO2'] < max)]))

    return [round(k, 3) for k in roc_auc], [round(y, 3) for y in recall], [round(x, 3) for x in f1Score], [round(z, 3) for z in accuracy]

##metricsByHH
def metricsByHH(x_test, y_test, prob, prob_bin):
    #AUC ROC
    roc_auc = []
    #Recall
    recall = []
    #F1
    f1Score = []
    #Accuracy
    accuracy = []

    for i in [0,1]:
        if i == 0:
            index = ((x_test['SpO2'] >= 88) & (x_test['SaO2'] >= 88)) #consistent values
        else:
            index = ((x_test['SpO2'] >= 88) & (x_test['SaO2'] < 88)) #hidden hypoxemia

        try:
            roc_auc.append(roc_auc_score(y_test[index], prob[index]))
        except:
            roc_auc.append(np.nan)
        recall.append(recall_score(y_test[index], prob_bin[index], average = 'binary'))
        f1Score.append(f1_score(y_test[index], prob_bin[index], average = 'binary'))
        accuracy.append(accuracy_score(y_test[index], prob_bin[index]))

    return [round(k, 3) for k in roc_auc], [round(y, 3) for y in recall], [round(x, 3) for x in f1Score], [round(z, 3) for z in accuracy]


###getMetrics
def getMetrics(y, prob, prob_bin):
    try:
        roc_auc = roc_auc_score(y, prob)
    except:
        roc_auc = np.nan
    recall = recall_score(y, prob_bin, average = 'binary')
    f1Score = f1_score(y, prob_bin, average = 'binary')
    accuracy = accuracy_score(y, prob_bin)
    return [round(x, 3) for x in [roc_auc, recall, f1Score, accuracy]]


##calculateMetrics
def calculateMetrics(model, x_data, X, Y, reference_feature, biased_feature, min_max):
    X_ = X[:]
    prob_bin = model.predict(x_data)
    prob = model.predict_proba(x_data)[:, 1]

    metrics = getMetrics(Y, prob, prob_bin)

    metrics_ByRace = metricsByRace(X_, Y, prob, prob_bin)

    bias_column = 'SpO2-SaO2'
    bias_bins = {}
    X_[bias_column] = X_[biased_feature] - X_[reference_feature]
    for min, max in min_max:
        bias_bins[str(min) + '_' + str(max)] = (X_[bias_column] >= min) & (X_[bias_column] < max)

    metrics_ByBiasBin = metricsByBiasBin(X_, Y, prob, prob_bin, min_max)

    metrics_ByHH = metricsByHH(X_, Y, prob, prob_bin)

    return np.hstack(([metrics[0]] + metrics_ByRace[0] + \
            [metrics[1]] + metrics_ByRace[1] + \
            [metrics[2]] + metrics_ByRace[2] + \
            [metrics[3]] + metrics_ByRace[3], \
            np.reshape(metrics_ByBiasBin, (1,-1))[0], \
            np.reshape(metrics_ByHH, (1,-1))[0]))


###calculateStatistics
def calculateStatistics(data):
    results = round(np.nanmean(data), 3)
    return results