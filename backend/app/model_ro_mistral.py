# NOT WORKING
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("OpenLLM-Ro/RoMistral-7b-Instruct-DPO")
model = AutoModelForCausalLM.from_pretrained("OpenLLM-Ro/RoMistral-7b-Instruct-DPO")

instruction = "Ce jocuri de societate pot juca cu prietenii mei?"
chat = [
        {"role": "user", "content": instruction},
        ]
prompt = tokenizer.apply_chat_template(chat, tokenize=False, system_message="")

inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, return_attention_mask=True)
outputs = model.generate(
    input_ids=inputs["input_ids"],
    attention_mask=inputs["attention_mask"],
    max_new_tokens=64,
    do_sample=True,
    temperature=0.7,
    top_p=0.9,
    eos_token_id=tokenizer.eos_token_id
)

#print(tokenizer.decode(outputs[0]))

response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(response.replace(prompt, "").strip())
