# Importing libraries
import tensorflow
from transformers import AutoModelForCausalLM, AutoTokenizer
from textblob import TextBlob

# Loading chatgpt model and tokenizer
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")

# Encoding user input
user_input = "The economy crisis is coming, red alert, it is dangerous"
encoded_input = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

# Generating chatgpt response
response_ids = model.generate(encoded_input, max_length=50)
print(response_ids)
response_text = tokenizer.decode(response_ids[:, encoded_input.shape[-1]:][0], skip_special_tokens=True)

# Printing user input and chatgpt response
print(f"User: {user_input}")
print(f"ChatGPT: {response_text}")

# Performing sentiment analysis on chatgpt response using TextBlob
response_sentiment = TextBlob(user_input).sentiment.polarity #TextBlob(response_text).sentiment.polarity

# Printing sentiment score and label
print(f"Sentiment score: {response_sentiment}")
if response_sentiment > 0:
  print("Sentiment label: Positive")
elif response_sentiment < 0:
  print("Sentiment label: Negative")
else:
  print("Sentiment label: Neutral")