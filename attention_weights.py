outputs = model(**inputs, output_attentions=True)
attentions = outputs.attentions
last_layer_attn = attentions[-1]
important_tokens = torch.topk(last_layer_attn.mean(dim=1), k=10)  # Top 10 most focused tokens
