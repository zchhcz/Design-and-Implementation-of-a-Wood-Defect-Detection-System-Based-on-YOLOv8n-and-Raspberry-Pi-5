# YOLOv8n 木材缺陷检测系统 (Raspberry Pi 5)

基于 YOLOv8n 和树莓派 5 的实时木材缺陷检测系统，支持本地推理与数据远程传输。

![系统演示](https://github.com/user-attachments/assets/5e937bec-64b2-4c83-8ba8-24a2956c9042)

---

## 📋 目录

- [项目简介](#项目简介)
- [功能特性](#功能特性)
- [硬件要求](#硬件要求)
- [快速开始](#快速开始)
- [模型训练](#模型训练)
- [部署指南](#部署指南)
  - [树莓派端部署](#树莓派端部署)
  - [主机端部署](#主机端部署)
- [使用说明](#使用说明)
- [项目结构](#项目结构)
- [常见问题](#常见问题)
- [联系方式](#联系方式)

---

## 项目简介

本项目是一个基于 YOLOv8n 轻量级目标检测模型和树莓派 5 的木材缺陷检测系统。系统通过树莓派连接摄像头采集图像，在本地进行推理后，将检测结果和图像实时传输至局域网内的主机端，便于数据存储、可视化和后续分析。

该系统可应用于木材加工厂流水线，帮助减轻人工检测的工作强度，提高检测效率和一致性。

> **注**：这是本人上传到 GitHub 的第一个项目，本科毕设级水准！还有很大的提升空间，欢迎交流！

---

## 功能特性

### 树莓派端
- ✅ 支持多种摄像头输入（Picamera2、USB摄像头）
- ✅ 基于 NCNN 格式模型推理，轻量高效
- ✅ 实时缺陷检测与本地显示
- ✅ 检测数据与图像远程传输
- ✅ 断线自动重连机制
- ✅ 支持图像压缩传输，节省带宽

### 主机端
- ✅ PyQt5 图形化界面
- ✅ 实时接收并显示检测画面
- ✅ 检测数据本地存储（图片 + JSON）
- ✅ 数据增删改查管理
- ✅ 检测统计与可视化
- ✅ 本地推理功能（可选）
- ✅ 提供已打包的 EXE 可执行文件

---

## 硬件要求

| 设备 | 推荐配置 |
|------|---------|
| 树莓派 | Raspberry Pi 5 (4GB/8GB) |
| 摄像头 | IMX219 / IMX477 / 兼容 USB 摄像头 |
| 主机 | Windows/Linux，任意配置 |
| 网络 | 局域网环境（WiFi/以太网） |

---

## 快速开始

### 1. 准备工作
确保你的树莓派和主机在同一局域网内，树莓派已烧录好系统并配置网络。

### 2. 快速部署步骤
1. 克隆本项目
2. 按照[部署指南](#部署指南)配置环境
3. 启动主机端服务器
4. 运行树莓派端检测程序
5. 开始检测！

---

## 模型训练

### 1. 数据集准备

#### 数据集来源
可以从以下平台获取木材缺陷相关数据集：
- **Kaggle**：搜索 "wood defect"、"wood surface" 等关键词
- **Roboflow**：已有多个公开木材检测数据集
- **数据集示例**：
  - 木材表面缺陷检测
  - 实木板材缺陷检测
  - 木材品质分类

#### 常见木材缺陷类型
| 缺陷类型 | 描述 |
|---------|------|
| 虫眼 | 木材被昆虫蛀蚀形成的孔洞 |
| 裂缝 | 木材干裂或外力导致的开裂 |
| 腐朽 | 木材受真菌侵蚀变质 |
| 变色 | 木材颜色异常变化 |
| 木节 | 树木生长过程中形成的结节 |
| 划痕 | 加工过程中产生的表面划伤 |

#### 数据格式转换
将数据集转换为 YOLO 格式：
```
dataset/
├── images/
│   ├── train/
│   ├── val/
│   └── test/
└── labels/
    ├── train/
    ├── val/
    └── test/
```

#### 数据增强建议
- 随机裁剪、翻转
- 亮度、对比度调整
- 添加噪声模拟工业环境
- 混合拼接增强

### 2. 训练配置

创建 `data.yaml` 配置文件：
```yaml
path: /path/to/dataset
train: images/train
val: images/val

names:
  0: 虫眼
  1: 裂缝
  2: 腐朽
  3: 变色
  4: 木节
  5: 划痕
```

### 3. 开始训练

```bash
# 安装 ultralytics
pip install ultralytics

# 开始训练 (根据显存调整 batch_size)
yolo detect train \
    data=data.yaml \
    model=yolov8n.pt \
    epochs=100 \
    batch=16 \
    imgsz=640 \
    device=0
```

> 我的训练环境：RTX 4070 Ti Super，训练参数需根据自身设备调整。

### 4. 导出模型

训练完成后，在 `runs/detect/train/weights/` 目录下找到 `best.pt`，重命名为 `yolov8n.pt`。

---

## 部署指南

### 树莓派端部署

#### 1. 连接树莓派

**方式一：VNC 远程桌面**
1. 登录路由器后台，查看树莓派 IP 地址
2. 下载 VNC Viewer 并连接
3. 进入树莓派桌面

**方式二：SSH 命令行**
```bash
ssh pi@<树莓派IP>
```

> ⚠️ 注意：树莓派重启后 IP 可能变化，建议设置静态 IP。

#### 2. 环境配置

```bash
# 创建项目目录
mkdir ~/yolo && cd ~/yolo

# 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 安装依赖 (使用清华镜像加速)
pip install ultralytics ncnn \
    -i https://pypi.tuna.tsinghua.edu.cn/simple \
    --trusted-host pypi.tuna.tsinghua.edu.cn \
    --resume-retries 100

# 安装模型转换工具
pip install onnx onnxslim onnxruntime \
    -i https://pypi.tuna.tsinghua.edu.cn/simple \
    --trusted-host pypi.tuna.tsinghua.edu.cn \
    --resume-retries 100

# 安装 Picamera2 (如果使用 CSI 摄像头)
pip install picamera2
```

#### 3. 模型转换

```bash
# 将训练好的模型传到树莓派 (使用 scp 或 xftp)
# 然后执行转换：
yolo export model=yolov8n.pt format=ncnn
```

转换完成后，检查目录结构：
```
yolo/
├── yolov8n.pt
└── yolov8n_ncnn_model/
    ├── model.ncnn.bin
    └── model.ncnn.param
```

#### 4. 测试模型

首先确认摄像头调用方式：

**Picamera2 (CSI 摄像头):**
```bash
python yolo_detect.py \
    --model=yolov8n_ncnn_model/ \
    --source=picamera \
    --resolution=640x480
```

**USB 摄像头:**
```bash
python yolo_detect.py \
    --model=yolov8n_ncnn_model/ \
    --source=usb0 \
    --resolution=640x480
```

看到检测画面即表示成功！

---

### 主机端部署

#### 方式一：直接运行 Python 脚本

```bash
# 安装依赖
pip install PyQt5 flask flask-cors opencv-python numpy requests

# 运行主机端程序
python server.py
```

#### 方式二：使用打包好的 EXE

直接运行 `YOLO_Server.exe`，无需配置 Python 环境。

#### 主机端界面配置

1. 启动主机端程序
2. 配置主机 IP 和端口（默认 5000）
3. 选择数据保存路径
4. 点击「启动服务器」

![主机端界面](https://github.com/user-attachments/assets/a22dfcb7-e6e2-444a-8591-49574376bd4a)

#### 连接树莓派与主机

在树莓派端执行：
```bash
python yolo_detector_client.py \
    --model yolov8n_ncnn_model/ \
    --source picamera \
    --resolution 640x480 \
    --server http://192.168.0.112:5000
```

> ⚠️ 将 `192.168.0.112` 替换为你的主机 IP！

成功连接后，主机端将实时显示检测画面：

![检测画面](https://github.com/user-attachments/assets/57d23bd2-66f1-4903-a7d5-4024b060ae34)

---

## 使用说明

### 树莓派端命令行参数

| 参数 | 说明 | 默认值 |
|-----|------|-------|
| `--model` | 模型路径（必需） | - |
| `--source` | 输入源（必需） | - |
| `--server` | 服务器地址（必需） | - |
| `--resolution` | 分辨率，如 640x480 | - |
| `--thresh` | 置信度阈值 | 0.5 |
| `--interval` | 发送间隔（秒） | 0（实时） |
| `--batch-size` | 批量发送大小 | 1 |
| `--compress` | 图像压缩质量 (1-100) | 80 |
| `--no-image` | 不发送图像，仅数据 | - |
| `--no-display` | 不显示本地窗口 | - |

### 使用示例

```bash
# 基本用法
python yolo_detector_client.py \
    --model yolov8n_ncnn_model/ \
    --source picamera \
    --server http://192.168.0.112:5000

# 高置信度 + 降低帧率
python yolo_detector_client.py \
    --model yolov8n_ncnn_model/ \
    --source picamera \
    --server http://192.168.0.112:5000 \
    --thresh 0.7 \
    --interval 0.5

# USB 摄像头 + 只传数据不传输图像
python yolo_detector_client.py \
    --model yolov8n_ncnn_model/ \
    --source usb0 \
    --server http://192.168.0.112:5000 \
    --no-image
```

### 主机端操作说明

1. **连接配置**
   - 填写主机 IP（点击「获取本机IP」可自动获取）
   - 设置端口（默认 5000）
   - 选择数据保存路径

2. **实时监控**
   - 切换到「检测画面」标签页
   - 查看实时检测结果
   - 点击「保存当前图像」手动保存

3. **数据管理**
   - 在「文件管理」中查看历史检测数据
   - 支持删除、导出操作
   - 可批量清理旧数据

4. **本地推理**
   - 在「本地推理」标签页
   - 选择模型和图片
   - 进行离线批量检测

---

## 项目结构

```
pi-server/
├── yolo_detector_client.py  # 树莓派端检测程序
├── server.py                # 主机端服务器程序
├── YOLO_Server.spec         # PyInstaller 打包配置
├── build_exe.py            # 打包脚本
├── quantized/              # 量化相关工具
├── dist/                   # 打包输出目录
│   └── YOLO_Server.exe     # 主机端可执行文件
└── pidata/                 # 默认数据保存目录
    ├── images/             # 检测图片
    ├── detections/         # 检测数据 (JSON)
    └── local_inference/    # 本地推理结果
```

---

## 常见问题

### Q: 树莓派无法连接到主机？
A: 请检查：
- 两者是否在同一局域网
- 主机 IP 是否正确
- 主机防火墙是否允许 5000 端口
- 服务器是否已启动

### Q: 摄像头无法打开？
A: 尝试不同的调用方式：
- Picamera2: `--source picamera`
- USB 摄像头: `--source usb0` 或 `--source usb1`
- 检查 `libcamera-hello` 是否正常工作

### Q: 检测速度慢？
A: 优化建议：
- 使用 NCNN 格式模型（已转换）
- 降低输入分辨率 `--resolution 480x320`
- 降低置信度阈值过滤小目标

### Q: 如何开机自启动？
A: 可以创建 systemd 服务或使用 rc.local。

---

## 联系方式

- 📧 Email: kexuehe1i@foxmail.com
- 💡 欢迎提交 Issue 和 PR！

如果这个项目对你有帮助，欢迎点个 Star ⭐，感谢支持！

![Star](https://github.com/user-attachments/assets/99b7a523-b16a-49ec-983b-fd224f2b7af2)

---

## 版本计划

- [ ] v1.1 提升模型精度（更大模型或更优数据集）
- [ ] 添加 Web 端远程查看功能
- [ ] 增加更多木材缺陷类别
- [ ] 录制演示视频

---

## 致谢

参考了很多 B 站上的教程，感谢开源社区！

