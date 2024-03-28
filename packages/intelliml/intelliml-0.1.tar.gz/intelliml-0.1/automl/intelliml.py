from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import VotingClassifier
import pickle



from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import VotingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor, BaggingRegressor, ExtraTreesRegressor
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.neighbors import KNeighborsRegressor
from lightgbm import LGBMRegressor
# from catboost import CatBoostRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import VotingRegressor

import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

class IntelliML:
    def __init__(self, dataframe):
        """
        Initializes the AutoML instance with a provided DataFrame.
        """
        if not isinstance(dataframe, pd.DataFrame):
            raise ValueError("The input is not a valid pandas DataFrame.")
        self.df = dataframe
        print("DataFrame loaded successfully.")
        self.trained_models = {}
        self.categories = {}
        self.dropfeatures = []
        self.target_variable = None
        
    def handle_missing_values(self, technique, constant_value=None, inplace=False):
        """
        Handles missing values in the dataset using various techniques, attempting to preserve original datatypes.
        """
        if technique not in range(1, 7):
            raise ValueError("Invalid imputation technique number. Please enter a number between 1 and 6.")
        
        if technique == 6 and constant_value is None:
            constant_value = -99999

        # Define the imputer based on the selected technique
        imputers = {
            1: ('mean', None),
            2: ('median', None),
            3: ('most_frequent', None),
            4: ('knn', 5),
            5: ('knn', 10),
            6: ('constant', constant_value)
        }

        strategy, param = imputers[technique]
        
        # Iterate over each column to apply the appropriate imputation
        for col in self.df.columns:
            original_dtype = self.df[col].dtype
            if strategy in ['mean', 'median', 'most_frequent', 'constant']:
                imputer = SimpleImputer(strategy=strategy, fill_value=constant_value if strategy == 'constant' else None)
                self.df[col] = imputer.fit_transform(self.df[[col]])
            elif strategy == 'knn':
                if self.df[col].dtype == np.dtype('O'):  # Skip object types for KNN
                    continue
                imputer = KNNImputer(n_neighbors=param)
                self.df[col] = imputer.fit_transform(self.df[[col]])
            
            # Attempt to convert back to original datatype if not object
            if original_dtype != np.dtype('O') and original_dtype != float:
                try:
                    self.df[col] = self.df[col].astype(original_dtype)
                except ValueError:
                    # Catch cases where conversion back is not possible due to NaNs
                    pass

        return self.df if inplace else self.df.copy()

    def replace_symbols(self, old_value, new_value):
        """
        Replaces specified symbols in the DataFrame.
        """
        self.df.replace(old_value, new_value, inplace=True)

    def feature_selection(self):
        """
        Interactively allows users to select which columns to keep or drop.
        """
        print("Column names:\n")
        for i, col in enumerate(self.df.columns):
            print(f"{i + 1}. {col}")
        cols_to_drop = input("Enter the ids of the columns to drop, separated by commas: ").split(",")
        if cols_to_drop[0].lower() != 'none':
            cols_to_drop = [self.df.columns[int(i) - 1] for i in cols_to_drop]
            self.df.drop(cols_to_drop, axis=1, inplace=True)
    
    def handle_non_numerical_data(self):
            numerical_dict = {}
            for column in self.df.columns:
                text_digit_vals = {}
                
                # Function to convert to integer
                def convert_to_int(val):
                    return text_digit_vals[val]
                
                # Check if column is not already numeric
                if self.df[column].dtype != np.int64 and self.df[column].dtype != np.float64:
                    column_contents = self.df[column].values.tolist()
                    unique_elements = set(column_contents)
                    x = 0
                    for unique in unique_elements:
                        if unique not in text_digit_vals:
                            text_digit_vals[unique] = x
                            if column not in numerical_dict:
                                numerical_dict[column] = {}
                            numerical_dict[column][unique] = x
                            x += 1
    
                    # Apply mapping to the DataFrame column
                    self.df[column] = list(map(convert_to_int, self.df[column]))
            self.categories = numerical_dict
            return self.df, numerical_dict


    def create_new_feature(self):
        """
        Allows creation of a new feature based on operations on existing features.
        """
        print("Existing features:")
        for i, col in enumerate(self.df.columns):
            print(f"{i + 1}. {col}")
        new_feature_name = input("Enter the name of the new feature: ")
        feature_ids = input("Enter the IDs of the existing features to use (comma-separated): ").split(",")
        operation = int(input("Select the operation to perform (1. Addition, 2. Subtraction, 3. Multiplication, 4. Division, 5. Modulo): "))
        operations = {
            1: lambda x: np.sum(x, axis=1),
            2: lambda x: np.subtract(*x.T),
            3: lambda x: np.prod(x, axis=1),
            4: lambda x: np.divide(*x.T),
            5: lambda x: np.mod(*x.T)
        }

        selected_features = self.df.iloc[:, [int(f_id.strip())-1 for f_id in feature_ids]]
        self.df[new_feature_name] = operations[operation](selected_features)

    def merge_datasets(self, df2):
        """
        Merges another DataFrame with the current one based on user input.
        """
        if not isinstance(df2, pd.DataFrame):
            print("Error: The second dataset is not a valid DataFrame.")
            return

        print("Column names for first dataset:\n")
        for i, col in enumerate(self.df.columns):
            print(f"{i+1}. {col}")
        print("\nColumn names for second dataset:\n")
        for i, col in enumerate(df2.columns):
            print(f"{i+1}. {col}")

        merge_type = input("Enter merge type (left, right, inner, outer): ").lower()
        merge_column = input("Enter column to merge on: ")

        if merge_type not in ["left", "right", "inner", "outer"]:
            print("Invalid merge type specified. Defaulting to 'inner'.")
            merge_type = "inner"
        if merge_column not in self.df.columns or merge_column not in df2.columns:
            print("Merge column not found in one or both DataFrames. Cannot merge.")
            return

        self.df = pd.merge(self.df, df2, on=merge_column, how=merge_type)
        print("\nMerged DataFrame:\n")
        print(self.df.head())





    def dataset_report(self):
        # Initial checks for missing values and datatypes
        missing_values = self.df.isnull().sum()
        categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        print("***Data report***")
        # Report missing values
        if missing_values.any():
            print("Missing values found in columns:", missing_values[missing_values > 0].index.tolist())
        else:
            print("No missing values found.")

        # Report categorical values
        if len(categorical_cols) > 0:
            print("Categorical columns found:", categorical_cols.tolist())
        else:
            print("No categorical columns found.")
        
        # Check for symbols in numeric columns
        symbol_check = {col: self.df[col].apply(lambda x: not str(x).replace('.', '', 1).isdigit()).any() for col in numeric_cols}
        symbols_found = [col for col, has_symbol in symbol_check.items() if has_symbol]
        if symbols_found:
            print("Symbols found in numeric columns:", symbols_found)
        else:
            print("No symbols found in numeric columns.")

    def model_classification(self, split_ratio=0.3, algorithms=None):
        # Print column names for user to select target variable
        print("Column names:")
        for col in self.df.columns:
            print(col)
        target_variable = input("Enter the name of the target variable: ")
        
        # Splitting the data into training and testing sets
        X = self.df.drop(columns=[target_variable])
        y = self.df[target_variable]
        xtrain, xtest, ytrain, ytest = train_test_split(X, y, test_size=split_ratio, random_state=0)
        
        # Initializing the classifiers
        lr = LogisticRegression()
        gnb = GaussianNB()
        knn = KNeighborsClassifier()
        dt = DecisionTreeClassifier()
        svm = SVC(kernel='poly')

        classifiers = {'lr': lr, 'gnb': gnb, 'knn': knn, 'dt': dt, 'svm': svm}

        if algorithms is None:
            algorithms = classifiers.values()
        elif not algorithms:
            print("No algorithms specified.")
            return

        for clf in algorithms:
            if isinstance(clf, str):
                if clf not in classifiers:
                    print(f"Unknown algorithm: {clf}")
                    continue
                clf = classifiers[clf]

            clf_name = clf.__class__.__name__
            clf.fit(xtrain, ytrain)
            y_pred = clf.predict(xtest)
            acc = accuracy_score(ytest, y_pred)
            precision = precision_score(ytest, y_pred, average='weighted')
            recall = recall_score(ytest, y_pred, average='weighted')
            f1 = f1_score(ytest, y_pred, average='weighted')
            print(f"Accuracy of {clf_name}: {acc}")
            print(f"Precision of {clf_name}: {precision}")
            print(f"Recall of {clf_name}: {recall}")
            print(f"F1-score of {clf_name}: {f1}")
            print()
            
            # Save trained model
            self.trained_models[clf_name] = clf

        # Using ensemble modeling
        if all(isinstance(clf, (LogisticRegression, GaussianNB, KNeighborsClassifier, DecisionTreeClassifier, SVC)) for clf in algorithms):
            voting_clf = VotingClassifier(estimators=[(clf_name, clf) for clf_name, clf in self.trained_models.items()], voting='hard')
            voting_clf.fit(xtrain, ytrain)
            y_pred_voting = voting_clf.predict(xtest)
            acc_voting = accuracy_score(ytest, y_pred_voting)
            precision_voting = precision_score(ytest, y_pred_voting, average='weighted')
            recall_voting = recall_score(ytest, y_pred_voting, average='weighted')
            f1_voting = f1_score(ytest, y_pred_voting, average='weighted')
            print(f"Accuracy of Ensemble Model: {acc_voting}")
            print(f"Precision of Ensemble Model: {precision_voting}")
            print(f"Recall of Ensemble Model: {recall_voting}")
            print(f"F1-score of Ensemble Model: {f1_voting}")
            print()

            # Save the ensemble model
            self.trained_models['EnsembleModel'] = voting_clf



    
    def model_regression(self, split_ratio=0.3, algorithms=None):
        # Print column names for user to select target variable
        print("Column names:")
        for col in self.df.columns:
            print(col)
        target_variable = input("Enter the name of the target variable: ")
    
        # Splitting the data into training and testing sets
        X = self.df.drop(columns=[target_variable])
        y = self.df[target_variable]
        xtrain, xtest, ytrain, ytest = train_test_split(X, y, test_size=split_ratio, random_state=0)
    
        # Initializing the regression models
        regression_models = {
            'lr': LinearRegression(),
            'ridge': Ridge(alpha=0.5),
            'lasso': Lasso(alpha=0.1),
            'knn': KNeighborsRegressor(n_neighbors=5),
            'en': ElasticNet(alpha=0.1, l1_ratio=0.5),
            'dt': DecisionTreeRegressor(),
            'rf': RandomForestRegressor(),
            'gbr': GradientBoostingRegressor(),
            'abr': AdaBoostRegressor(),
            'br': BaggingRegressor(),
            'etr': ExtraTreesRegressor(),
            'xgb': XGBRegressor(),
            'lgbm': LGBMRegressor()}
        #     'cat': CatBoostRegressor(verbose=False)
        # }
    
        if algorithms is None:
            algorithms = regression_models.keys()
        elif not algorithms:
            print("No algorithms specified.")
            return
    
        for algo in algorithms:
            if algo not in regression_models:
                print(f"Unknown algorithm: {algo}")
                continue
    
            model = regression_models[algo]
            model_name = model.__class__.__name__
    
            # Check if custom parameters are provided
            if isinstance(algorithms, dict) and algo in algorithms:
                model.set_params(**algorithms[algo])
    
            model.fit(xtrain, ytrain)
            y_pred = model.predict(xtest)
            mse = mean_squared_error(ytest, y_pred)
            r2 = r2_score(ytest, y_pred)
            print(f"Mean Squared Error of {model_name}: {mse}")
            print(f"R2 Score of {model_name}: {r2}")
            print()
    
            # Save trained model
            self.trained_models[model_name] = model
    
        # Using ensemble modeling
        ensemble_algorithms = [reg for reg in algorithms if reg in regression_models.values()]
        if ensemble_algorithms:
            ensemble_models = [(model_name, self.trained_models[model_name]) for model_name in ensemble_algorithms]
            voting_reg = VotingRegressor(estimators=ensemble_models)
            voting_reg.fit(xtrain, ytrain)
            y_pred_voting = voting_reg.predict(xtest)
            mse_voting = mean_squared_error(ytest, y_pred_voting)
            r2_voting = r2_score(ytest, y_pred_voting)
            print(f"Mean Squared Error of Ensemble Model: {mse_voting}")
            print(f"R2 Score of Ensemble Model: {r2_voting}")
            print()
    
            # Save the ensemble model
            self.trained_models['EnsembleModel'] = voting_reg
    










    def display_columns(self):
        print("Column names:")
        for col in self.df.columns:
            print(col)
        self.target_variable = input("Enter the name of the target variable: ")
        self.prepare_data()
    
    def prepare_data(self):
        # Preparing the data
        X = self.df.drop(columns=[self.target_variable])
        y = self.df[self.target_variable]

        # Encoding the target variable if it's categorical
        if y.dtype == 'object':
            le = LabelEncoder()
            y = le.fit_transform(y)
        
        self.X = X
        self.y = y
        self.evaluate_feature_impact()

    def evaluate_feature_impact(self):
        # Initial RandomForestClassifier setup
        model = RandomForestClassifier(n_estimators=100, random_state=42)

        # Calculate the baseline accuracy with all features
        baseline_accuracy = cross_val_score(model, self.X, self.y, cv=5, scoring='accuracy').mean()
        print(f"\nBaseline accuracy with all features: {baseline_accuracy:.4f}")

        # Store the impact of removing each feature
        feature_impact = []

        # Iterate through each feature to assess its impact on model accuracy
        for feature in self.X.columns:
            # Drop the current feature
            X_temp = self.X.drop(columns=[feature])
            
            # Recalculate accuracy without the feature
            new_accuracy = cross_val_score(model, X_temp, self.y, cv=5, scoring='accuracy').mean()
            
            # Calculate the impact and add it to the list
            impact = baseline_accuracy - new_accuracy
            feature_impact.append((feature, impact, new_accuracy))

        # Sort features by their impact on accuracy
        feature_impact.sort(key=lambda x: x[1], reverse=True)

        # Display the results
        print("\nFeature impact on model accuracy (sorted):")
        for feature, impact, acc_without_feature in feature_impact:
            print(f"{feature}: Impact = {impact:.4f}, Accuracy without feature = {acc_without_feature:.4f}")

        # Identifying features to drop based on impact threshold
        threshold = -0.005  # Negative impact indicates performance degradation
        features_to_keep = [f for f, impact, _ in feature_impact if impact > threshold]
        features_to_drop = [f for f, impact, _ in feature_impact if impact <= threshold]

        print("\nFeatures to keep:", features_to_keep)
        print("Features to consider dropping:", features_to_drop)
        self.dropfeatures = features_to_drop 

