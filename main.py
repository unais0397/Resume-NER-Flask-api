from flask import Flask, request, jsonify
import config
import logging
import os
import minegold
from werkzeug.utils import secure_filename
from flask_cors import CORS
from ner_model import extract_resume_entities
import warnings
warnings.filterwarnings('ignore')


app = Flask(__name__)
CORS(app)

# Configuration
RAW_FOLDER = config.RAW_FOLDER
CLEAN_FOLDER = config.CLEAN_FOLDER
LOG_FILE = config.LOG_FILE
ALLOWED_EXTENSIONS = {'pdf'}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB

app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/minedata', methods=['POST'])
def process_file():
    try:
        if 'file' not in request.files:
            return jsonify({
                'status': 400,
                'message': 'Bad Request',
                'error': 'No file part in request'
            }), 400

        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'status': 400,
                'message': 'Bad Request',
                'error': 'No selected file'
            }), 400

        if not allowed_file(file.filename):
            return jsonify({
                'status': 415,
                'message': 'Unsupported Media Type',
                'error': 'Only PDF files are allowed'
            }), 415

        filename = secure_filename(file.filename)
        filepath = os.path.join(RAW_FOLDER, filename)
        
        os.makedirs(RAW_FOLDER, exist_ok=True)
        
        try:
            file.save(filepath)
        except Exception as e:
            return jsonify({
                'status': 500,
                'message': 'File Save Error',
                'error': f'Could not save file: {str(e)}'
            }), 500

        try:
            extracted_text = minegold.process_pdf(filepath)
            
            if not extracted_text or len(extracted_text) < 50:
                return jsonify({
                    'status': 422,
                    'message': 'Unprocessable Content',
                    'error': 'PDF is either empty or contains too little text',
                    'character_count': len(extracted_text) if extracted_text else 0
                }), 422
            
            
            entities = extract_resume_entities(extracted_text, model_path="best_resume_ner_model.pt")
                
            return jsonify({
            'status': 200,
            'message': 'Success',
            'entities': entities  # This will include entity_type: [mentions] format
            })

        except Exception as e:
            logger.error(f'Processing error: {str(e)}', exc_info=True)
            return jsonify({
                'status': 500,
                'message': 'PDF Processing Failed',
                'error': f'Could not process PDF: {str(e)}'
            }), 500

    except Exception as e:
        logger.critical(f'Server error: {str(e)}', exc_info=True)
        return jsonify({
            'status': 500,
            'message': 'Internal Server Error',
            'error': 'An unexpected error occurred'
        }), 500

if __name__ == '__main__':
    logger.info(f"Starting application on port {config.PORT}")
    app.run(host="0.0.0.0", debug=config.DEBUG, port=config.PORT)