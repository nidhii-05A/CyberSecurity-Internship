from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__)

blocklist = {'password': True, 'pwned': True}

def log_violation(prompt):
    with open('violations.txt', 'a') as file:
        file.write(f"{prompt}\n")
        print('Violation detected and logged')

def response_checker(response):
    for word in blocklist:
        if word in response.lower():
            log_violation(response)
            return True, "That request goes against my safety guidelines. I'm here to provide helpful and appropriate information."

    return False, response

@app.route('/')
def home():
    return render_template('chatbot.html')

@app.route('/chat', methods=['POST'])
@app.route('/chat', methods=['POST'])
def chatbot():
    data = request.get_json()
    message = data.get('message')

    if not message:
        return jsonify({'response': 'No message provided'}), 400

    # Sanitize message
    sanitized_message = re.sub(r'[^\w\s.]', '', message)

    # Check for blocklisted words in the sanitized message
    is_violation, final_response = response_checker(sanitized_message)
    
    return jsonify({'response': final_response})
if __name__ == "__main__":
    app.run(debug=True)