# Example usage
# df = pd.read_csv("Iris.csv")  # Replace with your DataFrame
# selector = FeatureSelector(df)
# selector.display_columns()
    
    def save_model(self):
        if not self.trained_models:
            print("No models have been trained yet.")
            return
    
        print("Trained models:")
        for idx, model_name in enumerate(self.trained_models.keys()):
            print(f"{idx + 1}. {model_name}")
    
        model_idx = int(input("Enter the index of the model you want to save: ")) - 1
    
        try:
            selected_model_name = list(self.trained_models.keys())[model_idx]
            selected_model = self.trained_models[selected_model_name]
            with open(f"{selected_model_name}.pickle", 'wb') as file:
                pickle.dump(selected_model, file)
            print(f"Model '{selected_model_name}' saved successfully.")
        except IndexError:
            print("Invalid index. Please select a valid index from the list.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            
    def use_model(self, model_file, input_values):
        with open(model_file, "rb") as file:
            model = pickle.load(file)
    
        input_values = np.array([input_values])
        predict = model.predict(input_values)
        return predict[0]



    def automate(self, learning, testsize = 0.3):
        self.handle_non_numerical_data()
        self.display_columns()
        try:
            self.df.drop(self.dropfeatures, axis=1, inplace=True)
        except Exception as e:
            pass
        self.dataset_report()
        self.df.fillna(-99999, inplace=True)
        self.handle_non_numerical_data()
        X = self.df.drop(columns=[self.target_variable])
        y = self.df[self.target_variable]
        xtrain, xtest, ytrain, ytest = train_test_split(X, y, test_size= testsize, random_state=0)
        if learning == 1:
            models = [
                ('lr', LinearRegression()),
                ('ridge', Ridge(alpha=0.5)),
                ('lasso', Lasso(alpha=0.1)),
                ('knn', KNeighborsRegressor(n_neighbors=5)),
                ('en', ElasticNet(alpha=0.1, l1_ratio=0.5)),
                ('dt', DecisionTreeRegressor()),
                ('rf', RandomForestRegressor(n_estimators=100)),
                ('gbr', GradientBoostingRegressor(n_estimators=100)),
                ('abr', AdaBoostRegressor(n_estimators=100)),
                ('br', BaggingRegressor(n_estimators=10)),
                ('etr', ExtraTreesRegressor(n_estimators=100)),
                ('xgb', XGBRegressor(use_label_encoder=False, eval_metric='logloss'))
                
            ]
            
            # Fit all models
            for name, model in models:
                model.fit(xtrain, ytrain)
                y_pred = model.predict(xtest)
                mse = mean_squared_error(ytest, y_pred)
                r2 = r2_score(ytest, y_pred)
                # print(f"{name} - Mean Squared Error: {mse}, R2 Score: {r2}")
            
            # Create the ensemble model with the fitted models
            ensemble_model = VotingRegressor(estimators=models)
            
            # Fit the ensemble model
            ensemble_model.fit(xtrain, ytrain)
            
            # Predict and evaluate the ensemble model
            y_pred_ensemble = ensemble_model.predict(xtest)
            mse_ensemble = mean_squared_error(ytest, y_pred_ensemble)
            r2_ensemble = r2_score(ytest, y_pred_ensemble)
            print(f"Ensemble Model - Mean Squared Error: {mse_ensemble}, R2 Score: {r2_ensemble}")
            
            # Save the ensemble model to a pickle file
            with open("ensemble_model_regression.pickle", "wb") as f:
                pickle.dump(ensemble_model, f)
            
            print("Ensemble model saved as 'ensemble_model_regression.pickle'.")
        elif learning == 0:
            classifiers = [
                ('lr', LogisticRegression(max_iter=1000)),
                ('gnb', GaussianNB()),
                ('knn', KNeighborsClassifier()),
                ('dt', DecisionTreeClassifier()),
                ('svm', SVC(kernel='poly', probability=True))  # Ensure probability is True for SVC in VotingClassifier
            ]
            
            # Fit all classifiers and print their performance
            for name, clf in classifiers:
                clf.fit(xtrain, ytrain)
                y_pred = clf.predict(xtest)
                acc = accuracy_score(ytest, y_pred)
                precision = precision_score(ytest, y_pred, average='weighted')
                recall = recall_score(ytest, y_pred, average='weighted')
                f1 = f1_score(ytest, y_pred, average='weighted')
                # print(f"{name} - Accuracy: {acc}, Precision: {precision}, Recall: {recall}, F1-score: {f1}")
            
            # Create the ensemble model with the fitted classifiers
            ensemble_clf = VotingClassifier(estimators=classifiers, voting='soft')
            
            # Fit the ensemble model
            ensemble_clf.fit(xtrain, ytrain)
            
            # Predict and evaluate the ensemble model
            y_pred_ensemble = ensemble_clf.predict(xtest)
            acc_ensemble = accuracy_score(ytest, y_pred_ensemble)
            precision_ensemble = precision_score(ytest, y_pred_ensemble, average='weighted')
            recall_ensemble = recall_score(ytest, y_pred_ensemble, average='weighted')
            f1_ensemble = f1_score(ytest, y_pred_ensemble, average='weighted')
            print(f"Ensemble Model - Accuracy: {acc_ensemble}, Precision: {precision_ensemble}, Recall: {recall_ensemble}, F1-score: {f1_ensemble}")
            
            # Save the ensemble model to a pickle file
            with open("ensemble_model_classification.pickle", "wb") as f:
                pickle.dump(ensemble_clf, f)
            
            print("Ensemble model saved as 'ensemble_model_classification.pickle'.")
        else:
            print("Learning Not Mentioned")
        print("Automatic Machine Learning done on the given dataframe")
                        

        
