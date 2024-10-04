#Replace missing labs and vitals with their normal ranges
midpoint_map = {
    'cbc_mch': 29.8,
    'cbc_mchc': 33.6,
    'cbc_mcv': 90.0,
    'cbc_platelet': 300.0,
    'cbc_rbc': 5.0,
    'cbc_rdw': 13.0,
    'cbc_wbc': 7.25,
    'coag_inr': 1.0,
    'coag_pt': 10.75,
    'coag_ptt': 28.5,
    'coag_fibrinogen': 300.0,
    'hfp_alt': 31.5,
    'hfp_alp': 95.5,
    'hfp_ast': 25.0,
    'hfp_bilirubin_total': 0.65,
    'hfp_albumin': 4.4,
    'bmp_aniongap': 10.0,
    'bmp_bicarbonate': 25.0,
    'bmp_bun': 13.5,
    'bmp_calcium': 9.5,
    'bmp_chloride': 101.0,
    'bmp_creatinine': 0.9,
    'bmp_glucose': 84.5,
    'bmp_sodium': 140.0,
    'bmp_potassium': 4.25,
    'ph': 7.4,
    'bmp_lactate': 1.05,
    'vitals_heart_rate': 80.0,
    'vitals_mbp_ni': 87.5,
    'vitals_mbp_i': 87.5,
    'vitals_resp_rate': 16.0,
    'vitals_tempc': 36.65
}

data_filled = one_hot_encoded_data.fillna(midpoint_map)

data_filled['cbc_hemoglobin'][(data_filled['cbc_hemoglobin'].isnull()) & (data_filled['sex_female'] == 0)] = 15.5
data_filled['cbc_hemoglobin'][(data_filled['cbc_hemoglobin'].isnull()) & (data_filled['sex_female'] == 1)] = 13.7
data_filled['cbc_hematocrit'][(data_filled['cbc_hematocrit'].isnull()) & (data_filled['sex_female'] == 0)] = 44.4
data_filled['cbc_hematocrit'][(data_filled['cbc_hematocrit'].isnull()) & (data_filled['sex_female'] == 1)] = 39.7

data_filled = data_filled.drop(['weight_admission', 'height_admission', 'BMI_admission'], axis=1)