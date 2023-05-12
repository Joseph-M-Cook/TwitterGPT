# TwitterGPT
![Logo](https://github.com/Joseph-M-Cook/TwitterGPT/blob/87265eda9bfc12b37b0e886a2efcf0bec89855fc/TwitterGPT_Logo.png)
TwitterGPT is an AI-powered tool that leverages the power of GPT-4 and Twitter's Search API to answer user questions using real-time Twitter insights, all presented through an interactive Gradio interface.

## Overview
TwitterGPT uses OpenAI's GPT-4 model to generate context-aware search queries based on user input. It then fetches corresponding tweets using Twitter's Search API and summarizes the results, providing insightful answers to user queries.

## Installation
To run this project, you need to install the required Python libraries. You can do this by running:

```bash
pip install -r requirements.txt
```

## Configuration
You need to provide your own API keys for both Twitter and OpenAI. This can be done by replacing the placeholders in the `consumer_key`, `consumer_secret`, `access_token`, `access_token_secret`, and `openai.api_key` variables.

## Usage
To use TwitterGPT, run the script and open the Gradio interface in your browser. Enter your question into the textbox and press enter. The program will generate a context-aware search query, fetch the corresponding tweets, and provide a summarized answer based on the fetched tweets.

## Disclaimer
Please use this responsibly and ensure you comply with both OpenAI's and Twitter's terms of service.


