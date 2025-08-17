

# 🤖 WARL (like WARP but worse.. but local)

**A powerful, interactive CLI assistant that leverages local LLMs via Ollama to generate and execute shell commands or just have a chat.**


-----

## 🌟 Overview

LCAI brings the power of large language models directly to your terminal, without sending your data to the cloud. It operates in two distinct modes:

  * **💻 Command Mode**: Describe what you want to do, and LCAI will suggest the perfect shell command. You can then approve and execute it directly.
  * **💬 Chat Mode**: A general-purpose, conversational AI assistant that remembers your conversation history and provides helpful answers, right in your terminal.

The interface is built with `rich` for a beautiful and user-friendly experience.

## ✨ Features

  * **🧠 Dual Modes**: Seamlessly switch between a command generator and a chat assistant.
  * **🔒 Privacy-Focused**: Runs entirely locally using [Ollama](https://ollama.com/). Your queries and data never leave your machine.
  * **🚀 Interactive Workflow**: Suggests commands and waits for your confirmation before execution.
  * **🎨 Rich Terminal UI**: Beautifully formatted panels, prompts, and status indicators powered by the `rich` library.
  * **📝 Conversation History**: The assistant remembers the context of your current session for more relevant follow-up interactions.
  * **🔧 Customizable**: Easily change the Ollama model by modifying a single variable in the script.
  * **✅ Robust Error Handling**: Clear feedback for command execution errors or issues connecting to Ollama.

## 🎬 Demo


**Command Mode Interaction:**

**Chat Mode Interaction:**

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:

1.  **Python 3.8+**
2.  **Ollama**: Follow the installation guide at [ollama.com](https://ollama.com/).
3.  **An Ollama Model**: You need to have a model pulled locally. The script defaults to `qwen2.5-coder:3b`, which is excellent for code and command generation. You can pull it with:
    ```sh
    ollama pull qwen2.5-coder:3b
    ```

## 🚀 Installation & Setup

1.  **Clone the repository:**

    ```sh
    git clone https://https://github.com/steamed-p0tato/WARL/
    cd WARL
    ```

2.  **Create a virtual environment (recommended):**

    ```sh
    python3 -m venv venv
    source venv/bin/activate
    # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required Python packages:**
    Create a `requirements.txt` file with the following content:

    ```txt
    ollama
    rich
    ```

    Then run:

    ```sh
    pip install -r requirements.txt
    ```

## ▶️ How to Run

1.  **Make sure the Ollama application is running in the background.**

2.  **Execute the Python script:**

    ```sh
    python3 lcai.py
    ```

    *(Assuming you've renamed the provided script to `lcai.py`)*

### In-App Commands

  * The application starts in **Command Mode** by default.
  * Type `/chat` to switch to Chat Mode.
  * Type `/command` to switch back to Command Mode.
  * Type `exit` or `quit` (or press `Ctrl+C`) to end the session.

## ⚙️ Configuration

To use a different Ollama model, simply change the `OLLAMA_MODEL` constant at the top of the script:

```python
# Change this to any model you have pulled with Ollama
OLLAMA_MODEL = 'llama3:8b'
```

## 🤝 Contributing

Contributions are welcome\! If you have suggestions for improvements or find a bug, please feel free to:

1.  Fork the repository.
2.  Create a new feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

-----

\<div align="center"\>
Made with ❤️ and Python
\</div\>
