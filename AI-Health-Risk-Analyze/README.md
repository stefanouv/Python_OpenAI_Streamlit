# AI Health Risk Analyzer

An interactive health information application built with Python and Streamlit. It uses the OpenAI API to generate structured information about a disease, including symptoms, risk level, statistics, prevention tips, recovery options, and medication details.

Developed as a learning project to practice Streamlit application development, API integration, JSON processing, and data visualization.

> **Note:** This application has not been validated with an active OpenAI API account. A valid API key and access to the configured model (`gpt-4o-mini`) are required. API usage may incur additional costs.

## Features

- Enter a disease name to request AI-generated information.
- Display symptoms and an estimated risk level.
- Display total cases, recovery rates, and mortality rates.
- Visualize recovery and mortality rates using a bar chart.
- Show prevention tips and recovery options.
- Display AI-generated medication information.

## Technologies

- Python
- Streamlit
- OpenAI API
- Pandas
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
pip install streamlit openai pandas
```

## Configuration

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
streamlit run AIHealthRiskAnalyze.py
```

## Disclaimer

This application is intended for educational purposes only and is not a medical diagnostic tool. AI-generated medical information, statistics, recovery rates, and medication details may be inaccurate or incomplete and have not been independently verified. Do not use this application to make medical decisions or replace advice from a qualified healthcare professional.