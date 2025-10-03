import wikipedia
import streamlit as st
from typing import List, Tuple, Optional

class WikipediaHelper:
    """Helper class for Wikipedia operations"""
    
    def __init__(self):
        """Initialize Wikipedia helper"""
        self.supported_languages = {
            'en': 'en',
            'hi': 'hi', 
            'te': 'te'
        }
    
    def search_wikipedia(self, query: str, language: str = 'en') -> List[Tuple[str, str]]:
        """
        Search Wikipedia and return article summaries
        
        Args:
            query: Search query
            language: Language code for Wikipedia
            
        Returns:
            List of tuples containing (title, summary)
        """
        try:
            # Set Wikipedia language
            wikipedia_lang = self.supported_languages.get(language, 'en')
            wikipedia.set_lang(wikipedia_lang)
            
            # Search for articles
            search_results = wikipedia.search(query, results=3)
            
            if not search_results:
                return []
            
            articles = []
            
            for title in search_results:
                try:
                    # Get page summary
                    summary = wikipedia.summary(title, sentences=3)
                    articles.append((title, summary))
                    
                except wikipedia.exceptions.DisambiguationError as e:
                    # Handle disambiguation pages by taking the first option
                    try:
                        if e.options:
                            summary = wikipedia.summary(e.options[0], sentences=3)
                            articles.append((e.options[0], summary))
                    except:
                        continue
                        
                except wikipedia.exceptions.PageError:
                    # Skip if page doesn't exist
                    continue
                    
                except Exception as e:
                    # Skip any other errors for individual pages
                    continue
            
            return articles
            
        except Exception as e:
            # Return empty list if search fails completely
            st.error(f"Wikipedia search error: {str(e)}")
            return []
    
    def get_article_summary(self, title: str, language: str = 'en', sentences: int = 3) -> Optional[str]:
        """
        Get summary of a specific Wikipedia article
        
        Args:
            title: Article title
            language: Language code
            sentences: Number of sentences in summary
            
        Returns:
            Article summary or None if not found
        """
        try:
            wikipedia_lang = self.supported_languages.get(language, 'en')
            wikipedia.set_lang(wikipedia_lang)
            
            summary = wikipedia.summary(title, sentences=sentences)
            return summary
            
        except wikipedia.exceptions.DisambiguationError as e:
            # Try first disambiguation option
            if e.options:
                try:
                    summary = wikipedia.summary(e.options[0], sentences=sentences)
                    return summary
                except:
                    return None
            return None
            
        except wikipedia.exceptions.PageError:
            return None
            
        except Exception as e:
            st.error(f"Error fetching article: {str(e)}")
            return None
    
    def search_and_summarize(self, query: str, language: str = 'en') -> Optional[str]:
        """
        Search Wikipedia and return the best matching summary
        
        Args:
            query: Search query
            language: Language code
            
        Returns:
            Best matching summary or None
        """
        articles = self.search_wikipedia(query, language)
        
        if articles:
            # Return the first (most relevant) article summary
            return articles[0][1]
        
        return None
