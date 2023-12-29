from google.generativeai import GenerativeModel
from google.colab import userdata

genai.configure(userdata.get('API_KEY'))

model = GenerativeModel('gemini-pro')

response = model.generate_content('The opposite of hot is')
print(response.text)  # The opposite of hot is cold.
