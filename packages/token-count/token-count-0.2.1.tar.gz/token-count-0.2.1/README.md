# Token Count

Token Count is a command-line utility that counts the number of tokens in a text string, file, or directory, similar to the Unix `wc` utility. It uses the OpenAI `tiktoken` library for tokenization and is compatible with GPT-3.5-turbo or any other OpenAI model token counts.

## Installation

To install Token Count, run the following command in your terminal:

```bash
pip install token-count
```

## Usage - Python Library

```python
from token_count import TokenCount
tc = TokenCount(model_name="gpt-3.5-turbo")
text = "Your text here"
tokens = tc.num_tokens_from_string(text)
print(f"Tokens in the string: {tokens}")

file_path = "path/to/your/file.txt"
tokens = tc.num_tokens_from_file(file_path)
print(f"Tokens in the file: {tokens}")

dir_path = "path/to/your/directory"
tokens = tc.num_tokens_from_directory(dir_path)
print(f"Tokens in the directory: {tokens}")
```

## Usage - Command Line

Token Count has three main options:

Count tokens in a text string:
```bash
token-count --text "Your text here"
```
Count tokens in a file:
```bash
token-count --file path/to/your/file.txt
```

Count tokens in a directory (recursively):
```bash
token-count --directory path/to/your/directory
```
You can provide any combination of these options. Token Count will print the token count for each input type.

Additionally, you can provide any OpenAI model(gpt-4) to get token count according to the model. By default it uses "gpt-3.5-turbo".
```bash
token-count --model_name "gpt-4"
```

## License

This project is licensed under the MIT License.