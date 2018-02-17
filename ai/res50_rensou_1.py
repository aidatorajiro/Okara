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

base = "res50_rensou_out_1"

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

im = preprocess(Image.open("./data/test1.jpg"))
im.unsqueeze_(0)

def save(x, f):
  f = base + "/" + f
  tensor = x.data
  if tensor.dim() == 4 and tensor.size(0) == 1:
    save_image(tensor.view(tensor.size(1), tensor.size(0), tensor.size(2), tensor.size(3)), f, padding=0)
  else:
    save_image(tensor, f)

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

input = nn.Parameter(im)

optimizer = optim.LBFGS([input])
loss_fn = nn.CrossEntropyLoss()

for i in range(0, 10):
  def closure():
    optimizer.zero_grad()
    
    output = runmodel(input)
    
    target = Variable(torch.ones(1, 2048, 1, 1))
    
    loss = ((1 - output)**2).sum()
    loss.backward()
    
    return loss
  
  optimizer.step(closure)
  
  print(str(i) + "finished")
  
  save(input, str(i) + ".png")