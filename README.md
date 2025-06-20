# PresentAI - AI Presentation Generator

A powerful AI-driven presentation tool built with LangGraph that transforms user prompts and supporting documents into complete presentations with slides, speaker notes, and scripts.

## 🚀 Features

- **AI-Powered Generation**: Uses LangGraph and Google Gemini to create compelling presentations
- **Document Processing**: Upload and analyze supporting documents (PDF, Word, Excel, Text)
- **Complete Presentation Package**: Generates HTML slides, detailed speaker notes, and presentation scripts
- **Modern Web Interface**: Beautiful, responsive demo webpage
- **Real-time Generation**: Watch your presentation come to life in real-time

## 🛠️ Technology Stack

- **Backend**: FastAPI, LangGraph, LangChain
- **AI**: Google Gemini 1.5 Flash
- **Frontend**: HTML, CSS, JavaScript
- **Document Processing**: PyPDF2, python-docx, openpyxl
- **Templates**: Jinja2
- **Package Management**: uv

## 📋 Prerequisites

- Python 3.11+
- Google API key (for Gemini access)
- uv package manager

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd PresentAI
   ```

2. **Install uv (if not already installed)**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   source $HOME/.local/bin/env
   ```

3. **Install dependencies**
   ```bash
   uv sync
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example and edit with your API key
   cp env_example.txt .env
   # Edit .env and add your Google API key:
   # GOOGLE_API_KEY=your-api-key-here
   ```

## 🔑 Getting a Google API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and add it to your `.env` file

## 🚀 Running the Application

1. **Test your setup**
   ```bash
   uv run python -m scripts.test_setup
   ```

2. **Start the server**
   ```bash
   uv run python -m src.main
   ```

3. **Open your browser**
   Navigate to `http://localhost:8000`

## 📖 How to Use

1. **Enter your presentation prompt**: Describe your topic, target audience, and key points
2. **Upload supporting documents** (optional): Add PDFs, Word docs, Excel files, or text files
3. **Generate presentation**: Click the generate button and wait 1-2 minutes
4. **View results**: Access your slides, speaker notes, and presentation script

## 🏗️ Project Structure

```
PresentAI/
├── src/
│   ├── main.py                    # FastAPI application
│   ├── presentation_agent.py      # LangGraph AI agent
│   └── templates/
│       ├── index.html            # Main demo page
│       └── presentation.html     # Presentation viewer
├── scripts/
│   └── test_setup.py             # Setup verification script
├── pyproject.toml                # uv project configuration
├── env_example.txt               # Environment variables example
└── README.md                     # This file
```

## 🧠 How It Works

The AI agent follows a structured workflow using LangGraph:

1. **Document Processing**: Extracts content from uploaded files
2. **Structure Creation**: Analyzes prompt and documents to create presentation outline
3. **Slide Generation**: Creates beautiful HTML slides with CSS and JavaScript
4. **Speaker Notes**: Generates detailed notes for each slide
5. **Script Writing**: Creates a complete presentation script

## 🔌 API Endpoints

- `GET /` - Main demo page
- `POST /generate-presentation` - Generate a new presentation
- `GET /presentation/{id}` - View presentation
- `GET /presentation/{id}/slides` - Get HTML slides
- `GET /presentation/{id}/notes` - Get speaker notes
- `GET /presentation/{id}/script` - Get presentation script
- `GET /health` - Health check

## 📝 Example Usage

### Basic Presentation
```
Prompt: "Create a 10-minute presentation about sustainable energy for a corporate executive audience. Focus on cost benefits, environmental impact, and implementation strategies."
```

### With Supporting Documents
Upload research papers, data sheets, or company reports to enhance the presentation content.

## 🎨 Customization

The AI agent can be customized by:

- Modifying prompts in `src/presentation_agent.py`
- Adjusting the LangGraph workflow
- Changing the HTML/CSS templates for slides
- Adding new document processing capabilities
- Switching to different Gemini models (gemini-1.5-pro, etc.)

## 🔒 Security Notes

- Store your Google API key securely in the `.env` file
- The demo stores presentations in memory (not persistent)
- For production use, implement proper data storage and user authentication
- Never commit your `.env` file to version control

## 🐛 Troubleshooting

### Common Issues

1. **"No Google API key found"**
   - Ensure your `.env` file contains `GOOGLE_API_KEY=your-key`
   - Verify the key is valid at [Google AI Studio](https://makersuite.google.com/)

2. **"Failed to generate presentation"**
   - Check your internet connection
   - Verify your Google API key is valid and has quota remaining
   - Try running the test script: `uv run python scripts/test_setup.py`

3. **Import errors**
   - Run `uv sync` to ensure all dependencies are installed
   - Make sure you're running from the correct directory

4. **Document processing errors**
   - Ensure uploaded files are not corrupted
   - Check file format compatibility
   - Try with smaller files first

## 🚀 Development

### Adding New Features

1. **Install development dependencies**
   ```bash
   uv add --dev pytest black flake8
   ```

2. **Run tests**
   ```bash
   uv run python scripts/test_setup.py
   ```

3. **Format code**
   ```bash
   uv run black src/ scripts/
   ```

### Project Commands

- `uv sync` - Install/update dependencies
- `uv add <package>` - Add a new dependency
- `uv run <command>` - Run a command in the virtual environment
- `uv pip list` - List installed packages

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Run the test script to verify functionality
6. Submit a pull request

## 📄 License

This project is open source. Please check the license file for details.

## 🙏 Acknowledgments

- Built with LangGraph and LangChain
- Powered by Google Gemini AI
- Package management by uv
- UI inspired by modern design principles

---

**Ready to transform your ideas into stunning presentations? Get started now!** 🎯 