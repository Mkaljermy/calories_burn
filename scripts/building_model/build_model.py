import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
import numpy as np
import joblib
import os

# Models to try
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor

def load_data(path):
    """ load cleaned data """
    return pd.read_csv(path)

def preprocess_data(data, target_column):
    """
    Prepare features and target variable.
    Exclude user_id, height, Body_Temp and separate the target column.
    """
    # Create a copy to avoid modifying the original dataframe
    X = data.drop(columns=['User_ID', target_column], errors='ignore')
    y = data[target_column]
    return X, y

def create_preprocessor():
    """Create a preprocessing pipeline for categorical and numerical features."""
    return ColumnTransformer(
        transformers=[
            ('onehot', OneHotEncoder(drop='if_binary'), ['Gender']),
            ('scaler', StandardScaler(), ['Height', 'Weight', 'Duration', 'Heart_Rate', 'Body_Temp'])
        ])
        
def initialize_models():
    """Initialize a dictionary of models to evaluate."""
    return {
        'Linear Regression': LinearRegression(),
        'Decision Tree': DecisionTreeRegressor(random_state=42),
        'Random Forest': RandomForestRegressor(random_state=42),
        'Gradient Boosting': GradientBoostingRegressor(random_state=42),
        'XGBoost': XGBRegressor(random_state=42)
    }

def evaluate_models(models, preprocessor, X_train, y_train):
    """
    Evaluate models using cross-validation and return results.
    """
    model_results = {}
    best_score = float('inf')
    best_model = None

    print('Model Evaluation:')
    print("=================")

    for name, model in models.items():
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('model', model)
        ])

        scores = cross_val_score(pipeline, X_train, y_train, 
                                cv=5, scoring='neg_mean_squared_error')
        rmse_scores = np.sqrt(-scores)
        avg_rmse = np.mean(rmse_scores)
        model_results[name] = avg_rmse

        print(f"{name}:")
        print(f"    Average RMSE: {avg_rmse:.2f}")
        print(f"  Individual Fold RMSEs: {np.round(rmse_scores, 2)}")
        
        if avg_rmse < best_score:
            best_score = avg_rmse
            best_model = name
    
    print("\nBest Model from Cross-Validation:")
    print(f"{best_model} with average RMSE: {best_score:.2f}")
    
    return best_model, model_results

def tune_model(best_model_name, models, preprocessor, X_train, y_train):
    """
    Perform hyperparameter tuning for the best model.
    """
    print("\nHyperparameter Tuning:")
    print("======================")

    best_model_instance = models[best_model_name]
    tuning_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', best_model_instance)
    ])

    param_grids = {
        'Random Forest': {
            'model__n_estimators': [100, 200],
            'model__max_depth': [None, 10, 20],
            'model__min_samples_split': [2, 5]
        },
        'XGBoost': {
            'model__n_estimators': [100, 200],
            'model__learning_rate': [0.01, 0.1],
            'model__max_depth': [3, 5]
        },
        'Gradient Boosting': {
            'model__n_estimators': [100, 200],
            'model__learning_rate': [0.01, 0.1],
            'model__max_depth': [3, 5]
        },
        'Decision Tree': {
            'model__max_depth': [None, 5, 10, 20],
            'model__min_samples_split': [2, 5, 10]
        },
        'Linear Regression': {}
    }

    param_grid = param_grids.get(best_model_name, {})

    if param_grid:
        grid_search = GridSearchCV(tuning_pipeline, param_grid, 
                                  cv=5, scoring='neg_mean_squared_error',
                                  n_jobs=-1, verbose=1)
        grid_search.fit(X_train, y_train)
        
        best_params = grid_search.best_params_
        best_tuned_model = grid_search.best_estimator_
        
        print(f"Best parameters for {best_model_name}:")
        print(best_params)
    else:
        print(f"No tuning parameters available for {best_model_name}. Using base model.")
        best_tuned_model = tuning_pipeline.fit(X_train, y_train)

    return best_tuned_model


def evaluate_test_set(model, X_test, y_test):
    """Evaluate the final model on the test set."""
    y_pred = model.predict(X_test)
    final_rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f"\nFinal RMSE on Test Set: {final_rmse:.2f}")

def save_model(model, file_path):
    """Save the trained model to a file."""
    # Create directories if they don't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    joblib.dump(model, file_path)
    print(f"\nModel saved as {file_path}")

def main():
    # Load and preprocess data
    data = load_data(f"D:\calories_burn\dataset\cleaned_data\cleaned_calories_burn.csv")
    X, y = preprocess_data(data, target_column='Calories')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(X_train.head(3))


    # Create preprocessing pipeline
    preprocessor = create_preprocessor()

    # Initialize models
    models = initialize_models()

    # Evaluate models
    best_model_name, model_results = evaluate_models(models, preprocessor, X_train, y_train)

    # Tune the best model
    best_tuned_model = tune_model(best_model_name, models, preprocessor, X_train, y_train)

    # Evaluate on test set
    evaluate_test_set(best_tuned_model, X_test, y_test)

    # Save the best model
    save_model(best_tuned_model, f"saved_model/best_calories_model.pkl")


if __name__ == "__main__":
    main()