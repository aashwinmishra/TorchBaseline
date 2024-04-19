"""
Takes parameters from user; trains, evaluates and saves model on data.
"""
import torch
import torchvision
import torchvision.transforms as transforms
import torchmetrics
import os
import argparse
from data_setup import get_data, get_dataloaders
from models import TinyVGG
from engine import train
from utils import get_devices, set_seeds, save_model


parser = argparse.ArgumentParser()
parser.add_argument("--url", type=str, default="https://github.com/mrdbourke/pytorch-deep-learning/raw/main/data/pizza_steak_sushi.zip")
parser.add_argument("--num_classes", type=int, default=3)
parser.add_argument("--num_epochs", type=int, default=25)
parser.add_argument("--lr", type=float, default=0.001)
parser.add_argument("--batch_size", type=int, default=64)
args = parser.parse_args()



data_dir = "./Data"
dataset_dir = "Dataset1"
fname = "temp123.zip"
get_data(data_dir, dataset_dir, args.url, fname)
transform = transforms.Compose([transforms.Resize((64,64)), transforms.ToTensor()])
base_dir = os.path.join(data_dir, dataset_dir)
d = get_dataloaders(base_dir, transform, transform, args.batch_size, num_workers=0)
train_dl, val_dl = d["train_dl"], d["val_dl"]

set_seeds(42)
device = get_devices()
model = TinyVGG(n_classes=args.num_classes).to(device)
loss_fn = torch.nn.CrossEntropyLoss()
opt = torch.optim.Adam(model.parameters(), lr=args.lr)
metric = torchmetrics.classification.Accuracy(task="multiclass", num_classes=3).to(device)
results = train(model, train_dl, val_dl, loss_fn, opt, metric, device, args.num_epochs)
save_model("./Models", "model1", model)