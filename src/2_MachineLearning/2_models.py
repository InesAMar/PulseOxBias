#Models
models = [
        LogisticRegression()
        ,
        xgb.XGBClassifier(objective= "binary:logistic")
          ]