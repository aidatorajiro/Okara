import torch
from torch import nn
from torch.autograd import Variable
from model import *
import os
from torchvision.utils import save_image
import scipy.signal
import scipy.io.wavfile as wavfile

sample_rate = 44100

model = VAE()

is_cuda = torch.cuda.is_available()

if is_cuda:
  model.cuda()

if os.path.exists("model"):
  model.load_state_dict(torch.load("model"))

model.eval()

sample = Variable(torch.randn(10, 400))

if is_cuda:
  sample = sample.cuda()

sample = model.decode(sample).cpu()

for i, x in enumerate(sample):
  _, wave = scipy.signal.istft(x.data.view(129, 129).numpy(), 44100)
  wavfile.write("output/%s.wav" % i, 44100, wave)