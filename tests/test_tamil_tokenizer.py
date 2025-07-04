"""
Tests for tamil-tokenizer library.
"""

import pytest
from unittest.mock import patch

from tamil_tokenizer import (
    TamilTokenizer,
    tokenize_words,
    tokenize_sentences,
    tokenize_characters,
    clean_text,
    normalize_text,
)
from tamil_tokenizer.exceptions import (
    InvalidTextError,
    TokenizationError,
)


class TestTextValidation:
    """Test text validation functionality."""
    
    def test_valid_text(self):
        """Test valid Tamil text."""
        tokenizer = TamilTokenizer()
        result = tokenizer._validate_text("தமிழ் மொழி")
        assert result == "தமிழ் மொழி"
    
    def test_text_with_whitespace(self):
        """Test text with leading/trailing whitespace."""
        tokenizer = TamilTokenizer()
        result = tokenizer._validate_text("  தமிழ் மொழி  ")
        assert result == "தமிழ் மொழி"
    
    def test_none_text(self):
        """Test None text."""
        tokenizer = TamilTokenizer()
        with pytest.raises(InvalidTextError):
            tokenizer._validate_text(None)
    
    def test_empty_text(self):
        """Test empty text."""
        tokenizer = TamilTokenizer()
        with pytest.raises(InvalidTextError):
            tokenizer._validate_text("")
    
    def test_whitespace_only_text(self):
        """Test whitespace-only text."""
        tokenizer = TamilTokenizer()
        with pytest.raises(InvalidTextError):
            tokenizer._validate_text("   ")
    
    def test_non_string_text(self):
        """Test non-string text."""
        tokenizer = TamilTokenizer()
        with pytest.raises(InvalidTextError):
            tokenizer._validate_text(123)


class TestWordTokenization:
    """Test word tokenization functionality."""
    
    def test_simple_word_tokenization(self):
        """Test simple word tokenization."""
        tokenizer = TamilTokenizer()
        result = tokenizer.tokenize_words("தமிழ் மொழி அழகான மொழி")
        assert len(result) == 4
        assert "தமிழ்" in result
        assert "மொழி" in result
        assert "அழகான" in result
    
    def test_single_word(self):
        """Test single word tokenization."""
        tokenizer = TamilTokenizer()
        result = tokenizer.tokenize_words("தமிழ்")
        assert len(result) == 1
        assert result[0] == "தமிழ்"
    
    def test_words_with_extra_spaces(self):
        """Test words with extra spaces."""
        tokenizer = TamilTokenizer()
        result = tokenizer.tokenize_words("தமிழ்   மொழி")
        assert len(result) == 2
        assert "தமிழ்" in result
        assert "மொழி" in result
    
    def test_convenience_function(self):
        """Test convenience function for word tokenization."""
        result = tokenize_words("தமிழ் மொழி")
        assert len(result) == 2
        assert "தமிழ்" in result
        assert "மொழி" in result


class TestSentenceTokenization:
    """Test sentence tokenization functionality."""
    
    def test_simple_sentence_tokenization(self):
        """Test simple sentence tokenization."""
        tokenizer = TamilTokenizer()
        result = tokenizer.tokenize_sentences("வணக்கம். நீங்கள் எப்படி இருக்கிறீர்கள்?")
        assert len(result) == 2
        assert "வணக்கம்" in result[0]
        assert "நீங்கள்" in result[1]
    
    def test_single_sentence(self):
        """Test single sentence."""
        tokenizer = TamilTokenizer()
        result = tokenizer.tokenize_sentences("தமிழ் அழகான மொழி")
        assert len(result) == 1
        assert result[0] == "தமிழ் அழகான மொழி"
    
    def test_sentences_with_different_endings(self):
        """Test sentences with different ending punctuation."""
        tokenizer = TamilTokenizer()
        result = tokenizer.tokenize_sentences("வணக்கம்! நலமா? நன்றாக இருக்கிறேன்.")
        assert len(result) == 3
    
    def test_convenience_function(self):
        """Test convenience function for sentence tokenization."""
        result = tokenize_sentences("வணக்கம். நலமா?")
        assert len(result) == 2


