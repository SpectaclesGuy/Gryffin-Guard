import torch
from ultralytics import YOLO

def main():
    torch.cuda.set_device(0)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Create a new YOLO model from scratch
    model = YOLO("yolo11n.pt")
    model.to(device=device)
    
    # Train the model
    results = model.train(data="confg.yaml", epochs=200)
    metrics = model.val()

if __name__ == '__main__':
    main()
