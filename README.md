# LogosYandexART

A Flask-based web application for generating logos using Yandex ART API.

## Description
This project allows users to generate logos via a simple web interface. It uses the Yandex ART API to create images based on user input and displays them on the page. The application is built with Flask, a lightweight Python web framework.

## Features
- Generate logos using Yandex ART API.
- Simple web interface with Flask.
- Secure handling of API keys using environment variables.

## Installation
1. Clone the repository:
git clone https://github.com/TinaUma/LogosYandexART.git
cd LogosYandexART

2. Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
pip install -r requirements.txt

4. Create a `.env` file in the project root and add your Yandex ART API keys:
IAM_TOKEN=your_iam_token
CATALOG_ID=your_catalog_id

5. Run the application:
python app.py
6. Open your browser and go to `http://127.0.0.1:5000`.

## Usage
- Enter a description of the logo you want to generate in the web form.
- Click "Generate" to create a logo using Yandex ART API.
- The generated logo will be displayed on the page.

## Screenshots
![Generated Logo](screenshots/logo_generator.png)

## Requirements
- Python 3.8+
- Flask==2.0.1
- Requests==2.28.1
- Python-dotenv==1.0.0
