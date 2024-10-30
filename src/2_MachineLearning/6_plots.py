#Plots
def defineMetricsAndGroups(bias_bins):
    metricNames = ['AUROC', 'Recall', 'F1-score', 'Accuracy']
    tasksNames = ['Mortality', 'Respiratory\nSOFA score', 'Overall SOFA\nscore increase']
    metrics = np.arange(len(metricNames))
    race_groups = ['All','A','B','HL','O','W']

    bias_groups = []
    for min, max in bias_bins:
        if ([min, max] == bias_bins[0]):
            bias_groups.append('(-$\infty$, ' + str(max) + ')')
        elif ([min, max] == bias_bins[3]):
            bias_groups.append('[' + str(min) + ', +$\infty$)')
        else:
            bias_groups.append('[' + str(min) + ', ' + str(max) + ')')

    group_hidden_hypoxemia = [0, 1]

    return tasksNames, metricNames, metrics, race_groups, bias_groups, group_hidden_hypoxemia


## ----------------- plotBarChart -----------------
def plotSignificantValues(ax, x, y, p_values):
    for k in x:
        if p_values[k] == '<.001':
            ax.text(x[k], y+0.1, '***', fontsize=15, weight='bold', ha='center')
        elif p_values[k] == '<.01':
            ax.text(x[k], y+0.1, '**', fontsize=15, weight='bold', ha='center')
        elif float(p_values[k]) < 0.05:
            ax.text(x[k], y+0.1, '*', fontsize=15, weight='bold', ha='center')


def plotBarChart(figs, axs, data, model, task, tasks, reference_feature, biased_feature, bias_bins):
    tasksNames, metricNames, metrics, race_groups, bias_groups, group_hidden_hypoxemia = defineMetricsAndGroups(bias_bins)
    groups = [race_groups, bias_groups, group_hidden_hypoxemia]
    width = 0.4

    for group in [0,1,2]:
        for metric in metrics:
            ax = axs[group][metric, tasks.index(task)]
            x = np.arange(len(groups[group]))
            if group == 0:
                y1 = np.array(data[0][reference_feature])[(metric)*len(race_groups) : (metric)*len(race_groups)+len(race_groups)]
                y2 = np.array(data[0][biased_feature])[(metric)*len(race_groups) : (metric)*len(race_groups)+len(race_groups)]
                p_values = np.array(data[1][biased_feature])[(metric)*len(race_groups) : (metric)*len(race_groups)+len(race_groups) , 0]
            elif group == 1:
                y1 = np.array(data[0][reference_feature])[(metric)*len(bias_groups) + len(metricNames)*len(race_groups) +2 : (metric)*len(bias_groups)+len(bias_groups) + len(metricNames)*len(race_groups) +2]
                y2 = np.array(data[0][biased_feature])[(metric)*len(bias_groups)  + len(metricNames)*len(race_groups) +2 : (metric)*len(bias_groups)+len(bias_groups) + len(metricNames)*len(race_groups) +2]
                p_values = np.array(data[1][biased_feature])[(metric)*len(bias_groups) + len(metricNames)*len(race_groups) +2 : (metric)*len(bias_groups)+len(bias_groups) + len(metricNames)*len(race_groups) +2 , 0]
            else:
                y1 = np.array(data[0][reference_feature])[(metric)*len(group_hidden_hypoxemia) + len(metricNames)*(len(race_groups)+ len(bias_groups)) +2 : (metric)*len(group_hidden_hypoxemia)+len(group_hidden_hypoxemia) + len(metricNames)*(len(race_groups)+len(bias_groups)) +2]
                y2 = np.array(data[0][biased_feature])[(metric)*len(group_hidden_hypoxemia) + len(metricNames)*(len(race_groups)+ len(bias_groups)) +2 : (metric)*len(group_hidden_hypoxemia)+len(group_hidden_hypoxemia) + len(metricNames)*(len(race_groups)+len(bias_groups)) +2]
                p_values = np.array(data[1][biased_feature])[(metric)*len(group_hidden_hypoxemia) + len(metricNames)*(len(race_groups)+ len(bias_groups)) +2 : (metric)*len(group_hidden_hypoxemia)+len(group_hidden_hypoxemia) + len(metricNames)*(len(race_groups)+len(bias_groups)) +2, 0]

            ax.bar(x-width/2, y1, width, color='tab:red', alpha=0.9)
            ax.bar(x+width/2, y2, width, color='tab:blue', alpha= 0.9, edgecolor='w', hatch ='/')

            if group == 1:
                ax.axvline(x=1.5, linestyle='--', color='grey', linewidth = 0.5)

            for x_value in x:
               ax.text(x_value-width/2, y1[x_value], "%.2f" % y1[x_value], fontsize=8, ha='center', va='bottom')
               ax.text(x_value+width/2, y2[x_value], "%.2f" % y2[x_value], fontsize=8, ha='center', va='bottom')

            # Plot asterisks
            y_asterisk = np.array([y1, y2]).max()
            plotSignificantValues(ax, x, y_asterisk, p_values)

            ax.grid(True, axis='y', linestyle='--', color='grey', linewidth = 0.5)

            if tasks.index(task) == 0:
                ax.set_ylabel(metricNames[metric])

            if metric == 0:
                ax.set_title(tasksNames[tasks.index(task)])

        ax.set_xticks(x, labels=groups[group])

        if tasks.index(task) == (len(tasks)-1):
            if group == 1:
                figs[group].legend(['_legend', 'Model with SaO$_{2}$', 'Model with SpO$_{2}$'],
                                loc='lower center',
                                bbox_to_anchor=(0.54, -0.05),
                                fancybox=False, ncol=2)
            else:
                figs[group].legend(['Model with SaO$_{2}$', 'Model with SpO$_{2}$'],
                                loc='lower center',
                                bbox_to_anchor=(0.54, -0.05),
                                fancybox=False, ncol=2)
            ax.set_ylim([0, 1])
            if group == 0:
                figs[group].supxlabel('Race and ethnicity subgroups', x=0.54)
            elif group == 1:
                for i in range(len(tasks)):
                    axs[group][metric, i].text((ax.get_xlim()[1] + ax.get_xlim()[0])*0.47, ax.get_ylim()[0]-0.15, r'$\leftarrow$''SpO$_{2}$\nunderestimates',
                            ha='right', va='top', fontsize=8)
                    axs[group][metric, i].text((ax.get_xlim()[1] + ax.get_xlim()[0])*0.53, ax.get_ylim()[0]-0.15, 'SpO$_{2}$'r'$\rightarrow$''\noverestimates',
                            ha='left', va='top', fontsize=8)
                figs[group].supxlabel('SpO$_{2}$ - SaO$_{2}$ bins', x=0.54)
            else:
                figs[group].supxlabel('Hidden Hypoxemia', x=0.54)
            figs[group].supylabel('Performance metrics (mean)')
            figs[group].savefig(folder_path + 'Plots/' + model + str(group) + biased_feature + '_BarChart_new.png', bbox_inches='tight')
            figs[group].show()

