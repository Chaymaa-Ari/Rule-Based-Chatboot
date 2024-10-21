import nltk
from nltk.chat.util import Chat, reflections
from nltk.stem import PorterStemmer
from nltk import word_tokenize, pos_tag
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Ensure the required packages are downloaded
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Initialize stemmer
stemmer = PorterStemmer()

# Define chatbot patterns and responses focused on data science and AI
pairs = [
    [r"my name is (.*)", ["Hello %1, how can I assist you with data science today?"]],
    [r"hi|hello", ["Hi there! How can I help you ?"]],
    [r"what is your name?", ["I'm a chatbot specialized in data science. What's yours?"]],
    [r"how are you?", ["I'm just a bunch of code, but thanks for asking!"]],
    [r"tell me about|more data science", ["Data science involves extracting insights from structured and unstructured data using various techniques."]],
    [r"what is machine learning?", ["Machine learning is a subset of artificial intelligence that enables systems to learn from data and improve over time."]],
    [r"what is artificial intelligence?", ["Artificial intelligence refers to the simulation of human intelligence in machines, enabling them to perform tasks such as understanding language and making decisions."]],
    [r"how to analyze data?", ["Data analysis involves cleaning, transforming, and modeling data to discover useful information and support decision-making."]],
    [r"what tools are used for data analysis?", ["Common tools for data analysis include Python, R, SQL, and Excel."]],
    [r"what is the role of a data analyst?", ["A data analyst is responsible for interpreting data, analyzing results, and providing ongoing reports to help businesses make informed decisions."]],
    [r"quit|bye", ["Goodbye! If you have more questions in the future, feel free to ask."]],
    [r"(.*)", ["I'm sorry, I don't understand that. Can you rephrase?", "Could you please elaborate on that?"]]
]

class EnhancedChatbot:
    def __init__(self, pairs):
        self.chat = Chat(pairs, reflections)

    def preprocess_input(self, user_input):
        """Preprocess user input by converting to lowercase."""
        return user_input.lower()

    def respond(self, user_input):
        """Generate a response from the chatbot based on preprocessed user input."""
        preprocessed_input = self.preprocess_input(user_input)
        print(f"Preprocessed input: {preprocessed_input}")  # Debug print
        return self.chat.respond(preprocessed_input)


# Initialize the chatbot with enhanced logic
chatbot = EnhancedChatbot(pairs)

# Initialize FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (or specify your frontend URL)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Define a request model
class ChatRequest(BaseModel):
    message: str

# Define a route for chatbot interaction
@app.post("/chat/")
def chat_with_bot(request: ChatRequest):
    user_input = request.message
    response = chatbot.respond(user_input)
    return {"response": response}

# To run the FastAPI server, use the command:
# uvicorn your_script_name:app --reload
