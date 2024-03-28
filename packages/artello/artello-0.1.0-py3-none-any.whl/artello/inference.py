def make_prediction(model, input_text, tokenizer):
    model.eval()
    tokens = tokenizer.encode(input_text)
    with torch.no_grad():
        predictions = model(tokens)
    # Process predictions to return human-readable format
    return predictions
