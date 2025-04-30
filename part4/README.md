# Simple Web Client - Part 4

This project is the front-end portion of a larger web application. It focuses on creating a modern, user-friendly interface using HTML5, CSS3, and JavaScript ES6 that connects with a back-end API. The application includes features like user authentication, browsing a list of places, viewing place details, and submitting reviews.

## 🧾 Project Overview

This client-side application allows users to:
- Log in securely
- Browse a list of travel places
- View detailed information about a selected place
- Submit reviews (only when authenticated)

The front-end communicates with a RESTful API built in previous parts of the project using the Fetch API for asynchronous data interaction.

## 🛠️ Technologies Used

- HTML5
- CSS3
- JavaScript ES6 (Vanilla)
- Fetch API (AJAX)
- JWT (for session management)

## 🎯 Objectives

- Develop a responsive and accessible user interface
- Implement client-side logic for authentication and data display
- Securely handle user sessions with JWT
- Enable dynamic updates without full page reloads

## 📚 Learning Goals

- Apply front-end web development best practices
- Use JavaScript for DOM manipulation and HTTP requests
- Implement session handling and route guarding on the client side
- Enhance user experience through dynamic rendering

## 📋 Features & Task Breakdown

### ✅ Design (Task 1)
- Use provided HTML/CSS base
- Pages: Login, List of Places, Place Details, Add Review

### 🔐 Login (Task 2)
- Authenticate using the back-end API
- Store JWT in cookie for session persistence

### 🌍 List of Places (Task 3)
- Fetch and display places from API
- Filter places by country
- Redirect unauthenticated users to login page

### 📌 Place Details (Task 4)
- Fetch place information by ID
- Show review form for authenticated users

### 📝 Add Review (Task 5)
- Submit reviews using the API
- Only accessible to logged-in users

## 🚀 Getting Started

### Prerequisites
Make sure your back-end API is up and running (from previous parts of the project).

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/part4.git
   cd part4
   ```
2. Open index.html in your browser or use a local development server (e.g., Live Server extension in VS Code).

Configuration
You may need to set the API base URL in your JavaScript files if it's not hardcoded.

### 🧪 Testing
You can manually test functionality by:

Logging in with valid credentials

Viewing and filtering places

Adding a review after login

### 📌 Notes
Ensure proper CORS configuration on the back-end

Use secure HTTPS if deploying publicly

JWT handling is done client-side with basic cookie storage; consider HttpOnly cookies for production