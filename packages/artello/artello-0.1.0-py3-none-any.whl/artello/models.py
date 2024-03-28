import torch
import torch.nn as nn

class NanoLM(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim):
        super(NanoLM, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.rnn = nn.LSTM(embedding_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, vocab_size)
    
    def forward(self, x):
        x = self.embedding(x)
        output, (hidden, cell) = self.rnn(x)
        x = self.fc(output)
        return x