## ----------------- plotDeltaMetric -----------------
def plotDeltaMetric(figs, axs, data, model, task, tasks, biased_feature, bias_bins):
    tasksNames, metricNames, metrics, race_groups, bias_groups, group_hidden_hypoxemia = defineMetricsAndGroups(bias_bins)
    groups = [race_groups, bias_groups, group_hidden_hypoxemia]

    y_max = [0.1, 0.3, 0.15, 0.1]

    for group in [0,1,2]:
        for metric in metrics:
            ax = axs[group][metric, tasks.index(task)]
            x = np.arange(len(groups[group])) +1
            if group == 0:
                y = np.array(data[biased_feature])[:, (metric)*len(race_groups) : (metric)*len(race_groups)+len(race_groups)]
            elif group == 1:
                y = np.array(data[biased_feature])[:, (metric)*len(bias_groups) + len(metricNames)*len(race_groups) +2 : (metric)*len(bias_groups)+len(bias_groups) + len(metricNames)*len(race_groups) +2]
            else:
                y = np.array(data[biased_feature])[:, (metric)*len(group_hidden_hypoxemia) + len(metricNames)*(len(race_groups)+ len(bias_groups)) +2 : (metric)*len(group_hidden_hypoxemia)+len(group_hidden_hypoxemia) + len(metricNames)*(len(race_groups)+len(bias_groups)) +2]

            ax.boxplot(y, medianprops=dict(color='k', linewidth = 1.2), patch_artist=True,
                            boxprops=dict(facecolor='tab:blue', alpha=0.9, color='k'),
                            capprops=dict(color='k', linewidth = 0.5),
                            whiskerprops=dict(color='k', linewidth = 0.5))
            ax.axhline(y = 0, color = 'k', linestyle = 'dashed', linewidth = 0.5)
            ax.grid(True, axis='y', linestyle='--', color='grey', linewidth = 0.5)

            if group == 1:
                ax.axvline(x=1.5, linestyle='--', color='grey', linewidth = 0.5)

            if tasks.index(task) == 0:
                ax.set_ylabel(metricNames[metric])
                ax.set_ylim(ymin=-y_max[metric], ymax=y_max[metric])

            if metric == 0:
                ax.set_title(tasksNames[tasks.index(task)])

            if tasks.index(task) == (len(tasks)-1): #last task
                ax.text(len(groups[group])+0.6, 0+0.05, r'$\uparrow$''SpO$_{2}$ model\nperforms better',
                        ha='left', va='bottom', fontsize=8)
                ax.text(len(groups[group])+0.6, 0-0.05, r'$\downarrow$''SaO$_{2}$ model\nperforms better',
                        ha='left', va='top', fontsize=8)

        ax.set_xticks(x, labels=groups[group])

        if tasks.index(task) == (len(tasks)-1): #last task
            if group == 0:
                figs[group].supxlabel('Race and ethnicity subgroups')
            elif group == 1:
                for i in range(len(tasks)):
                    axs[group][metric, i].text((ax.get_xlim()[1] + ax.get_xlim()[0])*0.47, ax.get_ylim()[0]*1.3, r'$\leftarrow$''SpO$_{2}$\nunderestimates',
                            ha='right', va='top', fontsize=8)
                    axs[group][metric, i].text((ax.get_xlim()[1] + ax.get_xlim()[0])*0.53, ax.get_ylim()[0]*1.3, 'SpO$_{2}$'r'$\rightarrow$''\noverestimates',
                            ha='left', va='top', fontsize=8)
                figs[group].supxlabel('SpO$_{2}$ - SaO$_{2}$ bins', x=0.54)
            else:
                figs[group].supxlabel('Hidden Hypoxemia')

            figs[group].supylabel('Difference between SpO$_{2}$ and SaO$_{2}$ models\' performance')
            figs[group].savefig(folder_path + 'Plots/' + model + str(group) + biased_feature + '_Delta_new.png', bbox_inches='tight')
            figs[group].show()