import ast


def process_genai_response(response_text):
    if "python\n" in response_text:
        cleaned_string = response_text.strip().strip("```python\n").strip("```")
    try:
        return ast.literal_eval(cleaned_string)
    except (ValueError, SyntaxError) as e:
        raise ValueError(f"Error processing GenAI response: {str(e)}")
