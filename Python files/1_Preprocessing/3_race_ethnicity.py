##Race and ethnicity: group and encode categories
data['race_ethnicity'] = data['race_ethnicity'] \
                                    .apply(lambda x: x if (x == "White") | (x == "Hispanic OR Latino") | (x == "Black") | (x == "Asian") \
                                        else "Other")
###One hot encoding
one_hot_encoded_data = pd.get_dummies(data, columns = ['race_ethnicity'])
one_hot_encoded_data = one_hot_encoded_data.rename(columns={'race_ethnicity_Hispanic OR Latino': 'race_ethnicity_HispanicLatino'})