# Attribution and provenance

The Android application in this directory is a modification of an existing
open-source project. It is included here so that the results in the paper can
be reproduced, not as an original work.

## Upstream

| | |
|---|---|
| Project | `ncnn-android-yolov8` — "Real time yolov8 Android demo by ncnn" |
| Author | FeiGeChuanShu |
| Source | https://github.com/FeiGeChuanShu/ncnn-android-yolov8 |
| Licence | No licence file is declared in the upstream repository |

That project is itself a sample built on top of two libraries:

| | |
|---|---|
| ncnn | Copyright (C) 2017 THL A29 Limited, a Tencent company. BSD-3-Clause. https://github.com/Tencent/ncnn |
| opencv-mobile | Copyright (C) 2019 Ni Hui. Apache-2.0. https://github.com/nihui/opencv-mobile |

The upstream README additionally credits
[`ncnn-android-nanodet`](https://github.com/nihui/ncnn-android-nanodet) and the
[Ultralytics assets release](https://github.com/ultralytics/assets/releases).

## What was changed

The application sources are reproduced here with the following modifications,
made to run a custom single-class rebar binding model:

- `app/src/main/jni/yolo.cpp` — class names, class count, output tensor
  dimensions and `target_size` adjusted for the single-class model.
- `app/src/main/jni/yolov8ncnn.cpp` — model name in `assets`, same adjustments
  as above for the second inference path.
- `app/src/main/jni/CMakeLists.txt` — paths to the NCNN and OpenCV Mobile
  package directories.
- `app/src/main/assets/` — the upstream demo models replaced by
  `rebarbindingfp16.bin` and `rebarbindingfp16.param`.
- `app/src/main/res/` and `app/src/main/java/` — application name and the
  on-screen FPS display.

Two source-level changes were needed for the custom model to load at all, and
are described in Section 4 of the paper: ONNX export at opset 12 (higher opsets
triggered a `Fatal signal 11` on Android because of NCNN operator
incompatibility), and manual adjustment of the output dimensions.

## Notice

The upstream project declares no licence. All rights in the original code
remain with its author. This copy is redistributed for academic reproducibility
only; anyone reusing it should obtain the original from the upstream URL above.
