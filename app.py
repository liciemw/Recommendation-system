from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)

# Load the recommendation function from the pickle file
with open('svd.pkl', 'rb') as file:
    recommend_movies = pickle.load(file)

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
    
    # Assuming you have a function to generate recommendations based on ratings
    recommendations = recommend_movies(ratings)
    
    return render_template('recommendations.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)

