"""
Text Statistics and Readability Analysis Tool
Provides comprehensive text analysis for business and news content.
"""

import re
import json
from typing import Dict, Union, Any
from dataclasses import dataclass
from collections import Counter


@dataclass
class Tool:
    """Simple tool wrapper class as suggested in the assignment."""
    name: str
    description: str
    fn: callable
    
    def execute(self, **kwargs) -> Any:
        """Execute the tool function with provided kwargs."""
        return self.fn(**kwargs)


def analyze_text(text: str, include_syllables: bool = False) -> Dict[str, Union[str, int, float, Dict]]:
    """
    Analyze text and return comprehensive statistics and readability metrics.
    
    This tool performs detailed text analysis useful for:
    - Content quality assessment
    - Readability optimization
    - SEO analysis
    - Content comparison
    
    Args:
        text (str): The input text to analyze. Must be a non-empty string.
        include_syllables (bool): Whether to include syllable counting (slower but more detailed).
        
    Returns:
        Dict[str, Union[str, int, float, Dict]]: A dictionary containing:
            - basic_stats: Word, sentence, character counts
            - readability_scores: Flesch Reading Ease, grade level
            - vocabulary_analysis: Unique words, lexical diversity
            - error: Error message if any (only on failure)
            
    Raises:
        ValueError: If input validation fails (caught and returned as structured error)
    """
    try:
        # Input validation
        if not isinstance(text, str):
            raise ValueError("Input must be a string")
        
        text = text.strip()
        if not text:
            raise ValueError("Input text cannot be empty")
        
        if len(text) > 100000:  # Reasonable limit
            raise ValueError("Input text exceeds maximum length of 100,000 characters")
        
        if not isinstance(include_syllables, bool):
            raise ValueError("include_syllables must be a boolean")
        
        # Basic text cleaning
        text_clean = re.sub(r'\s+', ' ', text)
        
        # Word counting (split on whitespace)
        words = text_clean.split()
        word_count = len(words)
        
        # Sentence counting (simple regex for ., !, ?)
        sentences = re.split(r'[.!?]+', text_clean)
        sentences = [s.strip() for s in sentences if s.strip()]
        sentence_count = len(sentences)
        
        # Character counting
        char_count = len(text)
        char_count_no_spaces = len(text.replace(' ', ''))
        
        # Average word length
        avg_word_length = sum(len(word) for word in words) / word_count if word_count > 0 else 0
        
        # Vocabulary analysis
        unique_words = set(word.lower() for word in words)
        unique_word_count = len(unique_words)
        lexical_diversity = unique_word_count / word_count if word_count > 0 else 0
        
        # Word frequency (top 10)
        word_freq = Counter(word.lower() for word in words).most_common(10)
        
        # Readability calculations
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        
        # Simple syllable estimation (heuristic)
        def count_syllables(word):
            if include_syllables:
                word = word.lower()
                count = 0
                vowels = 'aeiouy'
                if word and word[0] in vowels:
                    count += 1
                for index in range(1, len(word)):
                    if word[index] in vowels and word[index-1] not in vowels:
                        count += 1
                if word.endswith('e'):
                    count -= 1
                if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
                    count += 1
                if count == 0:
                    count = 1
                return count
            return 0
        
        if include_syllables:
            total_syllables = sum(count_syllables(word) for word in words)
            syllables_per_word = total_syllables / word_count if word_count > 0 else 0
        else:
            total_syllables = 0
            syllables_per_word = 0
        
        # Flesch Reading Ease score
        if sentence_count > 0 and word_count > 0:
            if include_syllables and total_syllables > 0:
                flesch_score = 206.835 - 1.015 * (word_count / sentence_count) - 84.6 * (total_syllables / word_count)
            else:
                # Approximate if no syllable data
                flesch_score = 206.835 - 1.015 * (word_count / sentence_count) - 84.6 * (avg_word_length * 0.5)
        else:
            flesch_score = 0
        
        # Clamp score to reasonable range
        flesch_score = max(0, min(100, flesch_score))
        
        # Flesch-Kincaid Grade Level
        if sentence_count > 0 and word_count > 0:
            if include_syllables and total_syllables > 0:
                grade_level = 0.39 * (word_count / sentence_count) + 11.8 * (total_syllables / word_count) - 15.59
            else:
                grade_level = 0.39 * (word_count / sentence_count) + 11.8 * (avg_word_length * 0.5) - 15.59
        else:
            grade_level = 0
        
        grade_level = max(0, grade_level)
        
        # Determine reading level description
        if flesch_score >= 90:
            reading_level = "Very Easy (5th grade)"
        elif flesch_score >= 80:
            reading_level = "Easy (6th grade)"
        elif flesch_score >= 70:
            reading_level = "Fairly Easy (7th grade)"
        elif flesch_score >= 60:
            reading_level = "Standard (8th-9th grade)"
        elif flesch_score >= 50:
            reading_level = "Fairly Difficult (10th-12th grade)"
        elif flesch_score >= 30:
            reading_level = "Difficult (College)"
        else:
            reading_level = "Very Difficult (College Graduate)"
        
        return {
            "basic_stats": {
                "word_count": word_count,
                "sentence_count": sentence_count,
                "character_count": char_count,
                "character_count_no_spaces": char_count_no_spaces,
                "avg_word_length": round(avg_word_length, 2),
                "avg_sentence_length": round(avg_sentence_length, 2)
            },
            "vocabulary_analysis": {
                "unique_word_count": unique_word_count,
                "lexical_diversity": round(lexical_diversity, 3),
                "top_10_words": dict(word_freq)
            },
            "readability_scores": {
                "flesch_reading_ease": round(flesch_score, 2),
                "flesch_kincaid_grade": round(grade_level, 2),
                "reading_level": reading_level
            },
            "metadata": {
                "syllable_count": total_syllables if include_syllables else "Not calculated (set include_syllables=True)",
                "syllables_per_word": round(syllables_per_word, 2) if include_syllables else "Not calculated"
            }
        }
        
    except ValueError as e:
        return {
            "error": f"Validation error: {str(e)}",
            "basic_stats": {},
            "vocabulary_analysis": {},
            "readability_scores": {}
        }
    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}",
            "basic_stats": {},
            "vocabulary_analysis": {},
            "readability_scores": {}
        }


# Create the tool instance
text_analysis_tool = Tool(
    name="text_analyzer",
    description="Analyzes text to provide statistics, vocabulary insights, and readability scores. Useful for content assessment, SEO optimization, and ensuring appropriate reading levels.",
    fn=analyze_text
)