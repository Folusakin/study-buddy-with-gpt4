# Study Buddy with GPT-4

Study Buddy with GPT-4 is a tool designed to assist in studying books by providing explanations of excerpts using OpenAI's GPT-4 model. Simply highlight an excerpt from your book, activate the tool, and receive a clear and concise explanation in response.

## Features

- **Hotkey Activation**: Use `Ctrl+C+G` to activate the app, which copies the currently highlighted text and sends it to GPT-4.
- **Real-time Responses**: Displays streaming responses from GPT-4 in a dedicated window.

## Prerequisites

- Python 3.8+
- `openai`, `customtkinter`, `pyperclip`, `keyboard` Python libraries.

## Installation

Clone the repository and install the required packages:

```bash
git clone https://github.com/Folusakin/study-buddy-with-gpt4.git
cd study-buddy-with-gpt4
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python app.py
```

Press Ctrl+C+G after highlighting an excerpt from your book to see GPT-4's explanation in the GUI.

## Configuration

Modify `configure.py` to change the GPT model prompt settings as needed.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
