import torch
import torch.nn as nn
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from torch.autograd import Variable
import torchvision.transforms as transforms

# reading image
# imsize = [512,512] if torch.cuda.is_available() else [128,128] # use small size if no gpu
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

loader = transforms.Compose([
    transforms.ToTensor()])  # transform it into a torch tensor


def image_loader(image_name):
    image = Image.open(image_name)
    # fake batch dimension required to fit network's input dimensions
    image = loader(image).unsqueeze(0)
    return image.to(device, torch.float)


image = image_loader("dancing.jpg")


# compute image gradient
def gradient_img(img):
    img = img.squeeze(0)
    ten = torch.unbind(img)
    x = ten[0].unsqueeze(0).unsqueeze(0)

    a = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
    conv1 = nn.Conv2d(1, 1, kernel_size=3, stride=1, padding=1, bias=False)
    conv1.weight = nn.Parameter(torch.from_numpy(a).float().unsqueeze(0).unsqueeze(0))
    G_x = conv1(Variable(x)).data.view(1, x.shape[2], x.shape[3])

    b = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
    conv2 = nn.Conv2d(1, 1, kernel_size=3, stride=1, padding=1, bias=False)
    conv2.weight = nn.Parameter(torch.from_numpy(b).float().unsqueeze(0).unsqueeze(0))
    G_y = conv2(Variable(x)).data.view(1, x.shape[2], x.shape[3])

    G = torch.sqrt(torch.pow(G_x, 2) + torch.pow(G_y, 2))
    return G


grad = gradient_img(image)

# plotting
unloader = transforms.ToPILImage()  # reconvert into PIL image

plt.ion()


def imshow(tensor, title=None):
    image = tensor.cpu().clone()  # we clone the tensor to not do changes on it
    image = image.squeeze(0)  # remove the fake batch dimension
    image = unloader(image)
    plt.imshow(image)
    if title is not None:
        plt.title(title)
    plt.pause(0.001)  # pause a bit so that plots are updated


plt.figure()
imshow(image, title='Original Image')
imshow(grad, title='Edges identified')