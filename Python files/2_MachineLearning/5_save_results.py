#save_results
def save_results(path, model, results, O2_groups, tasks, reference_feature):
    n_metrics = 4*6 + 2 + 4*4 + 4*2
    new_results = []

    for task in tasks:
        for ft in O2_groups:
            for t in ['train', 'test']:
                new_results.append(results[0][t][task][ft])
                if (ft != reference_feature) & (t == 'test'):
                    pvalue_test = []
                    CI_test = []
                    for metric in range(n_metrics):
                        pvalue_test.append((results[1][task][ft][metric])[0])
                        CI_test.append(f"({(results[1][task][ft][metric])[1]} - {(results[1][task][ft][metric])[2]})")
                    new_results.append(pvalue_test)
                    new_results.append(CI_test)

    df_existing = pd.read_excel(path)
    df_combined = pd.concat([df_existing, pd.DataFrame([[model,
                                                            datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                                                            ]]),
                                pd.DataFrame(new_results)],
                            ignore_index=True) # Append new data
    df_combined.to_excel(path, index=False) # Save the combined data to Excel