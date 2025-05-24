# Resume Screening App

An intelligent resume screening application that uses machine learning to automatically categorize resumes into different job categories. Built with Python, Streamlit, and scikit-learn.

## Features

- Upload and process resumes in multiple formats (PDF, DOCX, TXT)
- Automatic text extraction from uploaded documents
- Machine learning-based resume categorization
- Clean and intuitive user interface
- Real-time prediction of resume categories
- Support for multiple resume formats
- Text cleaning and preprocessing
- Category prediction with confidence scores

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

The application requires the following files to function properly:
- `clf.pkl` - The trained machine learning model
- `tfidf.pkl` - The TF-IDF vectorizer
- `encoder.pkl` - The label encoder
- `UpdatedResumeDataSet.csv` - Training dataset

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Upload a resume file (PDF, DOCX, or TXT format)

4. The application will automatically:
   - Extract text from the uploaded resume
   - Clean and process the text
   - Predict the job category
   - Display the results

## Project Structure

- `app.py` - Main application file containing the Streamlit interface and processing logic
- `requirements.txt` - List of Python dependencies
- `*.pkl` files - Pre-trained models and encoders
- `UpdatedResumeDataSet.csv` - Dataset used for training the model
- `Resume Screening with Python.ipynb` - Jupyter notebook containing the model training code

## Technologies Used

- Streamlit - Web application framework
- scikit-learn - Machine learning library
- PyPDF2 - PDF processing
- python-docx - DOCX file processing
- pandas - Data manipulation and analysis
- numpy - Numerical computing

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
