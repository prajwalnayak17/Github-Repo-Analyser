# Welcome to GitHub Repo Analyser 👋

![Version](https://img.shields.io/badge/version-1.0-blue.svg?cacheSeconds=2592000)

**Analyse your GitHub Repos with the power of LLMs**

## Overview

GitHub Repository Analyzer is a powerful web application designed to analyze GitHub repositories for code quality and best practices. Built using Django for the backend and React with Tailwind CSS for the frontend, this application provides detailed insights and feedback on repositories, including code structure, file organization, and adherence to best practices.

## Features

- **Repository Analysis**: Analyze GitHub repositories to check for best practices and code quality.
- **Interactive UI**: Browse and view repository files with an interactive GitHub-like interface.
- **Code Review**: Fetch and display code suggestions and improvements.
- **Performance Metrics**: Display repository performance metrics such as feedback score and last commit hash.

## Tech Stack

- **Frontend**:
  - **React**: JavaScript library for building user interfaces.
  - **Tailwind CSS**: Utility-first CSS framework for styling.
  - **Font Awesome**: Icon library for using SVG icons.
- **Backend**:
  - **Django**: High-level Python web framework.
  - **Django REST Framework**: Toolkit for building Web APIs.

## Installation

### Backend

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/yourusername/github-repo-analyzer.git
   cd github-repo-analyzer
   ```

2. **Navigate to Backend Directory**:
   ```sh
   cd backend
   ```

3. **Create a Virtual Environment**:
   ```sh
   python -m venv venv
   ```

4. **Activate the Virtual Environment**:
   - On Windows:
     ```sh
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```sh
     source venv/bin/activate
     ```

5. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

6. **Apply Migrations**:
   ```sh
   python manage.py migrate
   ```

7. **Run the Server**:
   ```sh
   python manage.py runserver
   ```

### Frontend

1. **Navigate to Frontend Directory**:
   ```sh
   cd ../frontend
   ```

2. **Install Dependencies**:
   ```sh
   npm install
   ```

3. **Start the Development Server**:
   ```sh
   npm start
   ```

## Usage

1. **Access the Application**:
   Open a web browser and go to `http://localhost:3000` to view the React frontend.

2. **Submit a Repository URL**:
   Enter the GitHub repository URL and optional context into the provided form and submit.

3. **View Analysis Results**:
   After submission, view the file structure and analysis results in the interactive UI.

## Run Tests

```sh
npm run test
```



## Show Your Support

Give a ⭐️ if this project helped you!

---

_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_

```
