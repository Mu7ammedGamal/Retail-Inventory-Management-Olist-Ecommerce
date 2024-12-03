import mlflow
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
from sklearn.model_selection import train_test_split, GridSearchCV
import matplotlib.pyplot as plt
import json
import warnings
from sklearn.exceptions import ConvergenceWarning
from data_loader import olist
from sklearn.ensemble import RandomForestClassifier


# Function to set up MLflow experiment
def set_mlflow_experiment(experiment_name):
    mlflow.set_experiment(experiment_name)

# Suppress specific warnings
warnings.filterwarnings("ignore", category=UserWarning, module="mlflow.*")
warnings.filterwarnings("ignore", category=ConvergenceWarning)

def prepare_data(olist):
    # One-hot encode categorical variables
    olist.drop('customer_city',axis=1,inplace=True)
    olist.drop('seller_state',axis=1,inplace=True)
    olist.drop('product_category_name',axis=1,inplace=True)
    olist['arrival_time'] = olist['arrival_time'].map({'Early/OnTime': 1, 'Late': 0})
    olist['delivery_impression'] = olist['delivery_impression'].map({'Very_Fast': 4, 'Fast':3,'Neutral': 2,'Slow':1,'Worst':0})
    olist['estimated_del_impression'] = olist['estimated_del_impression'].map({'Very_Fast': 4, 'Fast':3,'Neutral': 2,'Slow':1,'Worst':0})
    olist['ship_impression'] = olist['ship_impression'].map({'Very_Fast': 4, 'Fast':3,'Neutral': 2,'Slow':1,'Worst':0})
    categorical_columns = ['payment_type', 'customer_state']
    olist = pd.get_dummies(olist, columns=categorical_columns)
    X = olist.drop('Score',axis=1)
    Y = olist.Score.values
    # Define features and target variable
    
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.30, stratify=Y, random_state=2022)

    return X_train, X_test, y_train, y_test

def validate_model(model, X, y):
    from sklearn.model_selection import cross_val_score
    scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')  # 5-fold cross-validation
    mlflow.log_metric("cross_val_mean_accuracy", scores.mean())
    mlflow.log_metric("cross_val_std_accuracy", scores.std())
    return scores

def train_model(X_train, y_train, X_test, y_test):
    with mlflow.start_run():
        # Hyperparameter tuning
        param_grid = {'n_estimators': [100, 200, 300]}
        grid = GridSearchCV(RandomForestClassifier(), param_grid, cv=5)
        grid.fit(X_train, y_train)

        best_model = grid.best_estimator_
        mlflow.log_param("best_estimator", grid.best_params_['n_estimators'])

        # Make predictions
        y_pred = best_model.predict(X_test)

        # Evaluate the model
        metrics = classification_report(y_test, y_pred, output_dict=True)
        print(confusion_matrix(y_test, y_pred))
        
        # Log parameters, metrics, and model with MLflow
        mlflow.log_param("model_type", "Random Forest")
        mlflow.log_param("train_size", X_train.shape[0])
        mlflow.log_param("test_size", X_test.shape[0])
        

        # Log metrics
        print(metrics)
        mlflow.log_metric("accuracy", metrics["accuracy"])
        mlflow.log_metric("precision", metrics["1.0"]["precision"])
        
        mlflow.log_metric("recall", metrics["1.0"]["recall"])
        mlflow.log_metric("f1-score", metrics["1.0"]["f1-score"])

        # Log AUC-ROC
        auc = roc_auc_score(y_test, best_model.predict_proba(X_test)[:, 1])
        mlflow.log_metric("roc_auc", auc)

        # Log the trained model
        mlflow.sklearn.log_model(best_model, "model")
        
         # Register the model
        model_uri = "runs:/{}/model".format(mlflow.active_run().info.run_id)
        mlflow.register_model(model_uri, "Review_Score_Prediction")  # Replace with your desired model name


        # Save and log ROC curve
        fpr, tpr, thresholds = roc_curve(y_test, best_model.predict_proba(X_test)[:, 1])
        plt.figure()
        plt.plot(fpr, tpr, color='blue', label='ROC curve (area = %0.2f)' % auc)
        plt.plot([0, 1], [0, 1], color='red', linestyle='--')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic')
        plt.legend(loc='lower right')
        plt.savefig("roc_curve.png")
        mlflow.log_artifact("roc_curve.png")

        # Save feature importance
        feature_importance = best_model.feature_importances_
        importance_dict = {feature: coef for feature, coef in zip(X_train.columns, feature_importance)}
        with open("feature_importance.json", "w") as f:
            json.dump(importance_dict, f)
        mlflow.log_artifact("feature_importance.json")

        return best_model, metrics

def main_train_model():
    try:
        set_mlflow_experiment("Review Score Prediction")  # Set your desired experiment name
        olist_data = olist
        print("Olist data:", olist_data.head())  # Debug print
        X_train, X_test, y_train, y_test = prepare_data(olist_data)
        model, metrics = train_model(X_train, y_train, X_test, y_test)
        print("Model training completed successfully.")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main_train_model()

