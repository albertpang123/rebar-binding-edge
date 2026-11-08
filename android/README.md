# Android application (NCNN)

Real-time detection of rebar binding nodes on an Android phone, using the NCNN
inference framework. Only the application sources are kept here; the NCNN and
OpenCV Mobile SDKs must be downloaded separately.

Built and tested on a Huawei Mate 40 Pro with Android Studio (SDK API 29+,
NDK R22+, CMake).

## 1. Get the SDKs

**NCNN** — download `ncnn-YYYYMMDD-android-vulkan.zip` from
<https://github.com/Tencent/ncnn/releases>, extract it into
`app/src/main/jni/`, and set `ncnn_DIR` in `app/src/main/jni/CMakeLists.txt`
to the package directory for your ABI.

The CMake file shipped here expects:

```
app/src/main/jni/ncnn-20221128-android-vulkan/${ANDROID_ABI}/lib/cmake/ncnn
```

**OpenCV Mobile** — download `opencv-mobile-XYZ-android.zip` from
<https://github.com/nihui/opencv-mobile>, extract it into
`app/src/main/jni/`, and set `OpenCV_DIR` likewise. The CMake file expects
`opencv-4.5.1-android-sdk/sdk/native/jni`.

Neither SDK is committed to this repository.

## 2. Build

Open the `android/` directory in Android Studio, let Gradle sync, and run. The
`jni` build is driven by `app/src/main/jni/CMakeLists.txt`; the APK needs a
device with the `camera2.full` feature (HAL3).

## 3. Model

`app/src/main/assets/rebarbindingfp16.bin` and `.param` are the NCNN FP16
conversion of `weights/yolo11n_rebar_binding.pt`. To use another model, replace
both files and update the model file name and class settings in
`app/src/main/jni/yolo.cpp` (see `yolo.cpp`, the `num_class` and
`class_names[]` entries) and `app/src/main/jni/yolov8ncnn.cpp` (`target_sizes`
and the model name).

## 4. Exporting the model to NCNN

The `.pt` weight file was exported with Ultralytics and then converted:

```python
from ultralytics import YOLO

model = YOLO("weights/yolo11n_rebar_binding.pt")
model.export(format="onnx", opset=12, imgsz=640, simplify=True)
```

Use **opset 12**. Higher opsets (18, 19) produced a `Fatal signal 11` on the
device because of an NCNN operator incompatibility. The ONNX model is then
converted to NCNN with `onnx2ncnn`, and the resulting `.param`/`.bin` pair is
reduced to FP16 storage before being placed in `assets/`.

## Attribution

This application is a modification of the `ncnn-android-yolov8` template by
FeiGeChuanShu. See `NOTICE.md`.
