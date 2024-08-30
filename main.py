import customtkinter as ctk
import requests
from chat_code import get_response, handle_location_query, handle_directions_query
from PIL import Image
import webbrowser
import re
 
 
# Google Cloud Translation API key
API_KEY = "AIzaSyBale6GUW-7By0SrLqHqdZ94WNgjG0urWo"
 
# Supported languages
LANGUAGES = {
    "English": "en",
    "French": "fr",
    "Spanish": "es",
}
 
def translate_text(text, target_language):
    """
    Translates text using Google Cloud Translation API.
    """
    url = f"https://translation.googleapis.com/language/translate/v2"
    params = {
        'q': text,
        'target': target_language,
        'key': API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()['data']['translations'][0]['translatedText']
    return text
 
def send_message(event=None):
    user_input = user_entry.get()
    target_language = LANGUAGES[language_var.get()]
 
    # Translate user input to English
    translated_input = translate_text(user_input, "en")
   
    chat_log.configure(state=ctk.NORMAL)
    chat_log.insert(ctk.END, f"You: {user_input}\n\n")
 
    if "map" in translated_input.lower():
        location = translated_input.split("map of")[-1].strip()
        response = handle_location_query(location)
    elif "directions" in translated_input.lower():
        origin, destination = translated_input.split("from")[1].split("to")
        origin = origin.strip()
        destination = destination.strip()
        response = handle_directions_query(origin, destination)
    else:
        response = get_response(translated_input)
 
    # Translate the bot's response back to the selected language
    translated_response = translate_text(response, target_language)
   
    insert_hyperlink(translated_response)
    chat_log.configure(state=ctk.DISABLED)
    user_entry.delete(0, ctk.END)
 
def insert_hyperlink(response):
    """
    Inserts a hyperlink into the chat log.
    """
    # Extract the URL from the response (assuming it ends with a space or period)
    url_match = re.search(r"http[s]?://[^\s]+", response)
   
    if url_match:
        url = url_match.group(0)
       
        def open_link(event):
            webbrowser.open_new(url)
       
        chat_log.insert(ctk.END, "Bot: Click here for directions", "hyperlink")
        chat_log.tag_config("hyperlink", foreground="blue", underline=True)
        chat_log.tag_bind("hyperlink", "<Button-1>", open_link)
        chat_log.insert(ctk.END, "\n\n")
    else:
        chat_log.insert(ctk.END, f"Bot: {response}\n\n")
 
def fill_search_bar(text):
    user_entry.delete(0, ctk.END)
    user_entry.insert(0, text)
    send_message()
 
# Create the main window
root = ctk.CTk()
root.title("City of Brampton Xplor Recreation Chatbot")
 
# Create the chat log
chat_log = ctk.CTkTextbox(root, state=ctk.DISABLED, wrap='word', text_color="black")
chat_log.grid(row=0, column=0, rowspan=8, padx=10, pady=10, sticky='nsew')
 
# Load the image
image_path = "c:/Users/VMehta/Desktop/chatbot code/brampton_logo.png"  # Update this with the path to your image
image = ctk.CTkImage(Image.open(image_path), size=(250, 200))  # Adjust size as needed
 
# Create an image label
image_label = ctk.CTkLabel(root, image=image, text="")
image_label.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky='n')
 
# Define the button texts
button_texts = [
    "How to purchase a membership",
    "How to create an account",
    "Registering for a registered program",
    "Registering for a drop-in program",
    "Booking Tennis courts"
]
 
# Create buttons on the right to fill the search bar
for i, text in enumerate(button_texts):
    btn = ctk.CTkButton(root, text=text, command=lambda t=text: fill_search_bar(t),
                        text_color="white", hover_color="blue", corner_radius=20, font=("Helvetica", 14))
    btn.grid(row=i+1, column=1, padx=10, pady=5, sticky='ew')
 
# Add the Directions button
def prompt_for_directions():
    chat_log.configure(state=ctk.NORMAL)
    chat_log.insert(ctk.END, "Bot: Please enter the origin and destination in the format 'directions from [origin] to [destination]' or 'map to [destination]'.\n\n")
    chat_log.configure(state=ctk.DISABLED)
 
directions_button = ctk.CTkButton(root, text="Directions", command=prompt_for_directions,
                                  text_color="white", hover_color="blue", corner_radius=20,
                                  font=("Helvetica", 14))
directions_button.grid(row=len(button_texts)+1, column=1, padx=10, pady=5, sticky='ew')
 
# Create the language dropdown
language_var = ctk.StringVar(value="English")
language_dropdown = ctk.CTkOptionMenu(root, variable=language_var, values=list(LANGUAGES.keys()),
                                      anchor='center')
language_dropdown.grid(row=len(button_texts)+2, column=1, padx=50, pady=10, sticky='ew')
 
# Create the user input entry box
user_entry = ctk.CTkEntry(root, placeholder_text="Type Here...", width=70, text_color="black")
user_entry.grid(row=len(button_texts)+3, column=0, padx=10, pady=40, sticky='ew')
 
# Create the send button
send_button = ctk.CTkButton(root, text="Send", command=send_message, text_color="white")
send_button.grid(row=len(button_texts)+3, column=1, padx=10, pady=40)
 
# Bind the Enter key to send_message function
root.bind('<Return>', send_message)
 
# Configure column and row weights for resizing
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=0)
 
# Display welcome message
chat_log.configure(state=ctk.NORMAL)
chat_log.insert(ctk.END, "Bot: Welcome to the City of Brampton Xplor Recreation Chatbot! How can I assist you today?\n\n")
chat_log.configure(state=ctk.DISABLED)
 
# Run the application
root.mainloop()



