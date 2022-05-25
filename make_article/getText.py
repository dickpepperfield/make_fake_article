from transformers import TFGPT2LMHeadModel, GPT2Tokenizer
import tensorflow as tf

def createGPT2Text(loadTitle):
    # GPT2 Stuff
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    GPT2 = TFGPT2LMHeadModel.from_pretrained("gpt2", pad_token_id=tokenizer.eos_token_id)
    # Input is random title from above, generate text using tensorflow
    input_sequence = loadTitle
    input_ids = tokenizer.encode(input_sequence, return_tensors='tf')
    sample_output = GPT2.generate(
                             input_ids,
                             do_sample = True,
                             max_length = GPT_MAX_LEN,
                             top_k = 0,
                             temperature = 0.8
    )
    # Output here
    GPT2Output = tokenizer.decode(sample_output[0], skip_special_tokens = True)

    return GPT2Output