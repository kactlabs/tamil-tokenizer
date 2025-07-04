"""
Core functionality for Tamil text tokenization and processing.
"""

import re
from typing import List, Optional, Union

from .exceptions import InvalidTextError, TokenizationError


class TamilTokenizer:
    """
    A class for Tamil text tokenization and processing.
    
    Provides functionality to tokenize Tamil text including:
    - Word tokenization
    - Sentence tokenization
    - Character tokenization
    - Text cleaning and normalization
    """
    
    def __init__(self):
        """Initialize the Tamil tokenizer."""
        # Tamil Unicode range: U+0B80–U+0BFF
        self.tamil_pattern = re.compile(r'[\u0B80-\u0BFF]+')
        
        # Common Tamil punctuation and sentence endings
        self.sentence_endings = r'[.!?।॥]'
        
        # Word boundary patterns for Tamil - match individual Tamil words
        self.word_pattern = re.compile(r'[\u0B80-\u0BFF]+')
        
        # Whitespace and punctuation patterns
        self.whitespace_pattern = re.compile(r'\s+')
        self.punctuation_pattern = re.compile(r'[^\u0B80-\u0BFF\s]')
    
    def _validate_text(self, text: Union[str, None]) -> str:
        """
        Validate input text.
        
        Args:
            text: Input text to validate
            
        Returns:
            Validated text as string
            
        Raises:
            InvalidTextError: If text is invalid
        """
        if text is None:
            raise InvalidTextError("Text cannot be None")
        
        if not isinstance(text, str):
            raise InvalidTextError("Text must be a string")
        
        if not text.strip():
            raise InvalidTextError("Text cannot be empty or only whitespace")
        
        return text.strip()
    
    def tokenize_words(self, text: str) -> List[str]:
        """
        Tokenize Tamil text into words.
        
        Args:
            text: Tamil text to tokenize
            
        Returns:
            List of word tokens
            
        Raises:
            InvalidTextError: If text is invalid
            TokenizationError: If tokenization fails
        """
        try:
            validated_text = self._validate_text(text)
            
            # Find all Tamil word sequences
            words = self.word_pattern.findall(validated_text)
            
            # Clean up words by removing extra whitespace
            cleaned_words = []
            for word in words:
                cleaned_word = re.sub(r'\s+', ' ', word.strip())
                if cleaned_word:
                    cleaned_words.append(cleaned_word)
            
            return cleaned_words
            
        except Exception as e:
            if isinstance(e, (InvalidTextError, TokenizationError)):
                raise
            raise TokenizationError(f"Failed to tokenize words: {str(e)}")
    
    def tokenize_sentences(self, text: str) -> List[str]:
        """
        Tokenize Tamil text into sentences.
        
        Args:
            text: Tamil text to tokenize
            
        Returns:
            List of sentence tokens
            
        Raises:
            InvalidTextError: If text is invalid
            TokenizationError: If tokenization fails
        """
        try:
            validated_text = self._validate_text(text)
            
            # Split by sentence endings
            sentences = re.split(self.sentence_endings, validated_text)
            
            # Clean up sentences
            cleaned_sentences = []
            for sentence in sentences:
                cleaned_sentence = sentence.strip()
                if cleaned_sentence:
                    cleaned_sentences.append(cleaned_sentence)
            
            return cleaned_sentences
            
        except Exception as e:
            if isinstance(e, (InvalidTextError, TokenizationError)):
                raise
            raise TokenizationError(f"Failed to tokenize sentences: {str(e)}")
    
    def tokenize_characters(self, text: str) -> List[str]:
        """
        Tokenize Tamil text into individual characters.
        
        Args:
            text: Tamil text to tokenize
            
        Returns:
            List of character tokens (excluding whitespace)
            
        Raises:
            InvalidTextError: If text is invalid
            TokenizationError: If tokenization fails
        """
        try:
            validated_text = self._validate_text(text)
            
            # Extract Tamil characters only
            characters = []
            for char in validated_text:
                if self.tamil_pattern.match(char):
                    characters.append(char)
            
            return characters
            
        except Exception as e:
            if isinstance(e, (InvalidTextError, TokenizationError)):
                raise
            raise TokenizationError(f"Failed to tokenize characters: {str(e)}")
    
    def clean_text(self, text: str, remove_punctuation: bool = False) -> str:
        """
        Clean Tamil text by normalizing whitespace and optionally removing punctuation.
        
        Args:
            text: Text to clean
            remove_punctuation: Whether to remove non-Tamil punctuation
            
        Returns:
            Cleaned text
            
        Raises:
            InvalidTextError: If text is invalid
        """
        try:
            validated_text = self._validate_text(text)
            
            # Normalize whitespace
            cleaned_text = self.whitespace_pattern.sub(' ', validated_text)
            
            # Remove punctuation if requested
            if remove_punctuation:
                cleaned_text = self.punctuation_pattern.sub('', cleaned_text)
            
            return cleaned_text.strip()
            
        except Exception as e:
            if isinstance(e, InvalidTextError):
                raise
            raise TokenizationError(f"Failed to clean text: {str(e)}")
    
    def normalize_text(self, text: str) -> str:
        """
        Normalize Tamil text by cleaning and standardizing format.
        
        Args:
            text: Text to normalize
            
        Returns:
            Normalized text
            
        Raises:
            InvalidTextError: If text is invalid
        """
        try:
            # Clean the text first
            cleaned_text = self.clean_text(text)
            
            # Additional normalization can be added here
            # For now, just return cleaned text
            return cleaned_text
            
        except Exception as e:
            if isinstance(e, InvalidTextError):
                raise
            raise TokenizationError(f"Failed to normalize text: {str(e)}")
    
    def tokenize(self, text: str, method: str = "words") -> List[str]:
        """
        General tokenization method.
        
        Args:
            text: Text to tokenize
            method: Tokenization method ("words", "sentences", "characters")
            
        Returns:
            List of tokens based on the specified method
            
        Raises:
            InvalidTextError: If text is invalid
            TokenizationError: If tokenization fails
        """
        method = method.lower()
        
        if method == "words":
            return self.tokenize_words(text)
        elif method == "sentences":
            return self.tokenize_sentences(text)
        elif method == "characters":
            return self.tokenize_characters(text)
        else:
            raise TokenizationError(f"Unknown tokenization method: {method}")
    
    def get_statistics(self, text: str) -> dict:
        """
        Get basic statistics about Tamil text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary containing text statistics
        """
        try:
            validated_text = self._validate_text(text)
            
            words = self.tokenize_words(validated_text)
            sentences = self.tokenize_sentences(validated_text)
            characters = self.tokenize_characters(validated_text)
            
            return {
                'total_characters': len(validated_text),
                'tamil_characters': len(characters),
                'words': len(words),
                'sentences': len(sentences),
                'average_word_length': sum(len(word) for word in words) / len(words) if words else 0,
                'average_sentence_length': len(words) / len(sentences) if sentences else 0,
            }
            
        except Exception as e:
            if isinstance(e, InvalidTextError):
                raise
            raise TokenizationError(f"Failed to get statistics: {str(e)}")


