#Feature selection
def getSelectedFeatures(method = []):
    selected_columns = []

    if method == 'mySelection':
        selected_columns = ['unique_hospital_admission_id',
                            'admission_age', 'sex_female',
                            'comorbidity_score_value',
                            'SaO2',	'SpO2',
                            'vitals_tempc',
                            'vitals_heart_rate',
                            'vitals_resp_rate',
                            'vitals_mbp_ni',
                            'vitals_mbp_i',
                            'cbc_hemoglobin',
                            'cbc_platelet',
                            'cbc_wbc',
                            'bmp_sodium',
                            'bmp_potassium',
                            'bmp_bun',
                            'bmp_creatinine',
                            'bmp_bicarbonate',
                            'bmp_glucose',
                            'bmp_aniongap',
                            'bmp_lactate',
                            'hfp_albumin',
                            'sofa_past_overall_24hr',
                            'sofa_past_respiratory_24hr',
                            'sofa_past_cardiovascular_24hr',
                            'race_ethnicity_Asian',
                            'race_ethnicity_Black',
                            'race_ethnicity_HispanicLatino',
                            'race_ethnicity_Other',
                            'race_ethnicity_White'
                            ]

    return selected_columns