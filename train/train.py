"""Train the single-class rebar binding detector.

Reproduces the run recorded in train/runs/g42_yolo11n_e500/args.yaml.
Requires ultralytics==8.3.163 (PyTorch 2.6.0 / CUDA 12.4 in the paper).

Edit `path` in data_group42.yaml before running, then:

    python train/train.py
"""
from pathlib import Path

from ultralytics import YOLO

ROOT = Path(__file__).resolve().parent


def main():
    model = YOLO("yolo11n.pt")          # Ultralytics pretrained checkpoint
    model.train(
        data=str(ROOT / "data_group42.yaml"),
        epochs=500,
        patience=100,
        batch=16,
        imgsz=640,
        cache="ram",
        workers=8,
        seed=0,
        amp=True,
        project=str(ROOT / "runs"),
        name="g42_yolo11n_e500",
    )


if __name__ == "__main__":
    # required on Windows: without it the DataLoader re-imports this module in
    # every worker and spawns processes recursively
    main()
