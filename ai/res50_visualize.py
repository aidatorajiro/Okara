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

try:
  os.mkdir("./res50_visualize_out/")
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
  f = "./res50_visualize_out/" + f
  tensor = x.data
  if tensor.dim() == 4 and tensor.size(0) == 1:
    save_image(tensor.view(tensor.size(1), tensor.size(0), tensor.size(2), tensor.size(3)), f, padding=0)
  else:
    save_image(tensor, f)

model.eval() # turn to test mode

# run model
x = Variable(im)
save(x, "in.jpg")

x = model.conv1(x)
save(x, "conv1.jpg")

x = model.bn1(x)
save(x, "bn1.jpg")

x = model.relu(x)
save(x, "relu.jpg")

x = model.maxpool(x)
save(x, "maxpool.jpg")

x = model.layer1(x)
save(x, "layer1.jpg")

x = model.layer2(x)
save(x, "layer2.jpg")

x = model.layer3(x)
save(x, "layer3.jpg")

x = model.layer4(x)
save(x, "layer4.jpg")

x = model.avgpool(x)
save(x, "avgpool.jpg")

x = x.view(x.size(0), -1)
save(x, "vs.jpg")

x = model.fc(x)
save(x, "fc.jpg")

c = x.data.numpy().argmax()

print(c) # returns 94, hummingbird