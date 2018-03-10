import torch
from torch import nn
from torch.autograd import Variable

class VAE(nn.Module):
    def __init__(self):
        super(VAE, self).__init__()

        self.fc1 = nn.Linear(16641, 1000)
        self.fc21 = nn.Linear(1000, 400)
        self.fc22 = nn.Linear(1000, 400)
        self.fc3 = nn.Linear(400, 1000)
        self.fc4 = nn.Linear(1000, 16641)

        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()

    def encode(self, x):
        h1 = self.relu(self.fc1(x))
        return self.fc21(h1), self.fc22(h1)

    def reparameterize(self, mu, logvar):
        if self.training:
            std = logvar.mul(0.5).exp_()
            eps = Variable(std.data.new(std.size()).normal_())
            return eps.mul(std).add_(mu)
        else:
            return mu

    def decode(self, z):
        h3 = self.relu(self.fc3(z))
        return self.sigmoid(self.fc4(h3))

    def forward(self, x):
        mu, logvar = self.encode(x.view(-1, 16641))
        z = self.reparameterize(mu, logvar)
        return self.decode(z), mu, logvar
