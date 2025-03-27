# NOT WORKING
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("OpenLLM-Ro/RoLlama2-7b-Chat")
model = AutoModelForCausalLM.from_pretrained("OpenLLM-Ro/RoLlama2-7b-Chat")

instruction = "Care este cel mai înalt vârf muntos din România?"
chat = [
        {"role": "system", "content": "Ești un asistent folositor, respectuos și onest. Încearcă să ajuți cât mai mult prin informațiile oferite, excluzând răspunsuri toxice, rasiste, sexiste, periculoase și ilegale."},
        {"role": "user", "content": instruction},
        ]
prompt = tokenizer.apply_chat_template(chat, tokenize=False)

inputs = tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")
outputs = model.generate(input_ids=inputs, max_new_tokens=128)
print(tokenizer.decode(outputs[0]))

# @misc{masala2024openllmrotechnicalreport,
#       title={OpenLLM-Ro -- Technical Report on Open-source Romanian LLMs}, 
#       author={Mihai Masala and Denis C. Ilie-Ablachim and Dragos Corlatescu and Miruna Zavelca and Marius Leordeanu and Horia Velicu and Marius Popescu and Mihai Dascalu and Traian Rebedea},
#       year={2024},
#       eprint={2405.07703},
#       archivePrefix={arXiv},
#       primaryClass={cs.CL},
#       url={https://arxiv.org/abs/2405.07703}, 
# }
