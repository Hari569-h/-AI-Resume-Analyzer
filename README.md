# AI Resume Ranker

An AI-powered web application that compares a candidate's resume with a job description to provide a match score, identify missing skills, suggest ATS optimizations, and generate a downloadable PDF report.

## 🎯 Features

- **Resume Analysis**: Upload a PDF resume and paste a job description for AI analysis
- **Match Score**: Get a 0-100 score indicating how well the resume matches the job requirements
- **Missing Skills**: Identify key skills and keywords missing from the resume
- **ATS Optimization**: Receive suggestions to make the resume more ATS-friendly
- **PDF Report**: Download a comprehensive analysis report as a PDF

## 🛠️ Technologies Used

- **Frontend/UI**: Streamlit
- **Backend/AI**: Python + Google Generative AI (Gemini)
- **Resume Parsing**: PyPDF2
- **PDF Report Export**: fpdf
- **Environment Variables**: python-dotenv

## 🚀 Setup & Installation

### Local Development

1. **Clone the repository**

```bash
git clone <repository-url>
cd ai-resume-ranker
```

2. **Create a virtual environment**

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the root directory and add your Google API key:

```
GOOGLE_API_KEY=your_gemini_api_key_here
```

You can obtain a Gemini API key from the [Google AI Studio](https://makersuite.google.com/app/apikey).

5. **Run the application**

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`.

## 🌐 Deployment on Streamlit Cloud

1. Push your code to a GitHub repository
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Click on "New app"
4. Connect your GitHub repository
5. Set the main file path to `app.py`
6. Add your Google API key to the Streamlit Cloud secrets:
   - Go to "Advanced settings" > "Secrets"
   - Add the following in the text area:
     ```
     GOOGLE_API_KEY=your_gemini_api_key_here
     ```
7. Deploy the app

## 📝 Usage

1. Upload your resume in PDF format
2. Paste the job description in the text area
3. Click "Analyze Resume"
4. View the analysis results
5. Download the PDF report if desired

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.