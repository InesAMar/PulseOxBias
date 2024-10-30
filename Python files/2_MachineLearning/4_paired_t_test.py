# Paired-sample t-test
def getPValue(group1, group2):
    _, p_value = st.ttest_rel(group1, group2, alternative = 'two-sided', nan_policy='omit')
    CI = st.ttest_rel(group1, group2, alternative = 'two-sided', nan_policy='omit').confidence_interval(confidence_level=0.95)

    if p_value <.001:
        pvalue = '<.001'
    elif p_value < .01:
        pvalue = '<.01'
    else:
        pvalue = round(p_value, 3)
    return pvalue, round(CI[0], 3), round(CI[1], 3)