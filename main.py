import openai
import configparser
import os
from concurrent.futures import ThreadPoolExecutor
from tiktoken import Tokenizer, TokenizerException
import argparse

def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    openai_api_key = config.get("openai", "api_key")
    language_models = {k: v for k, v in config.items("language_models")}
    colors = {k: v for k, v in config.items("colors")}

    return openai_api_key, language_models, colors

api_key, LANGUAGE_MODELS, COLORS = read_config("config.ini")
openai.api_key = api_key

def colored_print(message, color):
    print(f"{COLORS[color]}{message}{COLORS['reset']}")

def load_text(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def save_to_file(responses, output_file):
    with open(output_file, 'w') as file:
        for response in responses:
            file.write(response + '\n')

def call_openai_api(chunk, model, temperature):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "PASS IN ANY ARBITRARY SYSTEM VALUE TO GIVE THE AI AN IDENITY"},
            {"role": "user", "content": f"OPTIONAL PREPROMPTING FOLLOWING BY YOUR DATA TO PASS IN: {chunk}."},
        ],
        max_tokens=1750,
        n=1,
        stop=None,
        temperature=temperature,
    )
    return response.choices[0]['message']['content'].strip()

def call_openai_api_summary(chunk, model, temperature):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text."},
            {"role": "user", "content": f"Please summarize the following text: {chunk}"},
        ],
        max_tokens=1750,
        n=1,
        stop=None,
        temperature=temperature,
    )
    return response.choices[0]['message']['content'].strip()

def split_into_chunks(text, tokens=1500):
    words = text.split()
    chunks = [' '.join(words[i:i + tokens]) for i in range(0, len(words), tokens)]
    return chunks

def process_chunks(input_file, output_file, model, tokens, temperature):
    text = load_text(input_file)
    chunks = split_into_chunks(text, tokens)

    with ThreadPoolExecutor() as executor:
        responses = list(executor.map(lambda chunk: call_openai_api(chunk, model, temperature), chunks))

    save_to_file(responses, output_file)

def process_text_summary(input_file, output_file, model, tokens, temperature):
    text = load_text(input_file)
    chunks = split_into_chunks(text, tokens)

    with ThreadPoolExecutor() as executor:
        summaries = list(executor.map(lambda chunk: call_openai_api_summary(chunk, model, temperature), chunks))

    save_to_file(summaries, output_file)

def process_text_interactive(model, tokens, temperature):
    colored_print("Interactive mode: Type your input and press Enter. Type 'exit' to quit.")
    while True:
        user_input = input("> ")
        if user_input.lower() == "exit":
            break

        chunk = user_input.strip()
        response = call_openai_api(chunk, model, temperature)
        colored_print(f"AI: {response}")

def process_directory(input_dir, output_dir, model, tokens, temperature, summary):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        input_file = os.path.join(input_dir, filename)
        output_file = os.path.join(output_dir, filename)

        if os.path.isfile(input_file):
            if summary:
                process_text_summary(input_file, output_file, model, tokens, temperature)
           
            else:
                process_chunks(input_file, output_file, model, tokens, temperature)
            colored_print(f"Processed {input_file} -> {output_file}")

def count_tokens(text):
    tokenizer = Tokenizer()
    try:
        tokens = list(tokenizer.tokenize(text))
        return len(tokens)
    except TokenizerException:
        return 0

def dry_run(input_file, tokens):
    text = load_text(input_file)
    chunks = split_into_chunks(text, tokens)

    total_tokens = 0
    for chunk in chunks:
        token_count = count_tokens(chunk)
        total_tokens += token_count

    api_calls = len(chunks)

    return total_tokens, api_calls

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process text using OpenAI API")
    parser.add_argument("-i", "--input", required=True, help="Input file or directory")
    parser.add_argument("-o", "--output", required=True, help="Output file or directory")
    parser.add_argument("-t", "--tokens", type=int, default=1500, help="Tokens per chunk (default: 1500)")
    parser.add_argument("-l", "--language", default="en", choices=LANGUAGE_MODELS.keys(), help="Language of the input text (default: en)")
    parser.add_argument("-n", "--dry-run", action="store_true", help="Perform a dry run without making actual API requests")
    parser.add_argument("-m", "--interactive", action="store_true", help="Interactive mode")
    parser.add_argument("-s", "--summary", action="store_true", help="Generate summaries")
    parser.add_argument("-p", "--temperature", type=float, default=0.5, help="Sampling temperature (default: 0.5)")

    args = parser.parse_args()

    model = LANGUAGE_MODELS[args.language]

    if args.dry_run:
        total_tokens, api_calls = dry_run(args.input, args.tokens)
        colored_print(f"Dry run: Estimated tokens: {total_tokens}, Estimated API calls: {api_calls}")
    elif args.interactive:
        process_text_interactive(model, args.tokens, args.temperature)
    elif os.path.isfile(args.input):
        if args.summary:
            process_text_summary(args.input, args.output, model, args.tokens, args.temperature)
        else:
            process_chunks(args.input, args.output, model, args.tokens, args.temperature)
    elif os.path.isdir(args.input):
        process_directory(args.input, args.output, model, args.tokens, args.temperature, args.summary)
    else:
        colored_print("Error: Input path is not a valid file or directory")

