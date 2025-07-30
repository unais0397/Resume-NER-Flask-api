# Resume NER Flask API

A Flask-based REST API for extracting named entities from resume PDFs using a fine-tuned BERT model for Named Entity Recognition (NER).

## Features

- **PDF Processing**: Extract text from PDF resumes with advanced cleaning and preprocessing
- **Named Entity Recognition**: Extract entities like names, skills, companies, degrees, locations, etc.
- **RESTful API**: Simple HTTP endpoints for easy integration
- **CORS Support**: Cross-origin resource sharing enabled
- **Error Handling**: Comprehensive error handling and logging
- **File Validation**: Secure file upload with size and type validation

## Extracted Entities

The API extracts the following entity types from resumes:
- **NAME**: Person's name
- **EMAIL**: Email addresses
- **SKILLS**: Technical skills and competencies
- **COMPANY**: Company names and organizations
- **DESIGNATION**: Job titles and positions
- **DEGREE**: Educational degrees and qualifications
- **COLLEGE NAME**: Educational institutions
- **LOCATION**: Geographic locations and addresses

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd NER_Flask_API
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download the pre-trained model:
   - The model file `best_resume_ner_model.pt` should be placed in the root directory
   - This is a large file (416MB) and may need to be downloaded separately

## Usage

### Starting the Server

```bash
python main.py
```

The server will start on `http://localhost:8002` by default.

### API Endpoints

#### POST /minedata

Extract named entities from a resume PDF.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: PDF file in the `file` field

**Example using curl:**
```bash
curl -X POST -F "file=@resume.pdf" http://localhost:8002/minedata
```

**Response:**
```json
{
  "status": 200,
  "message": "Success",
  "entities": {
    "NAME": ["John Doe"],
    "EMAIL": ["john.doe@email.com"],
    "SKILLS": ["Python", "Machine Learning", "Flask"],
    "COMPANY": ["Tech Corp", "Startup Inc"],
    "DESIGNATION": ["Software Engineer", "Data Scientist"],
    "DEGREE": ["Bachelor of Science", "Master of Computer Science"],
    "COLLEGE NAME": ["University of Technology"],
    "LOCATION": ["San Francisco, CA"]
  }
}
```

**Error Responses:**

- `400 Bad Request`: No file provided or invalid file
- `415 Unsupported Media Type`: Non-PDF file uploaded
- `422 Unprocessable Content`: PDF is empty or contains insufficient text
- `500 Internal Server Error`: Server processing error

## Configuration

Edit `config.py` to customize:
- Port number (default: 8002)
- Debug mode (default: True)
- File size limits (default: 5MB)
- Folder paths for file storage

## Project Structure

```
NER_Flask_API/
├── main.py                 # Flask application entry point
├── ner_model.py           # NER model implementation
├── minegold.py            # PDF processing utilities
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── best_resume_ner_model.pt  # Pre-trained BERT model
├── raw_pdfs/             # Directory for uploaded PDFs
└── README.md             # This file
```

## Model Details

The API uses a fine-tuned BERT model (`bert-base-uncased`) trained specifically for resume entity extraction. The model:

- Supports 8 entity types
- Uses BIO tagging scheme (Begin-Inside-Outside)
- Maximum sequence length: 256 tokens
- Runs on CPU or GPU (CUDA if available)

## Development

### Training the Model

The model was trained using the notebook `Model Creation.ipynb` which contains:
- Data preprocessing
- Model training pipeline
- Evaluation metrics
- Model saving

### Adding New Entity Types

To add new entity types:
1. Update the `unique_labels` list in `ner_model.py`
2. Retrain the model with the new labels
3. Update the API documentation

## Dependencies

- **Flask**: Web framework
- **PyTorch**: Deep learning framework
- **Transformers**: BERT model implementation
- **pdfminer.six**: PDF text extraction


