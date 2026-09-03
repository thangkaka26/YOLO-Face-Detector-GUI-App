from ultralytics import YOLO

def training_model():
    model = YOLO("yolov8n.pt")

    history = model.train(
        data="data/data.yaml",
        epochs=5,
        batch=4,
        device=0,
        workers=8,
        imgsz=640
    )

if __name__ == "__main__":
    training_model()