def train_model(model, data_loader, optimizer, criterion, epochs=10):
    model.train()
    for epoch in range(epochs):
        for inputs in data_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, inputs)
            loss.backward()
            optimizer.step()
        print(f'Epoch {epoch+1}, Loss: {loss.item()}')
