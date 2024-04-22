from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

# Load the trained model
with open('svd.pkl', 'rb') as file:
    svd_model = pickle.load(file)

# Define a route for making predictions
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    user_id = data['user_id']
    movie_id = data['movie_id']
    
    # Make predictions using the loaded model
    prediction = svd_model.predict(user_id, movie_id)
    
    # Return the prediction as JSON
    return jsonify({'user_id': user_id, 'movie_id': movie_id, 'predicted_rating': prediction})

if __name__ == '__main__':
    app.run(debug=True)
