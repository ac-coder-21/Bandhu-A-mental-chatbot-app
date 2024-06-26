# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 11:05:47 2022

@author: auuch
"""

import random
import json
import torch
from Anxiety.model import NeuralNet
from Anxiety.data_learning import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
with open('Anxiety.json', 'r', errors='ignore') as f:
    data_json = json.load(f)
    
FILE = "Anxiety.pth"
data = torch.load(FILE)
input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "BOT"
"""
print("I am here to help you")
while True:
    sentence = input("You: ")
    if sentence == "quit":
        break
"""
    
def get_response_anx(msg):
    sentence = tokenize(msg)
    word = bag_of_words(sentence, all_words)
    word = word.reshape(1, word.shape[0])
    word = torch.from_numpy(word).to(device)
    output = model(word)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]
    
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    
    if prob.item() > 0.75:
        for d in data_json["data"]:
            if tag ==d["tag"]:
                return f"{random.choice(d['output'])}"
    else:
        return '2.I do not understand'

if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        sentence = input("You: ")
        if sentence == "quit":
            break

        
        
        resp = get_response(sentence)
        print(resp)
    