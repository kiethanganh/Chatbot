from flask import Flask, render_template, request, jsonify
import simple_nlp

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get')
def get_bot_response():
    userText = request.args.get('msg')
    response = simple_nlp.chatbot_response(userText)
    return str(response)

@app.route('/new_chat', methods=['POST'])
def new_chat():
    simple_nlp.reset_conversation()
    return jsonify({"message": "Đã tạo đoạn chat mới!"})

if __name__ == '__main__':
    app.run(debug=True)
    

