# Resume Screening App

An intelligent resume screening application that uses machine learning to automatically categorize resumes into different job categories. Built with Python, Flask, and scikit-learn.

## Features

- Upload and process resumes in multiple formats (PDF, DOCX, TXT)
- Automatic text extraction from uploaded documents
- Machine learning-based resume categorization
- Clean and intuitive web interface
- Real-time prediction of resume categories
- Text cleaning and preprocessing
- Category prediction with confidence scores
- REST API for programmatic access

## Prerequisites

- Python 3.10+
- pip (Python package installer)
- Git (for cloning the repository)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Tamanna5/Resume-Screening-App.git
    cd Resume-Screening-App
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Required Files

The application requires the following files to function properly (place them in the `models/` directory):
- `clf.pkl` - The trained machine learning model
- `tfidf.pkl` - The TF-IDF vectorizer
- `encoder.pkl` - The label encoder

## Usage

1. Start the Flask application:
    ```bash
    python app.py
    ```

2. Open your web browser and navigate to [http://localhost:5000](http://localhost:5000)

3. Use the web interface to:
    - Paste resume text or upload a file (PDF, DOCX, or TXT)
    - View the predicted job category

4. You can also use the REST API:
    - POST to `/classify` with JSON: `{ "resume": "your resume text" }`

## Project Structure

```
resume_classifier/
├── app.py                # Main Flask application file
├── templates/            # HTML templates
│   ├── index.html
│   ├── result.html
│   └── layout.html
├── static/               # Static files (CSS, JS)
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── models/               # Directory for ML models
│   ├── tfidf.pkl
│   ├── clf.pkl
│   └── encoder.pkl
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Technologies Used

- Flask - Web application framework
- scikit-learn - Machine learning library
- PyPDF2 / python-docx - Document processing
- pandas, numpy - Data manipulation and analysis

## Model Details

The application uses a machine learning model trained on a dataset of resumes to predict job categories. The model:
- Uses TF-IDF vectorization for text processing
- Implements text cleaning and preprocessing
- Provides category predictions based on resume content

## Contributing

Feel free to submit issues and enhancement requests! To contribute:
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
