from flask import Flask, request, jsonify
import pickle
import json
import re

try:
    # Load trained models and data
    print("Loading models and data...")
    with open("final_model.pkl", "rb") as f:
        model = pickle.load(f)
    print("Loaded final_model.pkl successfully.")

    with open("tfidf_vectorizer.pkl", "rb") as f:
        vectorizer = pickle.load(f)
    print("Loaded tfidf_vectorizer.pkl successfully.")

    with open("label_encoder.pkl", "rb") as f:
        mlb = pickle.load(f)
    print("Loaded label_encoder.pkl successfully.")

    with open("domain_knowledge.json", "r") as f:
        domain_knowledge = json.load(f)
    print("Loaded domain_knowledge.json successfully.")
except Exception as e:
    print(f"Error loading models or data: {e}")
    raise

# from flask import Flask, request, jsonify
# import pickle
# import json
# import re

# # Load trained models and data
# with open("final_model.pkl", "rb") as f:
#     model = pickle.load(f)
# with open("tfidf_vectorizer.pkl", "rb") as f:
#     vectorizer = pickle.load(f)
# with open("label_encoder.pkl", "rb") as f:
#     mlb = pickle.load(f)
# with open("domain_knowledge.json", "r") as f:
#     domain_knowledge = json.load(f)

# Initialize Flask app
app = Flask(__name__)

# # Function: Dictionary-based entity extraction
# def extract_entities_by_dict(text, knowledge_base):
#     extracted_entities = []
#     for category, terms in knowledge_base.items():
#         for term in terms:
#             if term.lower() in text.lower():
#                 extracted_entities.append({"type": category, "value": term})
#     return extracted_entities

# # Function: Regex-based entity extraction
# def extract_entities_by_regex(text):
#     patterns = {
#         "competitor": r"\bCompetitor[A-Z]\b",  # Matches CompetitorX, CompetitorY, etc.
#         "feature": r"\b(?:AI engine|analytics|data pipeline)\b",
#         "pricing": r"\b(?:discount|renewal cost|budget|pricing model)\b"
#     }
#     extracted_entities = []
#     for entity_type, pattern in patterns.items():
#         matches = re.findall(pattern, text, re.IGNORECASE)
#         for match in matches:
#             extracted_entities.append({"type": entity_type, "value": match})
#     return extracted_entities

# Function: Dictionary-based entity extraction
def extract_entities_by_dict(text, knowledge_base):
    print("Running dictionary-based entity extraction...")
    extracted_entities = []
    try:
        for category, terms in knowledge_base.items():
            for term in terms:
                if term.lower() in text.lower():
                    extracted_entities.append({"type": category, "value": term})
        print(f"Dictionary-based entities: {extracted_entities}")
    except Exception as e:
        print(f"Error in dictionary-based entity extraction: {e}")
        raise
    return extracted_entities

# Function: Regex-based entity extraction
def extract_entities_by_regex(text):
    print("Running regex-based entity extraction...")
    patterns = {
        "competitor": r"\bCompetitor[A-Z]\b",  # Matches CompetitorX, CompetitorY, etc.
        "feature": r"\b(?:AI engine|analytics|data pipeline)\b",
        "pricing": r"\b(?:discount|renewal cost|budget|pricing model)\b"
    }
    extracted_entities = []
    try:
        for entity_type, pattern in patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                extracted_entities.append({"type": entity_type, "value": match})
        print(f"Regex-based entities: {extracted_entities}")
    except Exception as e:
        print(f"Error in regex-based entity extraction: {e}")
        raise
    return extracted_entities


# Function: Combine dictionary lookup and regex
def combined_entity_extraction(text, knowledge_base):
    dict_entities = extract_entities_by_dict(text, knowledge_base)
    regex_entities = extract_entities_by_regex(text)
    all_entities = dict_entities + regex_entities
    unique_entities = {f"{e['type']}-{e['value']}": e for e in all_entities}.values()
    return list(unique_entities)

# Simple text summarization
def summarize_text(text):
    return f"Summary: {text[:50]}..." if len(text) > 50 else f"Summary: {text}"

# # Define API endpoint
# @app.route("/predict", methods=["POST"])
# def predict():
#     try:
#         data = request.get_json()
#         print(f"Received data: {data}")  # Add this to debug
#         text_snippet = data.get("text_snippet", "")
#         print(f"Text snippet: {text_snippet}")  # Add this to debug

#         # Perform predictions
#         X_input = vectorizer.transform([text_snippet])
#         print(f"Transformed input: {X_input}")  # Add this to debug

#         predicted_labels = mlb.inverse_transform(model.predict(X_input))[0]
#         print(f"Predicted labels: {predicted_labels}")  # Add this to debug

#         entities = combined_entity_extraction(text_snippet, domain_knowledge)
#         print(f"Extracted entities: {entities}")  # Add this to debug

#         summary = summarize_text(text_snippet)
#         print(f"Summary: {summary}")  # Add this to debug

#         return jsonify({
#             "text_snippet": text_snippet,
#             "predicted_labels": predicted_labels,
#             "extracted_entities": entities,
#             "summary": summary
#         })
#     except Exception as e:
#         print(f"Error occurred: {e}")  # Log any errors that happen
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        print("Received POST request...")
        data = request.get_json()
        print(f"Request data: {data}")

        text_snippet = data.get("text_snippet", "")
        if not text_snippet:
            raise ValueError("Missing 'text_snippet' in request data.")
        print(f"Text snippet: {text_snippet}")

        # Perform vectorizer transformation
        try:
            X_input = vectorizer.transform([text_snippet])
            print(f"Transformed input (X_input): {X_input}")
        except Exception as e:
            print(f"Error in vectorizer transformation: {e}")
            raise

        # Predict labels
        try:
            predicted_labels = mlb.inverse_transform(model.predict(X_input))[0]
            print(f"Predicted labels: {predicted_labels}")
        except Exception as e:
            print(f"Error in model prediction: {e}")
            raise

        # Extract entities
        try:
            entities = combined_entity_extraction(text_snippet, domain_knowledge)
            print(f"Extracted entities: {entities}")
        except Exception as e:
            print(f"Error in entity extraction: {e}")
            raise

        # Generate summary
        try:
            summary = summarize_text(text_snippet)
            print(f"Generated summary: {summary}")
        except Exception as e:
            print(f"Error in text summarization: {e}")
            raise

        # Construct response
        response = {
            "text_snippet": text_snippet,
            "predicted_labels": predicted_labels,
            "extracted_entities": entities,
            "summary": summary
        }
        print(f"Response: {response}")
        return jsonify(response)
    except Exception as e:
        print(f"Error occurred in /predict endpoint: {e}")
        return jsonify({"error": str(e)}), 500
if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(host="0.0.0.0", port=5000)
    print("Flask server is running.")

