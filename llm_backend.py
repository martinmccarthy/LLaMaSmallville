import torch
from transformers import MllamaForConditionalGeneration, AutoProcessor
from PIL import Image

model_id = "meta-llama/Llama-3.2-11B-Vision-Instruct"

model = MllamaForConditionalGeneration.from_pretrained(model_id, device_map=0, torch_dtype=torch.bfloat16)
processor = AutoProcessor.from_pretrained(model_id)

def create_agent_prompt():
    prompt = """Describe this person to me:"""

    user_prompt = {
        "role": "user",
        "content": [
            { "type": "text", "text": prompt},
            { "type": "image",}
        ]
    }

    return [
        [user_prompt],
    ]

def run_conversation(current_image_path):
    current_image = Image.open(current_image_path).resize((256, 256))

    messages = create_agent_prompt()
    text = processor.apply_chat_template(messages, add_generation_prompt=True)
    inputs = processor(text=text, images=current_image, return_tensors="pt").to(model.device)

    outputs = model.generate(**inputs, max_new_tokens=28000)
    
    response = processor.decode(outputs[0][inputs["input_ids"].shape[-1]:])
    response = response.replace("<|eot_id|>", "")
    return response
