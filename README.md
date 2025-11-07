# 📏 Object Volume Measurement using ArUco Marker

> **A modular computer vision system for real-world object size and volume measurement**  
> Built with OpenCV 4.10+, designed for use in Jupyter Notebook or standalone Python scripts.  
> Automatically calibrates scale using an **ArUco marker**, estimates **object dimensions and volume**,  
> and logs results with timestamps to `.csv` files.


## 🧩 Features
- ✅ **Automatic calibration** using ArUco markers  
- ✅ **Fallback mode** when the marker is not visible  
- ✅ **Real-time volume estimation** based on contour diameter slicing (Bai et al., 2006 model)  
- ✅ **Modular function design** for easy testing and maintenance  
- ✅ **CSV logging** with timestamps per measurement  
- ✅ **Error margin estimation** (weighted width/height deviation model)


## 🗂️ Project Structure

``` text
object_volume_measurement/
│
├── notebooks/
│   └── object_measurement.ipynb       # Main notebook
│
├── assets/
│   └── video2.mp4                     # sample input video
│   └── Image10.jpg                    # sample input image
│   └── ArUco Marker.pdf               # AruCo Marker
│   └── aruco.png                      # AruCo Marker
│
└── README.md
```


## ⚙️ Prerequisites

### 1️⃣ System Requirements
- Python **≥ 3.9**
- OpenCV **≥ 4.7.0** (supports `cv2.aruco.ArucoDetector`)
- Jupyter Notebook (optional, for research workflow)
- Webcam or video input file

### 2️⃣ Recommended Hardware
- A **printed ArUco marker** (DICT_4X4_50, ID=0)
  - Size: **5.0 × 5.0 cm**
  - Paper: Matte recommended for less glare
- A **flat surface** with even lighting



## 🧠 Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/object_volume_measurement.git
cd object_volume_measurement
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Used Main Libraries Version
```text
opencv-python>=4.10.0
numpy>=1.24.0
```



## 🚀 Usage

1. Launch Jupyter:

   ```bash
   jupyter notebook
   ```
2. Open `notebooks/object_measurement.ipynb`
3. Run all cells (Shift + Enter)
4. A live video window will open — press **Q** to quit.


## 🧪 Configuration Options

Inside the code or notebook, you can adjust key parameters:

| Parameter              | Description                                    | Default               |
| ---------------------- | ---------------------------------------------- | --------------------- |
| `use_webcam`           | Use live webcam (True) or video file           | `True`                |
| `video_path`           | Path to video file if `use_webcam=False`       | `"assets/video2.mp4"` |
| `marker_id_local`      | ArUco marker ID to detect                      | `0`                   |
| `marker_size_cm_local` | Physical printed marker size (in cm)           | `5.0`                 |
| `reference_width_cm`   | Fallback width reference if marker lost        | `4.0`                 |
| `reference_height_cm`  | Fallback height reference if marker lost       | `2.1`                 |
| `soft_mode`            | Continue using last-known scale if marker lost | `True`                |



## 📊 Output

### 1️⃣ Real-Time Display

The system overlays:

* **Blue box:** ArUco marker
* **Green box:** Object bounding rectangle
* **Width, height, volume:** live on-screen
* **Margin of error (%):** computed in real time

### 2️⃣ CSV File Logging

Automatically generated file on "data" folder:

```
data/Object Measurement_{timestamp}.csv
```

Columns:

Got it ✅ — you want the **CSV data (from your code output)** to be shown in a **Markdown table format** like your earlier one, so it’s readable in documentation or notebooks.

Here’s your adapted version 👇

---

### 📄 Example Measurement Data (No Marker | Marker Detected | Marker was Detected)

| Timestamp           | Frame Index | Marker Status                    | cm/pixel | Width (cm) | Height (cm) | Volume (cm³) | Margin of Error (%) |
| ------------------- | ----------- | -------------------------------- | -------- | ---------- | ----------- | ------------ | ------------------- |
| 2025-11-07 22:54:50 | 108         | No marker - using reference size | 0.005313 | 2.922      | 2.550       | 2.948        | 7.724               |
| 2025-11-07 22:54:51 | 130         | Marker OK (ID 0)                 | 0.070974 | 31.441     | 33.783      | 8061.351     | 23.937              |
| 2025-11-07 22:55:10 | 550         | Marker lost - using last scale   | 0.031759 | 16.356     | 10.957      | 240.351      | 3.795               |


## 📏 ArUco Marker Printing

1. Use OpenCV to generate one or download from [https://chev.me/arucogen/](https://chev.me/arucogen/)
2. Select:

   * Dictionary: **4x4 (50)**
   * Marker ID: **0**
3. Print size: **5.0 × 5.0 cm**

Place the marker near your object on a flat surface.



## 🧮 Error Model

The system estimates error using a **weighted RMS deviation** between measured and known physical size:

$$
E_{total} = \sqrt{0.7 \times \Delta W^2 + 0.3 \times \Delta H^2}
$$

Where:
$$
* ( \Delta W = \frac{|W_{measured} - W_{true}|}{W_{true}} \times 10 )
* ( \Delta H = \frac{|H_{measured} - H_{true}|}{H_{true}} \times 10 )
$$

This model empirically scales error for compact, camera-based measurement setups.




## References

Method adapted from:

> Bai, Y., et al. (2006). “Automatic measurement of bread volume by computer vision.”
> *Journal of Food Engineering, 77(3), 557–563.*
>https://www.researchgate.net/publication/263011656_Volume_Measurement_Algorithm_for_Food_Product_with_Irregular_Shape_using_Computer_Vision_based_on_Monte_Carlo_Method