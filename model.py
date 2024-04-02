import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from pymongo import MongoClient

def train_model_and_predict(input_data):
    # Load dataset
    heart_data = pd.read_csv('./dataset.csv')
    # Separate features and target variable
    X = heart_data.drop(columns='target', axis=1)
    Y = heart_data['target']
    # Split data into train and test sets
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=2)

    # Train the model
    model = LogisticRegression()
    model.fit(X_train, Y_train)

    # Perform prediction
    prediction = model.predict([input_data])[0]

    return prediction

def save_to_mongodb(input_data, prediction):
    # Establish connection to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['heart_disease_db']
    collection = db['user_data']

    # Insert input data and prediction result into MongoDB
    heart_data_columns = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
    input_data_dict = dict(zip(heart_data_columns, input_data))

    data = {
        'input_data': input_data_dict,
        'prediction': int(prediction)
    }
    collection.insert_one(data)

    client.close()
