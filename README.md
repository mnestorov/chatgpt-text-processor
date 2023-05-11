# 🤖 ChatGPT Text Processor

[![Licence](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](./LICENSE)

## Support The Project

Your support is greatly appreciated and will help ensure the project's continued development and improvement. Thank you for being a part of the community!

[![BuyMeACoffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://bmc.link/mnestorov)

## Overview

This script allows you to **process and manipulate text of any size using OpenAI's GPT models** without having to use the ChatGPT website. With various options and modes, you can generate output based on the input text, create summaries, process text in an interactive mode, and estimate the number of tokens and API calls for a given input. You can use this script to **access the power of ChatGPT directly on your local machine** or server.

The script is designed to **handle input text of any size**, automatically splitting it into chunks that adhere to the model's token limits. This means you **no longer need to manually copy and paste text into the ChatGPT website**, making it **easier to work with large documents** and automate text processing tasks.

## Features

- Text processing with **OpenAI's GPT models** without the need for the ChatGPT website
- Handle **input text of any size**, automatically splitting it into manageable chunks
- Summary generation
- Interactive mode for direct input and output
- Batch processing of multiple input files
- Language support with easily configurable language models
- Dry run mode to estimate tokens and API calls
- Customizable colors for print messages
- Configuration file support

## Requirements

- Python 3.6 or higher
- openai package
- tiktoken package (optional, for accurate token counting)
- An [OpenAI API key](https://platform.openai.com/account/api-keys)

## Important

1. Make sure Python is installed on your system. You can download and install the latest version from the official Python website: https://www.python.org/downloads/

2. Check if Python is added to your system's PATH:

    - #### **For Windows:**

        - Open the Start menu, search for "Environment Variables," and click on "Edit the system environment variables."
        - Click on "Environment Variables" in the System Properties window.
        - In the "System variables" section, look for the "Path" variable, select it, and click "Edit."
        - Make sure that the Python installation path (e.g., `C:\Python39\` or `C:\Users\YourUsername\AppData\Local\Programs\Python\Python39\`) and the Scripts path (e.g., `C:\Python39\Scripts\` or `C:\Users\YourUsername\AppData\Local\Programs\Python\Python39\Scripts\`) are both added to the Path variable.
        - If they're not, add them manually by clicking "New" and entering the paths.
        - Click "OK" to save the changes and close the windows.

    - #### **For macOS/Linux:**

        - Open a terminal and run the following command:

            ```
            echo $PATH
            ```
        - Check if the Python installation path is present in the output.
        - If it's not, you can add the Python installation path to the PATH variable by adding the following line to your shell configuration file (e.g., `~/.bashrc`, `~/.bash_profile`, or `~/.zshrc`):

            ```
            export PATH="/path/to/your/python/installation:$PATH"
            ```
        - Replace `/path/to/your/python/installation` with the actual path to your Python installation.
        - Save the file and restart your terminal or run source ~/.bashrc, source `~/.bash_profile`, or `source ~/.zshrc` to apply the changes.

3. If Python is installed and added to your system's PATH but you still get the error, try using the python3 command instead of python:

```
python3 main.py
```

Open a terminal and run the following command:

## Installation

1. Clone this repository or download the source code.

2. Install the required packages

**You can install the required Python packages using this commands:**

```
pip install openai
pip install tiktoken
```

3. Add your **OpenAI API key** and configure language models and colors in the `config.ini` file.

## Usage

**The script can be run using the following command:**

```
python3 main.py [options]
```

### Command Options

- `-i, --input`: Input file or directory (required)
- `-o, --output`: Output file or directory (required)
- `-t, --tokens`: Tokens per chunk (default: 1500)
- `-l, --language`: Language of the input text (default: en)
- `-n, --dry-run`: Perform a dry run without making actual API requests
- `-m, --interactive`: Interactive mode
- `-s, --summary`: Generate summaries
- `-p, --temperature`: Sampling temperature (default: 0.5)

## Examples

**Process a single input file and save the output to a specified file:**

```
python3 main.py -i input.txt -o output.txt
```

**Generate summaries of the input text:**

```
python3 main.py -i input.txt -o summary.txt -s
```

**Use interactive mode:**

```
python3 main.py -m
```

**Perform a dry run to estimate tokens and API calls:**

```
python3 main.py -i input.txt -n
```

**Process a directory of input files:**

```
python3 main.py -i input_directory -o output_directory
```

## Customization

You can add more language models and change the colors for print messages by updating the `config.ini` file. Refer to the **[OpenAI documentation](https://platform.openai.com/docs/models)** for a list of available models and their capabilities.

## TODOs

- **_Error handling_**: Improve error handling and provide more informative error messages to the user.
- **_API key management_**: Implement more secure methods for storing and managing the OpenAI API key.
- **_Performance optimization_**: Optimize the script for better performance and faster processing, especially for large input files.
- **_Pre-trained models_**: Allow users to download and use pre-trained models locally, reducing the reliance on the OpenAI API and potentially reducing costs.
- **_User interface_**: Create a user-friendly graphical user interface (GUI) to make the script more accessible to non-technical users.
- **_Additional language support_**: Add support for more languages by including the appropriate OpenAI models and extending the script's functionality.
- **_Documentation_**: Improve and extend the documentation, providing more examples, detailed explanations, and troubleshooting tips.

## Contributing

Feel free to fork this repository and create pull requests for any new features, improvements, or bug fixes. You can also open issues for any questions, suggestions, or problems you encounter while using the script.

## Support The Project

If you find this script helpful and would like to support its development and maintenance, please consider the following options:

- **_Star the repository_**: If you're using this script from a GitHub repository, please give the project a star on GitHub. This helps others discover the project and shows your appreciation for the work done.

- **_Share your feedback_**: Your feedback, suggestions, and feature requests are invaluable to the project's growth. Please open issues on the GitHub repository or contact the author directly to provide your input.

- **_Contribute_**: You can contribute to the project by submitting pull requests with bug fixes, improvements, or new features. Make sure to follow the project's coding style and guidelines when making changes.

- **_Spread the word_**: Share the project with your friends, colleagues, and social media networks to help others benefit from the script as well.

- **_Donate_**: Show your appreciation with a small donation. Your support will help me maintain and enhance the script. Every little bit helps, and your donation will make a big difference in my ability to keep this project alive and thriving.

[![BuyMeACoffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://bmc.link/mnestorov)

Your support is greatly appreciated and will help ensure the project's continued development and improvement. Thank you for being a part of the community!

## License

This project is released under the MIT License.