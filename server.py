from flask import Flask, render_template, request, jsonify
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route('/')
def index():
    """Renders the homepage."""
    return render_template('index.html')

@app.route('/emotionDetector', methods=['POST'])
def emotion_detector_route():
    """Processes text input and returns emotion score."""
    text_to_analyze = request.form.get('text', '')
    
    if not text_to_analyze:
        return "Invalid input! Please provide text to analyze."

    # Get emotion scores from the EmotionDetection package
    response = emotion_detector(text_to_analyze)
    response_dict = json.loads(response)

    # Check for missing keys (e.g., API failure)
    if 'dominant_emotion' not in response_dict:
        return "Error: Could not analyze emotions. Please try again."

    # Extract emotion scores
    anger = response_dict.get('anger', 0.0)
    disgust = response_dict.get('disgust', 0.0)
    fear = response_dict.get('fear', 0.0)
    joy = response_dict.get('joy', 0.0)
    sadness = response_dict.get('sadness', 0.0)
    dominant_emotion = response_dict['dominant_emotion']

    # Format the output string
    output = (
        f"For the given statement, the system response is "
        f"'anger': {anger}, 'disgust': {disgust}, 'fear': {fear}, "
        f"'joy': {joy} and 'sadness': {sadness}. "
        f"The dominant emotion is {dominant_emotion}."
    )
    
    return output

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)