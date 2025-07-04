"""
Core functionality for Tamil text tokenization and processing.
"""

import re
import unicodedata
from typing import List, Optional, Union

from .exceptions import InvalidTextError, TokenizationError


class TamilTokenizer:
    """
    A class for Tamil text tokenization and processing.
    
    Provides functionality to tokenize Tamil text including:
    - Word tokenization with proper Tamil morphology handling
    - Sentence tokenization
    - Character tokenization with proper grapheme clustering
    - Text cleaning and normalization
    """
    
    def __init__(self):
        """Initialize the Tamil tokenizer."""
        # Tamil Unicode ranges
        # Main Tamil block: U+0B80–U+0BFF
        # Tamil Supplement: U+11FC0–U+11FFF (not commonly used)
        self.tamil_pattern = re.compile(r'[\u0B80-\u0BFF]+')
        
        # Tamil base consonants (க-ன், ப-ஹ)
        self.tamil_consonants = re.compile(r'[\u0B95-\u0BB9]')
        
        # Tamil vowels (அ-ஔ)
        self.tamil_vowels = re.compile(r'[\u0B85-\u0B94]')
        
        # Tamil vowel signs (ா-ௌ)
        self.tamil_vowel_signs = re.compile(r'[\u0BBE-\u0BCC]')
        
        # Tamil combining marks (், ௗ)
        self.tamil_combining = re.compile(r'[\u0BCD\u0BD7]')
        
        # Common Tamil punctuation and sentence endings
        self.sentence_endings = r'[.!?।॥]'
        
        # Enhanced word pattern that handles Tamil script properly
        # This matches sequences of Tamil characters including combining marks
        self.word_pattern = re.compile(r'[\u0B80-\u0BFF]+(?:[\u0BCD\u0BD7][\u0B80-\u0BFF]*)*')
        
        # Whitespace and punctuation patterns
        self.whitespace_pattern = re.compile(r'\s+')
        self.punctuation_pattern = re.compile(r'[^\u0B80-\u0BFF\s]')
        
        # Tamil grapheme cluster pattern for proper character tokenization
        # This handles complex Tamil characters with combining marks
        self.grapheme_pattern = re.compile(
            r'[\u0B85-\u0B94]|'  # Independent vowels
            r'[\u0B95-\u0BB9](?:[\u0BCD][\u0B95-\u0BB9])*[\u0BBE-\u0BCC\u0BD7]?|'  # Consonants with optional conjuncts and vowel signs
            r'[\u0B95-\u0BB9][\u0BCD](?![\u0B95-\u0BB9])|'  # Consonant with virama (not followed by another consonant)
            r'[\u0B80-\u0BFF]'  # Any other Tamil character
        )
    
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
        Tokenize Tamil text into individual Unicode characters.
        
        This method returns individual Tamil Unicode characters,
        including base characters, vowel signs, and combining marks separately.
        
        Args:
            text: Tamil text to tokenize
            
        Returns:
            List of individual Tamil Unicode characters (excluding whitespace)
            
        Raises:
            InvalidTextError: If text is invalid
            TokenizationError: If tokenization fails
        """
        try:
            validated_text = self._validate_text(text)
            
            # Extract individual Tamil characters
            characters = []
            for char in validated_text:
                if self.tamil_pattern.match(char):
                    characters.append(char)
            
            return characters
            
        except Exception as e:
            if isinstance(e, (InvalidTextError, TokenizationError)):
                raise
            raise TokenizationError(f"Failed to tokenize characters: {str(e)}")
    
    def tokenize_graphemes(self, text: str) -> List[str]:
        """
        Tokenize Tamil text into grapheme clusters (logical characters).
        
        This method properly handles Tamil script's complex character structure,
        including base characters with combining marks, conjunct consonants, etc.
        
        Args:
            text: Tamil text to tokenize
            
        Returns:
            List of grapheme cluster tokens (excluding whitespace)
            
        Raises:
            InvalidTextError: If text is invalid
            TokenizationError: If tokenization fails
        """
        try:
            validated_text = self._validate_text(text)
            
            # Use grapheme pattern to extract proper Tamil character clusters
            graphemes = self.grapheme_pattern.findall(validated_text)
            
            # Filter out empty matches and non-Tamil characters
            filtered_graphemes = []
            for grapheme in graphemes:
                if grapheme and self.tamil_pattern.match(grapheme):
                    filtered_graphemes.append(grapheme)
            
            return filtered_graphemes
            
        except Exception as e:
            if isinstance(e, (InvalidTextError, TokenizationError)):
                raise
            raise TokenizationError(f"Failed to tokenize graphemes: {str(e)}")
    
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
            method: Tokenization method ("words", "sentences", "characters", "syllables", "graphemes")
            
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
        elif method == "syllables":
            return self.tokenize_syllables(text)
        elif method == "graphemes":
            return self.tokenize_graphemes(text)
        else:
            raise TokenizationError(f"Unknown tokenization method: {method}")
    
    def tokenize_syllables(self, text: str) -> List[str]:
        """
        Tokenize Tamil text into syllables.
        
        Tamil syllables follow specific patterns:
        - V (vowel)
        - CV (consonant + vowel)
        - CCV (consonant + consonant + vowel)
        
        Args:
            text: Tamil text to tokenize
            
        Returns:
            List of syllable tokens
            
        Raises:
            InvalidTextError: If text is invalid
            TokenizationError: If tokenization fails
        """
        try:
            validated_text = self._validate_text(text)
            
            # Pattern for Tamil syllables
            syllable_pattern = re.compile(
                r'[\u0B85-\u0B94]|'  # Independent vowels (V)
                r'[\u0B95-\u0BB9](?:[\u0BCD][\u0B95-\u0BB9])*(?:[\u0BBE-\u0BCC]|[\u0BD7])?|'  # Consonant clusters with vowel signs (C+V, CC+V)
                r'[\u0B95-\u0BB9][\u0BCD](?![\u0B95-\u0BB9])'  # Consonant with virama at end
            )
            
            syllables = syllable_pattern.findall(validated_text)
            
            # Filter out empty matches
            filtered_syllables = [syl for syl in syllables if syl and self.tamil_pattern.match(syl)]
            
            return filtered_syllables
            
        except Exception as e:
            if isinstance(e, (InvalidTextError, TokenizationError)):
                raise
            raise TokenizationError(f"Failed to tokenize syllables: {str(e)}")
    
    def analyze_word_structure(self, word: str) -> dict:
        """
        Analyze the structure of a Tamil word.
        
        Args:
            word: Tamil word to analyze
            
        Returns:
            Dictionary containing word structure analysis
        """
        try:
            if not word or not self.tamil_pattern.match(word):
                return {
                    'is_tamil': False,
                    'characters': [],
                    'syllables': [],
                    'character_count': 0,
                    'syllable_count': 0,
                    'has_conjuncts': False,
                    'has_vowel_signs': False
                }
            
            characters = self.tokenize_characters(word)
            syllables = self.tokenize_syllables(word)
            
            # Check for conjuncts (consonant clusters)
            has_conjuncts = bool(re.search(r'[\u0B95-\u0BB9][\u0BCD][\u0B95-\u0BB9]', word))
            
            # Check for vowel signs
            has_vowel_signs = bool(re.search(r'[\u0BBE-\u0BCC\u0BD7]', word))
            
            return {
                'is_tamil': True,
                'characters': characters,
                'syllables': syllables,
                'character_count': len(characters),
                'syllable_count': len(syllables),
                'has_conjuncts': has_conjuncts,
                'has_vowel_signs': has_vowel_signs
            }
            
        except Exception as e:
            raise TokenizationError(f"Failed to analyze word structure: {str(e)}")
    
    def get_statistics(self, text: str) -> dict:
        """
        Get comprehensive statistics about Tamil text.
        
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
            syllables = self.tokenize_syllables(validated_text)
            
            # Analyze word structures
            word_structures = [self.analyze_word_structure(word) for word in words]
            tamil_words = [ws for ws in word_structures if ws['is_tamil']]
            
            # Count conjuncts and vowel signs
            words_with_conjuncts = sum(1 for ws in tamil_words if ws['has_conjuncts'])
            words_with_vowel_signs = sum(1 for ws in tamil_words if ws['has_vowel_signs'])
            
            return {
                'total_characters': len(validated_text),
                'tamil_characters': len(characters),
                'words': len(words),
                'tamil_words': len(tamil_words),
                'sentences': len(sentences),
                'syllables': len(syllables),
                'average_word_length': sum(len(word) for word in words) / len(words) if words else 0,
                'average_sentence_length': len(words) / len(sentences) if sentences else 0,
                'average_syllables_per_word': len(syllables) / len(words) if words else 0,
                'words_with_conjuncts': words_with_conjuncts,
                'words_with_vowel_signs': words_with_vowel_signs,
                'conjunct_percentage': (words_with_conjuncts / len(tamil_words) * 100) if tamil_words else 0,
                'vowel_sign_percentage': (words_with_vowel_signs / len(tamil_words) * 100) if tamil_words else 0,
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


def tokenize_syllables(text: str) -> List[str]:
    """
    Convenience function to tokenize Tamil text into syllables.
    
    Args:
        text: Tamil text to tokenize
        
    Returns:
        List of syllable tokens
    """
    return _get_default_tokenizer().tokenize_syllables(text)


def tokenize_graphemes(text: str) -> List[str]:
    """
    Convenience function to tokenize Tamil text into grapheme clusters.
    
    Args:
        text: Tamil text to tokenize
        
    Returns:
        List of grapheme cluster tokens
    """
    return _get_default_tokenizer().tokenize_graphemes(text)


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
