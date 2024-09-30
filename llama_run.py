import transformers
import torch
from transformers import AutoTokenizer

model = "meta-llama/Llama-3.2-1B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model)
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    torch_dtype=torch.float16,
    device_map=0,
    return_full_text=False,
)

roles = ["Chef", "Farmer"]

def create_agent_prompt(agent_role, conversation_history):
    sys_prompt = {
        "role": "system",
        "content": f"""You are role-playing as {agent_role} in an ongoing conversation. Your job is to provide contextually appropriate responses based on the conversation history. Each response must start with '{agent_role}:', followed by your dynamic reply. 

        Do not repeat any previous responses verbatim. Respond only to the most recent message, and make sure your responses reflect the personality and context of your role.

        Examples:

        Example 1:
        User: 'Chef: Hello, how are you today?'
        Expected Response: '{agent_role}: I am doing well, thank you! How is your cooking coming along?'

        Example 2:
        User: 'Farmer: The crops are looking great! What do you think of the new irrigation system?'
        Expected Response: '{agent_role}: The new irrigation system sounds like a game-changer for the harvest. I would love to see how it works.'

        Example 3:
        User: 'Student: Could you help me with the math assignment?'
        Expected Response: '{agent_role}: Absolutely! What topic are you struggling with the most?'

        Make sure your response continues the conversation based on the context. Do not repeat yourself, and make each response unique and relevant to the dialogue so far.
        """
    }

    conversation_text = "\n".join([f"{entry['text']}" for entry in conversation_history])
    user_prompt = {
        "role": "user",
        "content": conversation_text,
    }

    print(conversation_text)

    return [sys_prompt, user_prompt]




def run_conversation(agent_role, conversation_history):
    messages = create_agent_prompt(agent_role, conversation_history)
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    
    sequences = pipeline(
        prompt,
        max_new_tokens=128,
        do_sample=True,
        pad_token_id=pipeline.tokenizer.eos_token_id
    )
    
    return sequences[0]["generated_text"]

starter_convo = "Hello, how are you today?"
conversation = [{"text": starter_convo, "agent": "undefined"}]  # Entire conversation history

import tkinter as tk

wrap_length = 300  

root = tk.Tk()
root.title("Chef and Farmer")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

chef_label = tk.Label(frame, text="Chef", font=("Arial", 16))
farmer_label = tk.Label(frame, text="Farmer", font=("Arial", 16))

chef_label.grid(row=0, column=0, padx=10, pady=10)
farmer_label.grid(row=0, column=1, padx=10, pady=10)

chef_button = tk.Button(frame, text="Send Message from Chef", command=lambda: have_convo("Chef"))
farmer_button = tk.Button(frame, text="Send Message from Farmer", command=lambda: have_convo("Farmer"))

chef_button.grid(row=1, column=0, padx=10, pady=10)
farmer_button.grid(row=1, column=1, padx=10, pady=10)

chef_row_counter = 2
farmer_row_counter = 2

def have_convo(agent_role):
    global chef_row_counter, farmer_row_counter

    if len(conversation) == 1:
        conversation[0]["text"] = agent_role + ": " + starter_convo
        conversation[0]["agent"] = agent_role
        
    convo = run_conversation("Farmer" if agent_role == "Chef" else "Chef", conversation)
    conversation.append({"text": convo, "agent": "Farmer" if agent_role == "Chef" else "Chef"})

    if agent_role == "Chef":
        if len(conversation) == 2:
            chef_convo_label = tk.Label(frame, text=conversation[0]["text"], wraplength=wrap_length)
            chef_convo_label.grid(row=chef_row_counter, column=0, padx=10, pady=5)
            chef_row_counter += 1

        farmer_convo_label = tk.Label(frame, text=convo, wraplength=wrap_length)
        farmer_convo_label.grid(row=farmer_row_counter, column=1, padx=10, pady=5)
        farmer_row_counter += 1
    else:
        if len(conversation) == 2:
            farmer_convo_label = tk.Label(frame, text=conversation[0]["text"], wraplength=wrap_length)
            farmer_convo_label.grid(row=farmer_row_counter, column=1, padx=10, pady=5)
            farmer_row_counter += 1
        
        chef_convo_label = tk.Label(frame, text=convo, wraplength=wrap_length)
        chef_convo_label.grid(row=chef_row_counter, column=0, padx=10, pady=5)
        chef_row_counter += 1
root.mainloop()