class TestCharacterTokenization:
    """Test character tokenization functionality."""
    
    def test_simple_character_tokenization(self):
        """Test simple character tokenization."""
        tokenizer = TamilTokenizer()
        result = tokenizer.tokenize_characters("தமிழ்")
        assert len(result) == 4  # த, ம, ி, ழ், ்
        assert "த" in result
        assert "ம" in result
    
    def test_characters_with_spaces(self):
        """Test character tokenization with spaces (should ignore spaces)."""
        tokenizer = TamilTokenizer()
        result = tokenizer.tokenize_characters("த மி")
        assert len(result) == 2
        assert "த" in result
        assert "மி" in result
    
    def test_convenience_function(self):
        """Test convenience function for character tokenization."""
        result = tokenize_characters("தமிழ்")
        assert len(result) >= 3  # At least த, ம, ழ்


class TestTextCleaning:
    """Test text cleaning functionality."""
    
    def test_clean_text_whitespace(self):
        """Test cleaning text with extra whitespace."""
        tokenizer = TamilTokenizer()
        result = tokenizer.clean_text("தமிழ்   மொழி   அழகு")
        assert result == "தமிழ் மொழி அழகு"
    
    def test_clean_text_with_punctuation(self):
        """Test cleaning text with punctuation removal."""
        tokenizer = TamilTokenizer()
        result = tokenizer.clean_text("தமிழ், மொழி!", remove_punctuation=True)
        assert "," not in result
        assert "!" not in result
        assert "தமிழ்" in result
        assert "மொழி" in result
    
    def test_clean_text_without_punctuation_removal(self):
        """Test cleaning text without punctuation removal."""
        tokenizer = TamilTokenizer()
        result = tokenizer.clean_text("தமிழ், மொழி!", remove_punctuation=False)
        assert "," in result
        assert "!" in result
    
    def test_convenience_function(self):
        """Test convenience function for text cleaning."""
        result = clean_text("தமிழ்   மொழி")
        assert result == "தமிழ் மொழி"


class TestTextNormalization:
    """Test text normalization functionality."""
    
    def test_normalize_text(self):
        """Test text normalization."""
        tokenizer = TamilTokenizer()
        result = tokenizer.normalize_text("  தமிழ்   மொழி  ")
        assert result == "தமிழ் மொழி"
    
    def test_convenience_function(self):
        """Test convenience function for text normalization."""
        result = normalize_text("  தமிழ்   மொழி  ")
        assert result == "தமிழ் மொழி"


class TestGeneralTokenization:
    """Test general tokenization method."""
    
    def test_tokenize_words_method(self):
        """Test general tokenize method with words."""
        tokenizer = TamilTokenizer()
        result = tokenizer.tokenize("தமிழ் மொழி", "words")
        assert len(result) == 2
    
    def test_tokenize_sentences_method(self):
        """Test general tokenize method with sentences."""
        tokenizer = TamilTokenizer()
        result = tokenizer.tokenize("வணக்கம். நலமா?", "sentences")
        assert len(result) == 2
    
    def test_tokenize_characters_method(self):
        """Test general tokenize method with characters."""
        tokenizer = TamilTokenizer()
        result = tokenizer.tokenize("தமிழ்", "characters")
        assert len(result) >= 3
    
    def test_invalid_tokenization_method(self):
        """Test invalid tokenization method."""
        tokenizer = TamilTokenizer()
        with pytest.raises(TokenizationError):
            tokenizer.tokenize("தமிழ்", "invalid_method")


class TestStatistics:
    """Test statistics functionality."""
    
    def test_get_statistics(self):
        """Test getting text statistics."""
        tokenizer = TamilTokenizer()
        stats = tokenizer.get_statistics("தமிழ் மொழி அழகான மொழி.")
        
        assert 'total_characters' in stats
        assert 'tamil_characters' in stats
        assert 'words' in stats
        assert 'sentences' in stats
        assert 'average_word_length' in stats
        assert 'average_sentence_length' in stats
        
        assert stats['words'] > 0
        assert stats['tamil_characters'] > 0
    
    def test_statistics_with_empty_result(self):
        """Test statistics with text that has no Tamil characters."""
        tokenizer = TamilTokenizer()
        # This should still work but have 0 Tamil characters
        stats = tokenizer.get_statistics("Hello World!")
        assert stats['tamil_characters'] == 0


class TestErrorHandling:
    """Test error handling."""
    
    def test_tokenization_error_propagation(self):
        """Test that tokenization errors are properly propagated."""
        tokenizer = TamilTokenizer()
        
        with pytest.raises(InvalidTextError):
            tokenizer.tokenize_words("")
        
        with pytest.raises(InvalidTextError):
            tokenizer.tokenize_sentences(None)
        
        with pytest.raises(InvalidTextError):
            tokenizer.tokenize_characters("   ")


if __name__ == '__main__':
    pytest.main([__file__])
