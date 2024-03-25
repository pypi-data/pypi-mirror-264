#!/usr/bin/env python3

import json
import os
import sys
import argparse
import requests

import pyfiglet
from termcolor import colored

def shell_interface():
	ascii_art = pyfiglet.figlet_format("genai", font="univers")
	colored_ascii = colored(ascii_art, 'green')

	print(colored_ascii)

	version = '1.0.4'
	github = 'https://github.com/Solonce/genai'
	author = 'Solomon Ince'

	print('┌───────────────────────────────────────────────────────')
	print(f"│ Version: {colored(version, 'yellow')}")
	print(f"│ Github: {colored(github, 'blue')}")
	print(f"│ Author: {colored(author, 'blue')}")
	print("└───────────────────────────────────────────────────────")

def generate(payload, context, raw=False):
	key = get_key()
	if key == "":
		print("You need to set up a HuggingFace API key first. Please use the command: \n'genai -S HUGGINGFACE_API_KEY'\n\nVisit: https://huggingface.co/docs/api-inference/en/quicktour#get-your-api-token")
		return "exit"

	API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
	headers = {"Authorization": f"Bearer {key}"}

	_input = {
		"inputs": context + payload,
		"parameters": {"max_new_tokens": 100, "max_time": 3, "return_full_text": False, "do_sample": False},

	}

	response = requests.post(API_URL, headers=headers, json=_input)

	rsp = response.json()[0]["generated_text"].split("TERMINATE")[0]
	if rsp[0] in '\n\t' or rsp[1] in '\n\t':
		if rsp[0] not in '\n\t' and rsp[1] in '\n\t':
			rsp = rsp[1:]
		rsp = rsp.lstrip('\n\t')
		rsp = rsp.rstrip('\n\t')

	if raw:
		print(f"\n{rsp}\n")
	else:
		print(' ┌─────────────────────────────')

		for line in rsp.split('\n'):
			print(f" │ {line}")
		
		print(' └─────────────────────────────\n')


	return



def get_key():
	hidden_dir = os.path.join(os.environ['HOME'], '.genai')
	hidden_file = os.path.join(hidden_dir, 'data.json')

	try:
		with open(hidden_file, 'r') as file:
			data = json.load(file)
			data = data['key']
		return data
	except:
		return ""


def set_key(key):
	hidden_dir = os.path.join(os.environ['HOME'], '.genai')
	hidden_file = os.path.join(hidden_dir, 'data.json')

	if not os.path.exists(hidden_dir):
		os.makedirs(hidden_dir)

	data = {"key": key}

	with open(hidden_file, 'w') as file:
		json.dump(data, file)

	print("API Key Set!")
	return

def main():
	context = """
		You are a simple lightweight text-based AI assistant that excells in programming and problem resolution.
		All your responses are to be as short as they can reasonably be.
		If the solution is any amount of code, respond only with the code.
		Do not pad your responses with text or '\n'.

		After you have finished answering the question, plase type TERMINATE.
		"""


	parser = argparse.ArgumentParser(description="AI text generation tool")
	parser.add_argument('-S', '--set-key', dest='key', help="Set the key for the AI service")
	parser.add_argument('-t', '--text-data', dest='textdata', help="No shell, just string. Make sure to wrap input in double quotes!")
	parser.add_argument('-r', '--raw-data', dest='rawdata', help="Direct raw response from the Mixtral-8x7B-Instruct-v0 model. (As of 3/24/24)")
	parser.add_argument('-c', '--context', dest='context', help="The context in which the Mixtral-8x7B-Instruct-v0 model to operate under. (As of 3/24/24)", default=context)
	

	args = parser.parse_args()

	if args.key:
		set_key(args.key)
	
	try:


		if args.textdata:
			print(f"\n   genai:")
			data = generate(args.textdata, args.context)
		elif args.rawdata:
			data = generate(args.rawdata, args.context, raw=True)

		else:
			shell_interface()
			while True:
				text = input("genai> ")

				if text == "exit":
					break;

				data = generate(text, args.context)
				if data == "exit":
					break;
					print("\nExiting interactive mode.")

	except KeyboardInterrupt:
		pass

