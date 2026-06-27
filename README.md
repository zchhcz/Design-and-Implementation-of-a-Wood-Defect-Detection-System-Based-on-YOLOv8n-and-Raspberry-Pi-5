# 🌲 YOLO木材缺陷检测系统

基于YOLOv8的实时木材表面缺陷检测系统，采用客户端-服务器架构，支持树莓派摄像头实时采集和PC端集中管理。

## ✨ 主要特性

- 🎯 **实时检测**: 支持树莓派Picamera2、USB摄像头实时采集
- 🖥️ **可视化界面**: PyQt5图形界面，实时显示检测画面和统计信息
- 💾 **智能存储**: 仅保存有缺陷的图像，节省存储空间
- 🔄 **本地推理**: 支持离线批量图像检测
- 📊 **数据管理**: 完整的文件管理和统计分析功能
- 🌐 **网络传输**: HTTP通信，支持多客户端连接

## 📋 系统架构

```
树莓派端 (客户端)                主机端 (服务器)
┌──────────────────┐           ┌──────────────────┐
│  摄像头采集      │           │  Flask API       │
│       ↓          │           │       ↓          │
│  YOLO推理        │  HTTP     │  数据接收        │
│       ↓          │  ────→    │       ↓          │
│  结果压缩        │           │  PyQt5 GUI       │
│       ↓          │           │       ↓          │
│  队列发送        │           │  存储+显示       │
└──────────────────┘           └──────────────────┘
```

## 🚀 快速开始

### 环境要求

- **服务器端 (PC)**:
  - Python 3.8+
  - Windows/Linux/macOS
  - 建议2GB+内存

- **客户端 (树莓派)**:
  - Python 3.8+
  - Raspberry Pi 3B+ 或更高
  - 摄像头 (Picamera2/USB)

### 安装步骤

#### 1. 克隆项目

```bash
git clone https://github.com/yourusername/yolo-wood-defect-detection.git
cd yolo-wood-defect-detection
```

#### 2. 安装依赖

**服务器端 (PC)**:
```bash
pip install -r requirements.txt
```

**客户端 (树莓派)**:
```bash
pip install -r requirements.txt
# 如果使用Picamera2
pip install picamera2
```

#### 3. 准备YOLO模型

将训练好的YOLO模型文件 (`.pt`) 放在项目根目录，例如 `best.pt`

## 📖 使用说明

### 服务器端

启动主机端GUI程序：

```bash
python server.py
```

**操作步骤**:
1. 在"连接配置"页面设置主机IP和端口
2. 设置数据保存路径
3. 点击"启动服务器"
4. 等待树莓派客户端连接

### 客户端 (树莓派)

#### 使用Picamera2摄像头：
```bash
python yolo_detector_client.py \
  --model best.pt \
  --source picamera \
  --resolution 640x480 \
  --server http://192.168.0.112:5000
```

#### 使用USB摄像头：
```bash
python yolo_detector_client.py \
  --model best.pt \
  --source usb0 \
  --server http://192.168.0.112:5000
```

#### 批量处理图像：
```bash
python yolo_detector_client.py \
  --model best.pt \
  --source /path/to/images/ \
  --server http://192.168.0.112:5000
```

### 客户端参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--model` | YOLO模型路径 | 必需 |
| `--source` | 输入源 (picamera/usb0/video/image/folder) | 必需 |
| `--server` | 服务器地址 | 必需 |
| `--thresh` | 置信度阈值 | 0.5 |
| `--resolution` | 分辨率 (如 640x480) | 默认 |
| `--compress` | 图像压缩质量 (1-100) | 80 |
| `--no-image` | 不发送图像，仅发送检测结果 | False |
| `--no-display` | 不显示本地窗口 | False |

### 快捷键

客户端运行时支持的快捷键：
- `q`: 退出程序
- `s`: 暂停/继续
- `p`: 保存当前帧截图
- `i`: 显示详细信息

## 🛠️ 工具脚本

### 模型转换

将PyTorch模型转换为ONNX格式：

```bash
python convert.py --model best.pt --format onnx
```

## 📁 项目结构

```
.
├── server.py                 # 主机端GUI程序
├── yolo_detector_client.py   # 树莓派客户端程序
├── convert.py                # 模型转换工具
├── requirements.txt          # Python依赖
├── README.md                 # 项目说明
├── LICENSE                   # 开源许可证
└── .gitignore               # Git忽略规则
```

运行时会自动创建：
```
pidata/                       # 数据存储目录
├── images/                   # 检测到缺陷的图像
├── detections/               # JSON格式检测结果
├── local_inference/          # 本地推理结果
└── stats/                    # 统计数据
```

## 🎯 功能特点

### 服务器端功能

- ✅ 实时接收和显示检测结果
- ✅ 仅保存有缺陷的图像（节省存储）
- ✅ 手动保存功能（任何图像）
- ✅ 本地离线推理
- ✅ 文件管理（浏览、删除、清理）
- ✅ 统计分析和数据可视化
- ✅ 多客户端支持

### 客户端功能

- ✅ 多种输入源支持
- ✅ 实时性能监控
- ✅ 队列缓冲机制
- ✅ 自动重连
- ✅ 离线模式
- ✅ 图像压缩传输

## 🔧 常见问题

### Q: 无法连接到服务器？
**A**: 检查以下几点：
1. 确认主机IP地址正确
2. 确认服务器已启动
3. 检查防火墙设置（开放5000端口）
4. 确认两台设备在同一网络

### Q: 树莓派Picamera2无法使用？
**A**: 确保已安装picamera2库：
```bash
sudo apt update
sudo apt install -y python3-picamera2
```

### Q: 检测速度慢？
**A**: 尝试以下方法：
1. 降低输入分辨率 `--resolution 320x240`
2. 提高压缩质量 `--compress 60`
3. 使用更小的YOLO模型（如YOLOv8n）
4. 关闭本地显示 `--no-display`

## 📊 性能参考

| 设备 | 模型 | 分辨率 | FPS |
|------|------|--------|-----|
| 树莓派 4B | YOLOv8n | 640×480 | ~8-10 |
| 树莓派 4B | YOLOv8n | 320×240 | ~15-20 |
| PC (RTX 3060) | YOLOv8n | 640×480 | ~60+ |

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 开源许可

本项目采用 [MIT License](LICENSE) 开源许可证。

## 👨‍💻 作者

[您的名字] - [您的邮箱或GitHub]

## 🙏 致谢

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- [OpenCV](https://opencv.org/)
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/)
