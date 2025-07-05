import os

# Base directory configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# File storage configuration
RAW_FOLDER = os.path.join(BASE_DIR, "raw_pdfs")
CLEAN_FOLDER = os.path.join(BASE_DIR, "clean_text")
BLURR_FOLDER = os.path.join(BASE_DIR, "blurred_docs")

# Logging configuration
LOG_FILE = os.path.join(BASE_DIR, "application.log")

# Application settings
PORT = 8002
DEBUG = True
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_MIME_TYPES = {'application/pdf'}

# Text processing parameters
MIN_TEXT_LENGTH = 100  # Minimum characters to consider valid