import os 
import json 
import sys 
import threading
import random
import time 
import requests
import inspect


def spinner():
    # ANSI escape codes for colors
    colors = [
    '\033[91m',  # Red
    '\033[92m',  # Green
    '\033[93m',  # Yellow
    '\033[94m',  # Blue
    '\033[95m',  # Purple
    '\033[96m',  # Cyan
    ]
    # Reset color to default
    reset_color = '\033[0m'
    
    
    spin_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    spin_chars = "⠁,⠁,⠉,⠙,⠚,⠒,⠂,⠂,⠒,⠲,⠴,⠤,⠄,⠄,⠤,⠠,⠠,⠤,⠦,⠖,⠒,⠐,⠐,⠒,⠓,⠋,⠉,⠈,⠈".split(',')
    # spin_chars = "◰ ◳ ◲ ◱".split(' ')
    offset = 15
    while True:
        for i in range(len(spin_chars)):
            color = random.choice(colors)
            chars = " ".join([spin_chars[(i+j+2)%len(spin_chars)] for j in range(offset)])
            sys.stdout.write('\r' + color + chars + reset_color)
            
            sys.stdout.flush()
            time.sleep(0.03)
        if not spinner_active:
            break
    sys.stdout.write('\r ')

def ask_llm(messages, model = "gpt-4o"): 

    global spinner_active 

    spinner_active = True
    thread = threading.Thread(target=spinner)
    thread.start()

    start = time.time()
    model_answer = openai_ask_requests(messages, model)
    duration = time.time() - start

    spinner_active = False
    thread.join()

    max_spacing = 50
    try: 
        called_by = inspect.stack()[2][3]
    except:
        called_by = "unknown"
    try:
        called_by_by = inspect.stack()[3][3]
    except:
        called_by_by = "unknown"

    to_print = [["Model", f"{model.upper()}"], 
    #             ["Called by", called_by],
    #             ["Called by by", called_by_by],
    #             ["Input tokens", f"{call_recap['in_tokens']}"], 
    #             ["Output tokens", f"{call_recap['out_tokens']}"],
                ["Gen time", "{:.2f}".format(duration)]]
                # ["Tokens/sec","{:.2f}".format(call_recap['out_tokens']/duration)]]
    to_print_formatted = "\n".join([""] + ["{} {} {}".format(p[0], '.'*(max_spacing - (len(p[0]) + len(p[1]))), p[1]) for p in to_print] + [""])

    cprint(to_print_formatted, [120,120,120])
    return model_answer

def cprint(text, color_list, end='\n'): 
    print_rgb_text(color_list[0], color_list[1], color_list[2], text, end=end)


def print_rgb_text(r, g, b, text, end='\n'):
    """
    Print text in a custom color specified by RGB values.
    """
    # ANSI escape code for 24-bit color
    escape_code = f"\x1b[38;2;{r};{g};{b}m"
    reset_code = "\x1b[0m"  # ANSI code to reset to default color
    print(f"{escape_code}{text}{reset_code}", end=end)



def openai_ask_requests(messages, model, image_path = None):

    url = f"https://cld.akkodis.com/api/openai/deployments/models-{model}/chat/completions?api-version=2024-12-01-preview"
    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        # "api-key": open(os.path.join(os.path.expanduser('~'), ".akr_key.txt"), 'r').read().strip()
        "api-key": "METTRE LA CLÉ ICI"
    }


    # messages = handle_image(messages, image_path)

    data = {
        "temperature": 0.,
        "top_p": 1,
        "stream": False,
        # "stop": None,
        "max_tokens": 4096,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "logit_bias": {},
        "user": "user",
        "messages": messages,
        "n": 1,
        "seed": 0,
        "response_format": {
            "type": "text"
        }
    }

    response = requests.post(url, headers=headers, json=data).json()
    # call_recap = {"in_tokens": response['usage']['prompt_tokens'],
    #               "out_tokens": response['usage']['completion_tokens'], 
    #     }
    
    return response['choices'][0]['message']['content']


if __name__ == "__main__": 
    
    messages = [{"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"}]
    
    
    print(ask_llm(messages, model = "gpt-4o"))