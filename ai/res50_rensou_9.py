import torch
import torchvision
from torchvision.utils import *
import torchvision.models as models
import torchvision.transforms as transforms
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import os
from PIL import Image

base = "res50_rensou_out_9"

try:
  os.mkdir(base)
except:
  pass

os.environ["TORCH_MODEL_ZOO"] = "./data"

model = models.resnet50(pretrained=True)
print(model)

model.eval() # turn to test mode

input = nn.Parameter(torch.randn(1, 3, 224, 224) / 10)

optimizer = optim.SGD([input], lr=10)
loss_fn = nn.CrossEntropyLoss()

target = Variable(torch.LongTensor([10]))

for i in range(0, 100):
  def closure():
    optimizer.zero_grad()
    
    output = model(input)
    
    loss = loss_fn(output, target)
    loss.backward()
    
    return loss
  
  optimizer.step(closure)
  
  print("%02dfinished" % i)
  
  save_image(input.data, "%s/%02d.png" % (base, i))