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

base = "res50_rensou_out_8"

try:
  os.mkdir(base)
except:
  pass

os.environ["TORCH_MODEL_ZOO"] = "./data"

model = models.resnet50(pretrained=True)
print(model)

def runmodel(input):
  x = model.conv1(input)
  x = model.bn1(x)
  x = model.relu(x)
  x = model.maxpool(x)
  x = model.layer1(x)
  x = model.layer2(x)
  x = model.layer3(x)
  x = model.layer4(x)
  return model.avgpool(x)

model.eval() # turn to test mode

mat = torch.randn(1, 3, 224, 224) / 100
input = nn.Parameter(mat)

optimizer = optim.SGD([input], lr=0.1)
loss_fn = nn.CrossEntropyLoss()

for i in range(0, 100):
  def closure():
    optimizer.zero_grad()
    
    output = runmodel(input)
    
    mat = torch.zeros(1, 2048, 1, 1)
    mat[0][10][0][0] = 1
    target = Variable(mat)
    
    sigmoid = nn.Sigmoid()
    
    loss = (sigmoid(target) - sigmoid(output)).sum()
    loss.backward()
    
    return loss
  
  optimizer.step(closure)
  
  print("%02dfinished" % i)
  
  save_image(input.data, "%s/%02d.png" % (base, i))