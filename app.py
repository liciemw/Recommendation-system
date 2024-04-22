from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
from surprise import SVD
from surprise import Dataset
from surprise import Reader

app = Flask(__name__)

# Load the trained model
with open('svd.pkl', 'rb') as file:
    svd_model = pickle.load(file)

# Define the Reader object
reader = Reader(rating_scale=(1, 5))

# Load data from DataFrame into Surprise Dataset
new_data = Dataset.load_from_df(new_df[['userId', 'movieId', 'rating']], reader)

# Define a route for rendering the form
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# Define a route for making predictions
@app.route('/predict', methods=['POST'])
def predict():
    ratings = {}
    for key, value in request.form.items():
        if key.startswith('rating'):
            ratings[key] = float(value)

    # Train SVD model
    svd_ = SVD(n_factors=100, reg_all=0.04)
    svd_.fit(new_data.build_full_trainset())

    # Make predictions for the user
    list_of_movies = []
    for m_id in new_df['movieId'].unique():
        list_of_movies.append((m_id, svd_.predict(1000, m_id)[3]))

    ranked_movies = sorted(list_of_movies, key=lambda x: x[1], reverse=True)

    # Return the top n recommendations using the recommended_movies function
    recommendations = recommended_movies(ranked_movies, new_df, 5)
    
    # Render recommendations in a template
    return render_template('recommendations.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
