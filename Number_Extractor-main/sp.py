import spacy
from spacy.matcher import Matcher

# Load the English model
nlp = spacy.load("en_core_web_sm")

# Initialize the matcher
matcher = Matcher(nlp.vocab)

# Define patterns for numerical words (including multi-word patterns and Indian units)
patterns = [
    [{"LOWER": "one"}], [{"LOWER": "two"}], [{"LOWER": "three"}], [{"LOWER": "four"}],
    [{"LOWER": "five"}], [{"LOWER": "six"}], [{"LOWER": "seven"}], [{"LOWER": "eight"}],
    [{"LOWER": "nine"}], [{"LOWER": "ten"}], [{"LOWER": "eleven"}], [{"LOWER": "twelve"}],
    [{"LOWER": "thirteen"}], [{"LOWER": "fourteen"}], [{"LOWER": "fifteen"}], [{"LOWER": "sixteen"}],
    [{"LOWER": "seventeen"}], [{"LOWER": "eighteen"}], [{"LOWER": "nineteen"}], [{"LOWER": "twenty"}],
    [{"LOWER": "thirty"}], [{"LOWER": "forty"}], [{"LOWER": "fifty"}], [{"LOWER": "sixty"}],
    [{"LOWER": "seventy"}], [{"LOWER": "eighty"}], [{"LOWER": "ninety"}], [{"LOWER": "hundred"}],
    [{"LOWER": "thousand"}], [{"LOWER": "million"}], [{"LOWER": "billion"}],
    [{"LOWER": "lakh"}], [{"LOWER": "crore"}],

    # # Patterns for multi-word numerical expressions
    # [{"LOWER": "one"}, {"LOWER": "hundred"}],
    # [{"LOWER": "two"}, {"LOWER": "hundred"}],
    # [{"LOWER": "three"}, {"LOWER": "hundred"}],
    # [{"LOWER": "four"}, {"LOWER": "hundred"}],
    # [{"LOWER": "five"}, {"LOWER": "hundred"}],
    # [{"LOWER": "six"}, {"LOWER": "hundred"}],
    # [{"LOWER": "seven"}, {"LOWER": "hundred"}],
    # [{"LOWER": "eight"}, {"LOWER": "hundred"}],
    # [{"LOWER": "nine"}, {"LOWER": "hundred"}],
    # [{"LOWER": "ten"}, {"LOWER": "thousand"}],
    # [{"LOWER": "hundred"}, {"LOWER": "thousand"}],
    # [{"LOWER": "one"}, {"LOWER": "lakh"}],
    # [{"LOWER": "two"}, {"LOWER": "lakh"}],
    # [{"LOWER": "three"}, {"LOWER": "lakh"}],
    # [{"LOWER": "four"}, {"LOWER": "lakh"}],
    # [{"LOWER": "five"}, {"LOWER": "lakh"}],
    # [{"LOWER": "six"}, {"LOWER": "lakh"}],
    # [{"LOWER": "seven"}, {"LOWER": "lakh"}],
    # [{"LOWER": "eight"}, {"LOWER": "lakh"}],
    # [{"LOWER": "nine"}, {"LOWER": "lakh"}],
    # [{"LOWER": "one"}, {"LOWER": "crore"}],
    # [{"LOWER": "two"}, {"LOWER": "crore"}],
    # [{"LOWER": "three"}, {"LOWER": "crore"}],
    # [{"LOWER": "four"}, {"LOWER": "crore"}],
    # [{"LOWER": "five"}, {"LOWER": "crore"}],
    # [{"LOWER": "six"}, {"LOWER": "crore"}],
    # [{"LOWER": "seven"}, {"LOWER": "crore"}],
    # [{"LOWER": "eight"}, {"LOWER": "crore"}],
    # [{"LOWER": "nine"}, {"LOWER": "crore"}]
]

# Add patterns to the matcher
for pattern in patterns:
    matcher.add("NUMERIC_WORDS", [pattern])

# Define the custom NER function
def extract_numerical_data(text):
    doc = nlp(text)
    matches = matcher(doc)
    spans = [doc[start:end] for match_id, start, end in matches]
    
    # Sort spans by start position
    spans = sorted(spans, key=lambda span: span.start)
    
    # Merge contiguous spans
    merged_spans = []
    current_span = spans[0]
    for span in spans[1:]:
        if span.start <= current_span.end:
            current_span = doc[current_span.start:span.end]
        else:
            merged_spans.append(current_span)
            current_span = span
    merged_spans.append(current_span)
    
    return [(span.text, "NUM") for span in merged_spans]

# Test the function
text = "I have four thousand five hundred sixty two dollars"
print(extract_numerical_data(text))
