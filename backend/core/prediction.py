import pandas as pd
from sklearn.linear_model import LinearRegression
from django.contrib.auth.models import User
from core.models import UserProfile, Voter
import joblib

# Extract voter entries from models
voters = Voter.objects.select_related('profile').all()
voter_data = []
for voter in voters:
    voter_entry = {
        'age': voter.profile.age,
        'gender': voter.profile.gender,
        'occupation': voter.profile.occupation,
        'special_condition': voter.profile.special_condition,
        'service_time': voter.service_time
    }
    voter_data.append(voter_entry)

# Select the features (attributes) for the regression model
features = ['age', 'gender', 'occupation', 'special_condition']

def train():
    # Convert the extracted data to a pandas DataFrame
    df = pd.DataFrame(voter_data)

    # Convert categorical features to numerical using one-hot encoding
    df_encoded = pd.get_dummies(df[features], drop_first=True)

    # Select the target variable (service_time) for the regression model
    target = df['service_time']

    # Build the regression model
    regression_model = LinearRegression()

    # Train the model
    regression_model.fit(df_encoded, target)

    # Save the trained model
    joblib.dump(regression_model, 'regression_model.pkl')

def predict(new_voter):
    # Load the saved model
    loaded_model = joblib.load('regression_model.pkl')

    # Example: Use the model to predict service time for a new voter

    # Convert the new voter data to a DataFrame
    new_voter_df = pd.DataFrame([new_voter])

    # Add missing columns to the new voter data if necessary
    for feature in features:
        if feature not in new_voter_df.columns:
            new_voter_df[feature] = 0

    # Perform one-hot encoding on the new voter data
    new_voter_encoded = pd.get_dummies(new_voter_df[features], drop_first=True)

    # Ensure that new voter data has the same columns as the training data
    new_voter_encoded = new_voter_encoded.reindex(columns=df_encoded.columns, fill_value=0)

    # Predict the service time for the new voter
    predicted_service_time = loaded_model.predict(new_voter_encoded)

    print('Predicted Service Time:', predicted_service_time[0])

new_voter = {
        'age': 30,
        'occupation': 'F',
    }
train()
predict(new_voter)
