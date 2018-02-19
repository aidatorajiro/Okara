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

base = "res50_rensou_out_5b"

try:
  os.mkdir(base)
except:
  pass

os.environ["TORCH_MODEL_ZOO"] = "./data"

model = models.resnet50(pretrained=True)
print(model)

preprocess = transforms.Compose([
  lambda x: x.convert('RGB'),
  transforms.Resize((224, 224)),
  transforms.ToTensor()
])

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
mat[0][0][112][112] = 1
mat[0][0][113][112] = 1
mat[0][0][112][113] = 1
mat[0][0][113][113] = 1
mat[0][1][112][112] = 1
mat[0][1][113][112] = 1
mat[0][1][112][113] = 1
mat[0][1][113][113] = 1

input = nn.Parameter(mat)

optimizer = optim.SGD([input], lr=0.1)
loss_fn = nn.CrossEntropyLoss()
sigmoid = nn.Sigmoid()

for i in range(0, 100):
  def closure():
    optimizer.zero_grad()
    
    output = runmodel(input)
    
    loss = (1 - sigmoid(output)**4).sum()
    loss.backward()
    
    return loss
  
  optimizer.step(closure)
  
  print("%02dfinished" % i)
  
  save_image(input.data, "%s/%02d.png" % (base, i))