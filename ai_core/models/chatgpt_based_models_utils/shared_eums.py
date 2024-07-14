from enum import Enum

class GPTPrompts(Enum):
    SUMMARIZATION = """PROMPT: Summarize the following text. Do this by following the rules defined in your persona. Lastly, keep the summary strictly between {} and {} words"""

    INFO_EXTRACTION = """PROMPT: Extract the information in the given EXTRACTION_LIST: {} from the text given below. Make sure to closely follow the rules defined in your persona."""

    INFO_EXTRACTION_ASSISTANT = """PROMPT: Extract the information in the given EXTRACTION_LIST: {} from the files given in the attachments. Make sure to closely follow the rules defined in your persona."""

    CHATBOT = """
<START KNOWLEDGE>
{}
<END KNOWLEDGE>

PROMPT: {}

You have chat history to refer to -> HISTORY: {}"""
