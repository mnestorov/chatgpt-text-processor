import openai
import os
import argparse
from concurrent.futures import ThreadPoolExecutor
from config import OPENAI_API_KEY, LANGUAGE_MODELS, COLORS

openai.api_key = OPENAI_API_KEY

def colored_print(message, color="green"):
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

def split_into_chunks(text, chunk_size=1500):
    words = text.split()
    chunks = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

def process_chunks(input_file, output_file, model, tokens, temperature):
    text = load_text(input_file)
    chunks = split_into_chunks(text, tokens)

    with ThreadPoolExecutor() as executor:
        responses = list(executor.map(lambda chunk: call_openai_api(chunk, model, temperature), chunks))

    save_to_file(responses, output_file)

def process_text(input_file, output_file, model, temperature, summary=False, interactive=False):
    text = load_text(input_file)
    chunks = split_into_chunks(text)

    with ThreadPoolExecutor() as executor:
        if summary:
            responses = list(executor.map(lambda chunk: call_openai_api_summary(chunk, model, temperature), chunks))
        elif interactive:
            colored_print("Interactive mode: Type your input and press Enter. Type 'exit' to quit.")
            while True:
                user_input = input("> ")
                if user_input.lower() == "exit":
                    break

                chunk = user_input.strip()
                response = call_openai_api(chunk, model, temperature)
                colored_print(f"AI: {response}", "green")
        else:
            responses = list(executor.map(lambda chunk: call_openai_api(chunk, model, temperature), chunks))

        save_to_file(responses, output_file)    

def process_text_summary(input_file, output_file, model, tokens, temperature):
    text = load_text(input_file)
    chunks = split_into_chunks(text, tokens)

    with ThreadPoolExecutor() as executor:
        summaries = list(executor.map(lambda chunk: call_openai_api_summary(chunk, model, temperature), chunks))

    save_to_file(summaries, output_file)

def process_text_interactive(model, tokens, temperature):
    colored_print("Interactive mode: Type your input and press Enter. Type 'exit' to quit.", "green")
    while True:
        user_input = input("> ")
        if user_input.lower() == "exit":
            break

        chunk = user_input.strip()
        response = call_openai_api(chunk, model, temperature)
        colored_print(f"AI: {response}", "green")

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
            colored_print(f"Processed {input_file} -> {output_file}", "green")

def dry_run(input_file, max_tokens):
    text = load_text(input_file)
    chunks = split_into_chunks(text, max_tokens)
    
    colored_print(f"Input text will be split into {len(chunks)} chunks.", "green")
    
    total_tokens = sum(len(chunk) for chunk in chunks)
    api_calls = len(chunks)
    
    colored_print(f"Total tokens to be processed are {total_tokens}.", "green")
    colored_print(f"This will make {api_calls} API calls.\n", "green")
    
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
        colored_print(f"Dry run: Estimated tokens - {total_tokens}", "green")
        colored_print(f"Dry run: Estimated API calls - {api_calls}", "green")
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
        colored_print("Error: Input path is not a valid file or directory", "red")

