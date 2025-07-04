# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-07

### Added
- Initial release of tamil-tokenizer library
- Basic Tamil text tokenization functionality:
  - Word tokenization using Unicode Tamil character ranges
  - Sentence tokenization with Tamil punctuation support
  - Character tokenization for individual Tamil characters
- Text processing utilities:
  - Text cleaning with whitespace normalization
  - Punctuation removal options
  - Text normalization
- TamilTokenizer class with comprehensive API:
  - Object-oriented interface for all tokenization methods
  - Text statistics generation
  - Error handling with custom exceptions
- Convenience functions for quick tokenization:
  - `tokenize_words()` - Word-level tokenization
  - `tokenize_sentences()` - Sentence-level tokenization
  - `tokenize_characters()` - Character-level tokenization
  - `clean_text()` - Text cleaning utility
  - `normalize_text()` - Text normalization utility
- Command-line interface (CLI):
  - Support for all tokenization methods
  - Text statistics display
  - Text cleaning operations
  - JSON output format
  - Verbose output options
- Comprehensive test suite:
  - Unit tests for all functionality
  - Error handling tests
  - Edge case coverage
- Modern Python packaging:
  - pyproject.toml configuration
  - Type hints throughout codebase
  - Python 3.8+ support
- Documentation:
  - Comprehensive README with examples
  - API reference documentation
  - CLI usage examples
  - Development setup instructions
- Development tools configuration:
  - Black code formatting
  - MyPy type checking
  - Pytest testing framework
  - Coverage reporting

### Technical Details
- Uses regex library for efficient Tamil text processing
- Tamil Unicode range support (U+0B80–U+0BFF)
- Comprehensive error handling with custom exception classes
- Type-safe implementation with full type annotations
- Modern Python project structure following best practices

### Dependencies
- Python >= 3.8
- regex >= 2022.0.0

### Development Dependencies
- pytest >= 7.0.0
- pytest-cov >= 4.0.0
- black >= 22.0.0
- flake8 >= 5.0.0
- mypy >= 1.0.0
