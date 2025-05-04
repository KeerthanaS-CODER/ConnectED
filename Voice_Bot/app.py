from flask import Flask, render_template, request, jsonify
import wikipedia
import logging

# Initialize Flask
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        query = data.get('query')

        if not query:
            msg = "Please say something to search."
            return jsonify({'spoken_text': msg, 'image': 'talkingface.jpeg'})

        logger.info(f"Processing query: {query}")
        info = wikipedia.summary(query, sentences=2)
        return jsonify({'spoken_text': info, 'image': 'talkingface.jpeg'})

    except wikipedia.exceptions.DisambiguationError as e:
        msg = f"Your question is too broad. Try asking about: {', '.join(e.options[:3])}."
        logger.warning(f"DisambiguationError for query '{query}': {str(e)}")
        return jsonify({'spoken_text': msg, 'image': 'talkingface.jpeg'})

    except wikipedia.exceptions.PageError:
        msg = f"Sorry, I couldn't find anything about '{query}'."
        logger.warning(f"PageError for query '{query}'")
        return jsonify({'spoken_text': msg, 'image': 'talkingface.jpeg'})

    except Exception as e:
        msg = "Sorry, I had trouble finding that information."
        logger.error(f"Unexpected error for query '{query}': {str(e)}")
        return jsonify({'spoken_text': msg, 'image': 'talkingface.jpeg'})

if __name__ == '__main__':
    app.run(debug=True, port=1010)