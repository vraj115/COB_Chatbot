import openai
from mapping import get_map_url, get_directions_url

# Initialize the OpenAI API key
openai.api_key = 'sk-proj-qdwzBDSEa72qpitIXDGGT3BlbkFJrcPZ9kkAcdLQqd1agVfy'

def get_response_from_fine_tuned_model(prompt):
    try:
        response = openai.ChatCompletion.create(
            model='ft:gpt-3.5-turbo-0125:personal:cob:9rrDLbvZ',
            messages=[
                {"role": "system", "content": "You are a Brampton, Ontario resident seeking help on the Xplor Recreation website. Accordingly, you ask the chatbot for assisting with the issue that you have."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error in get_response_from_fine_tuned_model: {e}")
        return "Sorry, I couldn't process your request."

def get_response_from_base_model(prompt):
    try:
        # Provide context about the City of Brampton Xplor website
        context_prompt = (
            "You are a knowledgeable assistant for the City of Brampton Xplor Recreation website. "
            "Provide relevant information and help with inquiries related to memberships, accounts, programs, and bookings. "
            "Respond appropriately to the following query:\n\n" + prompt
        )
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": context_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error in get_response_from_base_model: {e}")
        return "Sorry, I couldn't process your request."

def is_question_within_domain(prompt):
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',  # Use base GPT model for classification
            messages=[
                {"role": "system", "content": "You are a classifier to determine if a question is within the domain of a fine-tuned model for Brampton, Ontario Xplor Recreation website."},
                {"role": "user", "content": f"Can the fine-tuned model handle the following question: {prompt}"}
            ],
            max_tokens=10
        )
        classification = response['choices'][0]['message']['content'].strip().lower()
        print(f"Classification Response: {classification}")  # Debug statement
        return "yes" in classification
    except Exception as e:
        print(f"Error in is_question_within_domain: {e}")
        return False

def get_response(prompt):
    try:
        if is_question_within_domain(prompt):
            print(f"Using fine-tuned model for prompt: {prompt}")  # Debug statement
            return get_response_from_fine_tuned_model(prompt)
        else:
            print(f"Using base model for prompt: {prompt}")  # Debug statement
            return get_response_from_base_model(prompt)
    except Exception as e:
        print(f"Error in get_response: {e}")
        return "Sorry, I couldn't process your request."
    
def handle_location_query(location):
    map_url = get_map_url(location)
    return f"Here is the map for {location}: {map_url}"

def handle_directions_query(origin, destination):
    directions_url = get_directions_url(origin, destination)
    return f"Here are the directions from {origin} to {destination}: {directions_url}"

# Example usage
if __name__ == "__main__":
    prompt = "How do I book a tennis court?"
    response = get_response(prompt)
    print(response)
