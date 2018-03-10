from torch.autograd import Variable
from torch.nn import functional as F
import torch
from torch import nn, optim
import scipy.signal
import scipy.io.wavfile as wavfile
from model import *
import os

def normalize(x):
  return (x - x.mean()) * x.std()

sample_rate, sounds = wavfile.read('input.wav')

_, _, stfted = scipy.signal.stft((sounds.T.astype("float32") / 32768)[0], sample_rate)

spectrogram = torch.from_numpy(stfted.real)

batches = map(lambda x: x.t(), torch.split(spectrogram.t(), 129)[:-1])

is_cuda = torch.cuda.is_available()

model = VAE()

if is_cuda:
  model.cuda()

optimizer = optim.Adam(model.parameters(), lr=1e-3)

# Reconstruction + KL divergence losses summed over all elements and batch
def loss_function(recon_x, x, mu, logvar):
  BCE = F.binary_cross_entropy(recon_x, x.view(-1, 16641), size_average=False)
  
  # see Appendix B from VAE paper:
  # Kingma and Welling. Auto-Encoding Variational Bayes. ICLR, 2014
  # https://arxiv.org/abs/1312.6114
  # 0.5 * sum(1 + log(sigma^2) - mu^2 - sigma^2)
  KLD = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
  
  return BCE + KLD

if os.path.exists("model"):
  model.load_state_dict(torch.load("model"))

model.train()

for data in batches:
  data = Variable(data).contiguous().view(1,129,129)
  if is_cuda:
    data = data.cuda()
  optimizer.zero_grad()
  recon_batch, mu, logvar = model(data)
  loss = loss_function(recon_batch, data, mu, logvar)
  loss.backward()
  optimizer.step()

torch.save(model.state_dict(), "model")