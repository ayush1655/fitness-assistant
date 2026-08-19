from google import genai

client=genai.Client()

response=client.models.generate_content(
model="gemini-3.6-flash",
contents="do you love me?"


)

print(response.text)