# Global instance for convenience functions
_default_tokenizer: Optional[TamilTokenizer] = None


def _get_default_tokenizer() -> TamilTokenizer:
    """Get or create the default TamilTokenizer instance."""
    global _default_tokenizer
    if _default_tokenizer is None:
        _default_tokenizer = TamilTokenizer()
    return _default_tokenizer


# Convenience functions
def tokenize_words(text: str) -> List[str]:
    """
    Convenience function to tokenize Tamil text into words.
    
    Args:
        text: Tamil text to tokenize
        
    Returns:
        List of word tokens
    """
    return _get_default_tokenizer().tokenize_words(text)


def tokenize_sentences(text: str) -> List[str]:
    """
    Convenience function to tokenize Tamil text into sentences.
    
    Args:
        text: Tamil text to tokenize
        
    Returns:
        List of sentence tokens
    """
    return _get_default_tokenizer().tokenize_sentences(text)


def tokenize_characters(text: str) -> List[str]:
    """
    Convenience function to tokenize Tamil text into characters.
    
    Args:
        text: Tamil text to tokenize
        
    Returns:
        List of character tokens
    """
    return _get_default_tokenizer().tokenize_characters(text)


def clean_text(text: str, remove_punctuation: bool = False) -> str:
    """
    Convenience function to clean Tamil text.
    
    Args:
        text: Text to clean
        remove_punctuation: Whether to remove punctuation
        
    Returns:
        Cleaned text
    """
    return _get_default_tokenizer().clean_text(text, remove_punctuation)


def normalize_text(text: str) -> str:
    """
    Convenience function to normalize Tamil text.
    
    Args:
        text: Text to normalize
        
    Returns:
        Normalized text
    """
    return _get_default_tokenizer().normalize_text(text)
