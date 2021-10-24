
# Imports the Google Cloud client library
from google.cloud import language_v1
#from googleapiclient.discovery import build
import sys
import time
import pip._vendor.requests as requests

filename = "C:\\Users\\zhiho\\Downloads\\Recording.m4a"
 
def read_file(filename, chunk_size=5242880):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data
 
headers = {'authorization': "2e1eaa1b8a924f528140194d3783924f"}
response = requests.post('https://api.assemblyai.com/v2/upload',
                         headers=headers,
                         data=read_file(filename))

endpoint = "https://api.assemblyai.com/v2/transcript"

json = {
  "audio_url": response.json()["upload_url"]
}

headers = {
    "authorization": "2e1eaa1b8a924f528140194d3783924f",
    "content-type": "application/json"
}

response = requests.post(endpoint, json=json, headers=headers)

endpoint = "https://api.assemblyai.com/v2/transcript/" + response.json()["id"]

headers = {
    "authorization": "2e1eaa1b8a924f528140194d3783924f",
}

response = requests.get(endpoint, headers=headers)
while (response.json()["status"] == "queued" or response.json()["status"] == "processing"):
    response = requests.get(endpoint, headers=headers)

#print(response.json()["status"])
#print(response.json()["text"])

# Instantiates a client
client = language_v1.LanguageServiceClient()

# The text to analyze
#text = "I love my friends. They help me out so much. I am so appreciative of them. Today we went to get some brunch, and we also did some crafts in the common room. I wish that every day could be like this."

text = response.json()["text"]
document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

# Detects the sentiment of the text
sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

print("Text: {}".format(text))
print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))

