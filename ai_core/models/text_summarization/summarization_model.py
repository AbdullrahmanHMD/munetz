from transformers import pipeline


def get_summarization_model(model_path : str):
    return pipeline("summarization", model=model_path)

def summarize(model, text, **kwargs):
    return model(text, **kwargs)[0]['summary_text']


# def summarize(model, text):
#     a_txt = "Summarize the following text: " + text
#     return model(a_txt)[0]['summary_text']
