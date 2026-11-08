# Rebar Binding Detection and Edge Deployment Using YOLO

Code, trained weights and training logs accompanying the paper *Rebar Binding
Detection and Edge Deployment Using YOLO*.

The detector is a single-class (bound node) YOLO11n model trained on rebar mesh
photographs. It is deployed on two edge targets: an Android smartphone through
NCNN, and a Seeed Studio reCamera 2002 through its Sophgo TPU.

## What is in this repository

| Path | Contents |
|---|---|
| `train/runs/` | `args.yaml` and `results.csv` of each training run (seven runs: YOLO11n at 250 and 500 epochs, YOLO11s, YOLO11m, YOLOv8n, YOLOv8m, and the three-class ablation) |
| `train/train.py` | Training entry point reproducing the settings in `train/runs/g42_yolo11n_e500/args.yaml` |
| `train/data_group42.yaml` | Dataset descriptor for the group split (paths must be edited before use) |
| `weights/yolo11n_rebar_binding.pt` | Trained YOLO11n weights (5.24 MiB) |
| `android/` | Android application built on the `ncnn-android-yolov8` template |
| `android/app/src/main/assets/` | The same model converted to NCNN FP16 (`rebarbindingfp16.bin` / `.param`) |

The `rebarbindingfp16.bin` file is 6,022,696 bytes (5.74 MiB).

## Training

The dataset is described in Section 2.1 of the paper: 677 source photographs,
expanded to 3,388 images by the Roboflow augmentation pipeline, and split
70:15:15 **by source photograph** rather than by augmented file, so that no
scene appears in more than one split. The split yields 474 / 102 / 101 source
photographs, of which all 2,354 augmented copies of the training photographs
are used and one image per photograph is used for validation and test.

```bash
pip install ultralytics==8.3.163
python train/train.py
```

Edit `path` in `train/data_group42.yaml` first. Training was run on an NVIDIA
GeForce RTX 4080 Laptop GPU (12 GB VRAM) with PyTorch 2.6.0 / CUDA 12.4, batch
size 16, `imgsz=640`, `cache=ram`, 8 workers, patience 100, seed 0.

The dataset itself is **not** distributed here; see *Dataset availability*.

## Android application

`android/` contains only the application sources. The NCNN and OpenCV Android
SDKs it links against are not included: follow `android/README.md` to download
them and place them under `android/app/src/main/jni/`.

The application is a modification of the open-source
[`ncnn-android-yolov8`](https://github.com/FeiGeChuanShu/ncnn-android-yolov8)
template; see `android/NOTICE.md` for attribution.

## reCamera deployment

The reCamera accepts neither `.pt` nor `.onnx` models. Conversion to
`cvimodel` was carried out with the `tpu-mlir` toolchain driven by a project
that is not part of this repository. The route used is: export the trained
model to ONNX (opset 12, `imgsz=640`, `simplify=True`), compile the ONNX graph
to MLIR with `tpu-mlir`, and quantise to INT8 or FP16. On-device inference and
the Node-RED counting dashboard are configured inside the reCamera's own
workspace and are not included either.

## Dataset availability

The source photographs are of two kinds, and neither is redistributed here:

- Images from four public Roboflow Universe datasets, cited as [12]–[15] in the
  paper. They remain available at those sources under their own licences.
- Frames extracted from on-site video supplied by a construction partner.
  These depict a commercial site and cannot be released.

Requests for the annotated dataset should be addressed to the corresponding
author and are subject to the partner's approval.

## Licence

No licence is declared for this repository as a whole at present.

Third-party components keep their own terms:

- `android/` derives from the `ncnn-android-yolov8` template and from
  [ncnn](https://github.com/Tencent/ncnn); see `android/NOTICE.md`.
- The trained weights derive from Ultralytics YOLO11 checkpoints, distributed
  by Ultralytics under AGPL-3.0.

## Citation

If you use this code, please cite the paper (bibliographic details to be added
on publication).
