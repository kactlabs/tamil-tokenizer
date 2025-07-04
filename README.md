# tamil-tokenizer

A simple and efficient Tamil text tokenizer library with modern Python structure.

[![Python Support](https://img.shields.io/pypi/pyversions/tamil-tokenizer.svg)](https://pypi.org/project/tamil-tokenizer/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Features

- **Tamil Text Tokenization**: Comprehensive tokenization for Tamil text
- **Multiple Tokenization Methods**: Word, sentence, and character-level tokenization
- **Text Cleaning**: Remove extra whitespace and punctuation
- **Text Normalization**: Standardize Tamil text format
- **Modern Python API**: Clean, type-hinted interface with both functional and object-oriented approaches
- **Command Line Interface**: Full-featured CLI tool for Tamil text processing
- **Fast Processing**: Efficient regex-based operations
- **Error Handling**: Comprehensive exception handling with meaningful error messages
- **Well Tested**: Extensive test suite with high coverage
- **Type Hints**: Full type annotation support for better IDE experience

## Installation

```bash
pip install tamil-tokenizer
```

### Dependencies

- Python 3.8+
- regex >= 2022.0.0

### Optional Dependencies

For development:
```bash
pip install tamil-tokenizer[dev]
```

## Quick Start

```python
from tamil_tokenizer import tokenize_words, tokenize_sentences, TamilTokenizer

# Quick tokenization
words = tokenize_words("தமிழ் மொழி அழகான மொழி")
print(f"Words: {words}")

sentences = tokenize_sentences("வணக்கம். நீங்கள் எப்படி இருக்கிறீர்கள்?")
print(f"Sentences: {sentences}")

# Using TamilTokenizer class
tokenizer = TamilTokenizer()
tokens = tokenizer.tokenize("தமிழ் உரை", method="words")
print(f"Tokens: {tokens}")
```

## Usage Examples

### Basic Tokenization

```python
from tamil_tokenizer import tokenize_words, tokenize_sentences, tokenize_characters

# Word tokenization
text = "தமிழ் மொழி அழகான மொழி"
words = tokenize_words(text)
print(f"Words: {words}")
# Output: ['தமிழ்', 'மொழி', 'அழகான', 'மொழி']

# Sentence tokenization
text = "வணக்கம். நீங்கள் எப்படி இருக்கிறீர்கள்? நன்றாக இருக்கிறேன்!"
sentences = tokenize_sentences(text)
print(f"Sentences: {sentences}")
# Output: ['வணக்கம்', 'நீங்கள் எப்படி இருக்கிறீர்கள்', 'நன்றாக இருக்கிறேன்']

# Character tokenization
text = "தமிழ்"
characters = tokenize_characters(text)
print(f"Characters: {characters}")
# Output: ['த', 'ம', 'ி', 'ழ', '்']
```

### Using TamilTokenizer Class

```python
from tamil_tokenizer import TamilTokenizer

# Create tokenizer instance
tokenizer = TamilTokenizer()

# General tokenization method
text = "தமிழ் மொழி அழகான மொழி"
words = tokenizer.tokenize(text, method="words")
sentences = tokenizer.tokenize(text, method="sentences")
characters = tokenizer.tokenize(text, method="characters")

print(f"Words: {words}")
print(f"Sentences: {sentences}")
print(f"Characters: {characters}")
```

### Text Cleaning and Normalization

```python
from tamil_tokenizer import clean_text, normalize_text, TamilTokenizer

# Clean text with extra whitespace
messy_text = "  தமிழ்   மொழி   அழகு  "
cleaned = clean_text(messy_text)
print(f"Cleaned: '{cleaned}'")
# Output: 'தமிழ் மொழி அழகு'

# Clean text and remove punctuation
tokenizer = TamilTokenizer()
text_with_punct = "தமிழ், மொழி! அழகு?"
cleaned_no_punct = tokenizer.clean_text(text_with_punct, remove_punctuation=True)
print(f"No punctuation: '{cleaned_no_punct}'")
# Output: 'தமிழ் மொழி அழகு'

# Normalize text
normalized = normalize_text(messy_text)
print(f"Normalized: '{normalized}'")
# Output: 'தமிழ் மொழி அழகு'
```

### Text Statistics

```python
from tamil_tokenizer import TamilTokenizer

tokenizer = TamilTokenizer()
text = "தமிழ் மொழி அழகான மொழி. இது உலகின் பழமையான மொழிகளில் ஒன்று!"

stats = tokenizer.get_statistics(text)
print(f"Total characters: {stats['total_characters']}")
print(f"Tamil characters: {stats['tamil_characters']}")
print(f"Words: {stats['words']}")
print(f"Sentences: {stats['sentences']}")
print(f"Average word length: {stats['average_word_length']:.2f}")
print(f"Average sentence length: {stats['average_sentence_length']:.2f}")
```

### Error Handling

```python
from tamil_tokenizer import tokenize_words
from tamil_tokenizer.exceptions import InvalidTextError, TokenizationError

try:
    words = tokenize_words("")  # Empty text
except InvalidTextError as e:
    print(f"Invalid text: {e}")

try:
    words = tokenize_words(None)  # None text
except InvalidTextError as e:
    print(f"Invalid text: {e}")
```

## Command Line Interface

The library includes a comprehensive CLI tool:

```bash
# Basic word tokenization (default)
tamil-tokenizer "தமிழ் மொழி அழகான மொழி"

# Sentence tokenization
tamil-tokenizer --method sentences "வணக்கம். நலமா?"

# Character tokenization
tamil-tokenizer --method characters "தமிழ்"

# Show text statistics
tamil-tokenizer --stats "தமிழ் உரை"

# Clean text
tamil-tokenizer --clean "தமிழ்   உரை"

# Clean text and remove punctuation
tamil-tokenizer --clean --remove-punctuation "தமிழ், உரை!"

# JSON output
tamil-tokenizer --json "தமிழ் மொழி"

# Verbose output
tamil-tokenizer --verbose "தமிழ் மொழி"
```

### CLI Examples

```bash
# Basic tokenization
$ tamil-tokenizer "தமிழ் மொழி அழகான மொழி"
தமிழ்
மொழி
அழகான
மொழி

# Sentence tokenization with verbose output
$ tamil-tokenizer --method sentences --verbose "வணக்கம். நலமா?"
Tokenization method: sentences
Input text: வணக்கம். நலமா?
Token count: 2
Tokens:
--------------------
  1. வணக்கம்
  2. நலமா

# Text statistics
$ tamil-tokenizer --stats "தமிழ் மொழி"
Total characters: 9
Tamil characters: 8
Words: 2
Sentences: 1
Average word length: 4.00
Average sentence length: 2.00

# JSON output
$ tamil-tokenizer --json "தமிழ் மொழி"
{
  "method": "words",
  "input_text": "தமிழ் மொழி",
  "tokens": ["தமிழ்", "மொழி"],
  "token_count": 2
}
```

## API Reference

### Functions

#### `tokenize_words(text: str) -> List[str]`
Tokenize Tamil text into words.

**Parameters:**
- `text`: Tamil text to tokenize

**Returns:** List of word tokens

#### `tokenize_sentences(text: str) -> List[str]`
Tokenize Tamil text into sentences.

**Parameters:**
- `text`: Tamil text to tokenize

**Returns:** List of sentence tokens

#### `tokenize_characters(text: str) -> List[str]`
Tokenize Tamil text into individual characters.

**Parameters:**
- `text`: Tamil text to tokenize

**Returns:** List of character tokens (Tamil characters only)

#### `clean_text(text: str, remove_punctuation: bool = False) -> str`
Clean Tamil text by normalizing whitespace and optionally removing punctuation.

**Parameters:**
- `text`: Text to clean
- `remove_punctuation`: Whether to remove non-Tamil punctuation

**Returns:** Cleaned text

#### `normalize_text(text: str) -> str`
Normalize Tamil text by cleaning and standardizing format.

**Parameters:**
- `text`: Text to normalize

**Returns:** Normalized text

### Classes

#### `TamilTokenizer()`
Main class for Tamil text tokenization operations.

**Methods:**
- `tokenize(text, method="words")`: General tokenization method
- `tokenize_words(text)`: Tokenize into words
- `tokenize_sentences(text)`: Tokenize into sentences
- `tokenize_characters(text)`: Tokenize into characters
- `clean_text(text, remove_punctuation=False)`: Clean text
- `normalize_text(text)`: Normalize text
- `get_statistics(text)`: Get text statistics

### Exceptions

#### `TamilTokenizerError`
Base exception class for tamil-tokenizer library.

#### `InvalidTextError`
Raised when invalid text is provided (None, empty, or non-string).

#### `TokenizationError`
Raised when tokenization fails due to processing errors.

## Development

### Setup Development Environment

```bash
git clone https://github.com/rajacsp/tamil-tokenizer.git
cd tamil-tokenizer
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov=tamil_tokenizer --cov-report=html
```

### Code Formatting

```bash
black tamil_tokenizer tests examples
```

### Type Checking

```bash
mypy tamil_tokenizer
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Changelog

### v0.1.0
- **Initial release**
- Basic Tamil text tokenization (words, sentences, characters)
- Text cleaning and normalization
- Command-line interface
- Comprehensive test suite
- Type hints throughout the codebase
- Modern Python packaging with pyproject.toml

## Tamil Language Support

This library is specifically designed for Tamil text processing and uses Unicode ranges for Tamil script (U+0B80–U+0BFF). It handles:

- Tamil characters and diacritics
- Common Tamil punctuation
- Mixed Tamil-English text (extracts Tamil portions)
- Various sentence ending patterns

## Acknowledgments

- The Tamil language community for inspiration
- The Python community for excellent libraries like regex
- Contributors and users who help improve this library

## Support

If you encounter any issues or have questions, please:

1. Check the [documentation](https://github.com/rajacsp/tamil-tokenizer)
2. Search existing [issues](https://github.com/rajacsp/tamil-tokenizer/issues)
3. Create a new issue if needed

For general questions, you can also reach out via email: raja.csp@gmail.com
