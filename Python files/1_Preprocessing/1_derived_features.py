##Derived features
data.dropna(subset=['sofa_past_overall_24hr',
                    'sofa_past_coagulation_24hr',
                    'sofa_past_liver_24hr',
                    'sofa_past_cardiovascular_24hr',
                    'sofa_past_cns_24hr',
                    'sofa_past_renal_24hr',
                    'sofa_future_overall_24hr',
                    'sofa_future_coagulation_24hr',
                    'sofa_future_liver_24hr',
                    'sofa_future_cardiovascular_24hr',
                    'sofa_future_cns_24hr',
                    'sofa_future_renal_24hr',
                    'in_hospital_mortality'], inplace = True)

###SOFA respiratory
data['sofa_past_respiratory_24hr'] = (data['sofa_past_overall_24hr']
                                    - data['sofa_past_coagulation_24hr']
                                    - data['sofa_past_liver_24hr']
                                    - data['sofa_past_cardiovascular_24hr']
                                    - data['sofa_past_cns_24hr']
                                    - data['sofa_past_renal_24hr'])

data['sofa_future_respiratory_24hr'] = (data['sofa_future_overall_24hr']
                                    - data['sofa_future_coagulation_24hr']
                                    - data['sofa_future_liver_24hr']
                                    - data['sofa_future_cardiovascular_24hr']
                                    - data['sofa_future_cns_24hr']
                                    - data['sofa_future_renal_24hr'])

data['sofa_future_respiratory_24hr'] = data['sofa_future_respiratory_24hr'] \
                                            .apply(lambda x: 1 if (x > 0) \
                                                else 0)

###SOFA overall increase
data['sofa_overall_increased'] = ((data['sofa_future_overall_24hr'] - data['sofa_past_overall_24hr']) >= 2)