from enum import Enum



class GPTPrompts(Enum):
    SUMMARIZATION = """Summarize the following text. Do this by following the rules defined in your persona.
    Lastly, keep the summary strictly between {} and {} words"""

    INFO_EXTRACTION = """Extract the information given in the following prompt.
    Make sure to closely follow the rules defined in your persona."""

    CHATBOT = """TO BE ADDED"""
