import model


def train():
    file = open("text.txt", 'r')
    text = file.read()
    model.n_model(text)

