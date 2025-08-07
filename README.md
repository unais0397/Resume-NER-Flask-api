# Resume NER Flask API

Flask REST API for extracting named entities from resume PDFs using fine-tuned BERT model.

## Features

- PDF text extraction and preprocessing
- Named Entity Recognition (8 entity types)
- File validation and error handling

## Extracted Entities

- **NAME**: Person's name
- **EMAIL**: Email addresses  
- **SKILLS**: Technical skills
- **COMPANY**: Company names
- **DESIGNATION**: Job titles
- **DEGREE**: Educational degrees
- **COLLEGE NAME**: Educational institutions
- **LOCATION**: Geographic locations

## Quick Start

```bash
# Clone and install
git clone https://github.com/unais0397/Resume-NER-Flask-api.git
cd Resume-NER-Flask-api
pip install -r requirements.txt

# Add model file (416MB) to root directory
# Download: best_resume_ner_model.pt

# Run server
python main.py
```

Server runs on `http://localhost:8002`

## API Usage

**Endpoint:** `POST /minedata`

**Request:** PDF file via `multipart/form-data`

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
    "EMAIL": ["john@email.com"],
    "SKILLS": ["Python", "ML"],
    "COMPANY": ["Tech Corp"],
    "DESIGNATION": ["Engineer"],
    "DEGREE": ["BS Computer Science"],
    "COLLEGE NAME": ["University"],
    "LOCATION": ["San Francisco"]
  }
}
```

## Configuration

Edit `config.py` for:
- Port (default: 8002)
- Debug mode
- File size limits
- Storage paths

## Project Structure

```
├── main.py                 # Flask app
├── ner_model.py           # NER model
├── minegold.py            # PDF processing
├── config.py              # Configuration
├── requirements.txt       # Dependencies
├── best_resume_ner_model.pt  # Model file
└── raw_pdfs/             # Upload directory
```

## Model

- BERT-based NER model
- 8 entity types with BIO tagging
- 256 token sequence length
- CPU/GPU compatible

## Dependencies

- Flask, PyTorch, Transformers, pdfminer.six


