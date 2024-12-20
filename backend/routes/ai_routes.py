from flask import Blueprint, request, jsonify
from openai import OpenAI
from config import Config

# Create blueprint
ai_routes = Blueprint('ai_routes', __name__)

# Initialize OpenAI client
client = OpenAI(api_key=Config.OPENAI_API_KEY)

@ai_routes.route('/api/ai/chat', methods=['POST'])
def chat_with_ai():
    try:
        data = request.get_json()
        message = data.get('message')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a helpful assistant for our application."
                },
                {"role": "user", "content": message}
            ]
        )

        ai_response = response.choices[0].message.content
        return jsonify({'response': ai_response})

    except Exception as e:
        print(f"Error in chat_with_ai: {str(e)}")
        return jsonify({'error': str(e)}), 500