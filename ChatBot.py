import tkinter as tk
import random
import re
from PIL import Image, ImageTk

class ChatbotGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chatbot")
        self.geometry("400x500")
        self.configure(bg="#d6d6d6")

        icon_image = Image.open(
            "C:/Users/H P826/Downloads/Untitled design.png")
        icon_photo = ImageTk.PhotoImage(icon_image)
        self.tk.call("wm", "iconphoto", self._w, icon_photo)

        self.support_responses = {
            'ask_about_product': r'(product|new product|details about product)',
            'technical_support': r'(technical support|tech help|issue)',
            'about_returns': r'(return policy|how to return a product|return)',
        }

        # Chat history
        self.chat_history = tk.Text(self, wrap=tk.WORD, state=tk.DISABLED, font=("Arial", 14, "bold"), bg="#225", fg="#d6d6d6")
        self.chat_history.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

        # User input entry
        self.user_input = tk.Entry(self, font=("Arial", 14, "bold"))
        self.user_input.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Send button
        self.send_button = tk.Button(self, text="Send", font=("Arial", 14, "bold"), command=self.handle_input)
        self.send_button.grid(row=1, column=1, padx=10, pady=10, sticky="e")

        # Configure grid weights to make the chat history expandable
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.display_response("Chatbot: Hello! What's your name?")



    def handle_input(self):
        user_input = self.user_input.get().strip().lower()
        self.user_input.delete(0, tk.END)
        self.display_response(f"You: {user_input}")

        if user_input in ("quit", "pause", "exit", "goodbye", "bye", "farewell","thankyou"):
            self.display_response("Chatbot: Thanks for using the chatbot. Goodbye!")
            self.after(2000, self.destroy)  # Close the application after 2 seconds
        elif not hasattr(self, 'user_name'):
            self.user_name = user_input
            self.display_response(f"Chatbot: Hello, {self.user_name}! How can I assist you today?")
        else:
            intent = self.match_reply(user_input)
            response = self.generate_response(intent)
            self.display_response("Chatbot: " + response)

    def match_reply(self, message):
        for intent, regexPattern in self.support_responses.items():
            found_match = re.search(regexPattern, message)
            if found_match:
                return intent
        return 'general_query'

    def generate_response(self, intent):
        if intent == 'ask_about_product':
            responses = ["We recently launched a new product and so far it has top-notch and has excellent reviews.",
                         "You can find all the details about our products on our website."]
            return random.choice(responses)
        elif intent == 'technical_support':
            responses = ["Please check out our technical support page.",
                         "You can also call our helpline for further assistance at 021-24567."]
            return random.choice(responses)
        elif intent == 'about_returns':
            responses = ["We have a strict 30 days return policy.",
                         "Please make sure the product is unused for a successful return."]
            return random.choice(responses)
        else:
            responses = ["I'm here to assist you. How can I help you today?",
                         "Is there anything specific you would like to know or ask?"]
            return random.choice(responses)

    def display_response(self, response):
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, response + "\n")
        self.chat_history.config(state=tk.DISABLED)
        self.chat_history.see(tk.END)

if __name__ == "__main__":
    app = ChatbotGUI()
    app.mainloop()
