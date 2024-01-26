
# Vendor Management System

## Introduction

The Vendor Management System is a web application designed to manage vendor information effectively. It allows users to add, edit, and delete vendor details. This application uses Flask as its backend framework and integrates Google OAuth 2.0 for user authentication.

## Features

- User authentication with Google OAuth 2.0.
- CRUD operations: Create, Read, Update, Delete vendor details.
- Confirmation prompts before deleting vendor information.
- Responsive design, ensuring accessibility on various devices.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6+
- Flask
- A Google Cloud Platform account with OAuth 2.0 set up.

## Installation and Setup

1. **Set up Google OAuth 2.0:**

    - Create a project in the Google Developers Console.
    - Enable the OAuth API.
    - Configure the consent screen.
    - Create credentials (Client ID and Client Secret).
    - Set the Authorized redirect URIs to match your application's redirect path.

2. **Configure your application with your Google credentials and database URI in `config.py`:**

    ```python
    GOOGLE_CLIENT_ID = "your-google-client-id"
    GOOGLE_CLIENT_SECRET = "your-google-client-secret"
    ```

## Running the Application

1. **Start the Flask server:**

    ```Windows
    python run main.py
    ```

2. **Access the application through your web browser:**

    ```
    http://localhost:8501
    ```



## Contact

Your Name - [Soumya Choudhury](mailto:soumyaneel104@gmail.com)

