from torch.utils.data import Dataset, DataLoader
import torch

class TextDataset(Dataset):
    def __init__(self, texts, tokenizer):
        self.tokens = [tokenizer.encode(text) for text in texts]

    def __len__(self):
        return len(self.tokens)

    def __getitem__(self, idx):
        return torch.tensor(self.tokens[idx], dtype=torch.long)

# Example tokenizer function (to be replaced with a real tokenizer)
def simple_tokenizer(text):
    # Dummy implementation
    return text.split()

def get_data_loader(texts, tokenizer, batch_size=32):
    dataset = TextDataset(texts, tokenizer)
    return DataLoader(dataset, batch_size=batch_size, shuffle=True)
