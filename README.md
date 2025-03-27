# MIMI - AI Parenting Assistant

MIMI is an intelligent, empathetic AI assistant designed to support parents with practical advice, emotional encouragement, and reliable information about child care, development, and parenting challenges.

## 🌟 Features

- 🤖 AI-powered parenting advice and support
- 💬 Natural conversation interface in Romanian
- 📱 Responsive web interface
- 💾 Persistent chat history
- 🔄 Memory reset capability
- 🔒 Secure and private conversations

## 🛠️ Tech Stack

### Backend
- FastAPI (Python web framework)
- SQLite database for chat history
- Ollama for AI model integration
- Transformers for language processing

### Frontend
- HTML5
- CSS3
- JavaScript (Vanilla)
- Responsive design

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js (for frontend development)
- Ollama installed locally

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   .\venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the backend server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Open `index.html` in your web browser or serve it using a local server.

## 💻 Usage

1. Open the application in your web browser
2. Type your parenting-related questions or concerns in the chat input
3. Receive personalized advice and support from MIMI
4. Use the "Reset Memory" button to start a fresh conversation

## 🔧 Configuration

The application uses environment variables for configuration. Create a `.env` file in the backend directory with the following variables:
```
OLLAMA_MODEL=your_model_name
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Ollama for providing the AI model infrastructure
- FastAPI for the robust backend framework
- All contributors and users of the application

## 📞 Support

For support, please open an issue in the GitHub repository or contact the maintainers.
