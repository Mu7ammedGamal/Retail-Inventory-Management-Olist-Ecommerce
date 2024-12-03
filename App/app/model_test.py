import mlflow
import pandas as pd
import matplotlib.pyplot as plt  # Add this import statement
from data_loader import olist
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve

# Function to prepare the test data
def prepare_test_data(olist):
    # Remove the first 10 rows
    olist = olist.iloc[10:]

    olist.drop('customer_city',axis=1,inplace=True)
    olist.drop('seller_state',axis=1,inplace=True)
    olist.drop('product_category_name',axis=1,inplace=True)
    olist['arrival_time'] = olist['arrival_time'].map({'Early/OnTime': 1, 'Late': 0})
    olist['delivery_impression'] = olist['delivery_impression'].map({'Very_Fast': 4, 'Fast':3,'Neutral': 2,'Slow':1,'Worst':0})
    olist['estimated_del_impression'] = olist['estimated_del_impression'].map({'Very_Fast': 4, 'Fast':3,'Neutral': 2,'Slow':1,'Worst':0})
    olist['ship_impression'] = olist['ship_impression'].map({'Very_Fast': 4, 'Fast':3,'Neutral': 2,'Slow':1,'Worst':0})
    categorical_columns = ['payment_type', 'customer_state']
    olist = pd.get_dummies(olist, columns=categorical_columns)
    X_test = olist.drop('Score',axis=1)
    y_test = olist.Score.values

    
    return X_test, y_test

def load_model(model_name):
    model_uri = f"models:/{model_name}/latest"
    return mlflow.sklearn.load_model(model_uri)

def evaluate_model(model, X_test, y_test):
    # Make predictions
    y_pred = model.predict(X_test)

    # Evaluate the model
    metrics = classification_report(y_test, y_pred, output_dict=True)
    print(confusion_matrix(y_test, y_pred))

    # Log AUC-ROC
    auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
    
    # Print evaluation metrics
    print(f"Accuracy: {metrics['accuracy']}")
    print(f"Precision: {metrics['1.0']['precision']}")
    print(f"Recall: {metrics['1.0']['recall']}")
    print(f"F1-Score: {metrics['1.0']['f1-score']}")
    print(f"ROC AUC: {auc}")

    # Save and plot ROC curve
    fpr, tpr, thresholds = roc_curve(y_test, model.predict_proba(X_test)[:, 1])
    
    plt.figure()
    plt.plot(fpr, tpr, color='blue', label='ROC curve (area = %0.2f)' % auc)
    plt.plot([0, 1], [0, 1], color='red', linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc='lower right')
    plt.savefig("roc_curve_test.png")

def main_test_model():
    try:
        olist_data = olist
        print("Olist data:", olist_data.head())  # Debug print
        X_test, y_test = prepare_test_data(olist_data)
        model = load_model("Review_Score_Prediction")  # Replace with your model name
        evaluate_model(model, X_test, y_test)
        print("Model testing completed successfully.")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main_test_model()
