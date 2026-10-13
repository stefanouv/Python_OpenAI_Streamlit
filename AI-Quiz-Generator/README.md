# AI Quiz Generator

An interactive quiz application built with Python and Streamlit. It allows users to answer multiple-choice questions, track their scores, and generate additional questions on selected topics using the OpenAI API.

Developed as a learning project to practice object-oriented programming, Streamlit session state, interactive user interfaces, JSON processing, and API integration.

> **Note:** The AI question generation feature has not been tested with an active OpenAI API account. A valid API key and access to the configured model (`gpt-3.5-turbo`) are required. API usage may incur additional costs.

## Features

- Answer multiple-choice questions.
- Track scores and success rates.
- View quiz progress through the sidebar.
- Receive feedback and explanations after submitting answers.
- Restart the quiz and try again.
- Generate additional questions based on a user-provided topic using AI.

## Technologies

- Python
- Streamlit
- OpenAI API
- JSON

## Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

Install the required dependencies:

```bash
pip install streamlit openai
```

## Configuration

The AI question generation feature requires an OpenAI API key with access to the model configured in the application.

Set the `OPENAI_API_KEY` environment variable before running the application.

**Windows PowerShell:**

```powershell
$env:OPENAI_API_KEY="your-api-key"
```

**macOS / Linux:**

```bash
export OPENAI_API_KEY="your-api-key"
```

Without a configured API key, the application stops during initialization.

## Run the Application

```bash
streamlit run AIQuizGenerator.py
```

## Disclaimer

This project was developed for educational purposes. AI-generated questions, answers, and explanations may contain errors and should be reviewed for accuracy.