---
title: "JNEEG - Jetson Nano脑机接口扩展板"
description: "JNEEG是专为NVIDIA Jetson Nano设计的扩展板，实现8通道EEG、EMG及ECG生物信号采集，专为机器学习优化"
image: "images/jneeg.png"
weight: 40
---

# JNEEG - Jetson Nano脑机接口扩展板

## 基础信息

通过 JNEEG 脑机接口（低成本 EEG 设备）为 NVIDIA Jetson Nano 配备扩展板，实现 8 通道 EEG、EMG 及 ECG 生物信号的采集。

JNEEG 是专为 Jetson Nano 设计的一款工具，能够测量来自大脑、肌肉及心脏的生物电信号。该设备开源且免费，兼容多种传感器类型。只需连接传感器并运行简单的 Python 程序，即可开始数据采集。广泛适用于游戏、娱乐、运动、健康管理、冥想等多个领域。

⚠️ **重要提示**: JNEEG 不是医疗设备，未获得任何政府监管机构认证用于人体。购买与使用风险由用户自行承担，请务必阅读[《免责声明》](/disclaimer/)。

## 产品特性及参数

- **兼容性**: 兼容 NVIDIA Jetson Nano
- **通道数**: 支持 8 个通道，连接湿电极或干电极
- **数据传输**: 采用 SPI 协议传输数据，采样频率 250 SPS 至 16 kSPS，24 位分辨率
- **信号增益**: 可编程信号增益：1、2、4、6、8、12、24
- **阻抗测量**: 支持阻抗测量
- **软件支持**: 提供开源软件，支持 Python 编程读取和处理数据

## 为什么选择JNEEG

JNEEG 专为结合机器学习和深度学习技术处理 EEG 及其他生物信号的特征提取任务而设计。

Jetson Nano 是全球最受尊敬的单板计算机之一，因其出色的实时机器学习能力而广泛应用于计算机视觉和机器人控制等领域。

将 JNEEG 与 Jetson Nano 结合使用，开启了借助深度学习深入神经科学研究的新途径。该组合能够在 Jetson Nano 上实现 EEG 数据的无缝实时读取和信号处理，无需额外的数据传输或计算资源进行特征提取，极大提升效率。

我们为 JNEEG 用户提供完整的软件包、技术文档及全面的用户支持，助力开发者轻松实现创新应用。

## 潜在应用场景

### 智能控制系统
- [EEG 控制的智能轮椅](https://www.intechopen.com/chapters/86899)
- [便携式神经假肢手，基于深度学习实现手指动作控制](https://iopscience.iop.org/article/10.1088/1741-2552/ac2a8d/meta)

### 信号处理与分析
- [基于 EEG 信号时序分析的听觉脑波同步系统](https://ieeexplore.ieee.org/abstract/document/9813957)
- [个性化实时联邦学习，用于癫痫发作检测](https://ieeexplore.ieee.org/abstract/document/9479691)

## 支持文件及软件

- **GitHub仓库**: [https://github.com/pieeg-club/EEG-with-JetsonNano](https://github.com/pieeg-club/EEG-with-JetsonNano)
- **技术文档**: [https://pieeg.cn/docs/docs/jneeg/](https://pieeg.cn/docs/docs/jneeg/)

## 技术规格

| 规格项 | 参数 |
|--------|------|
| 兼容平台 | NVIDIA Jetson Nano |
| 通道数 | 8通道 |
| 电极类型 | 湿电极/干电极 |
| 分辨率 | 24位 |
| 采样频率 | 250 SPS - 16 kSPS |
| 信号增益 | 1, 2, 4, 6, 8, 12, 24 |
| 通信协议 | SPI |
| AI加速 | GPU加速深度学习 |

## 产品优势

### AI与机器学习优化
- **GPU加速**: 利用Jetson Nano的GPU进行实时深度学习推理
- **边缘计算**: 本地处理，无需云端传输
- **实时分析**: 毫秒级的信号处理和特征提取
- **深度学习框架**: 支持TensorFlow、PyTorch等主流框架

### 应用领域
- **计算机视觉**: 结合脑电和视觉信号的多模态分析
- **机器人控制**: 脑控机器人和自动化系统
- **智能医疗**: 实时健康监测和疾病预警
- **人机交互**: 自然的脑机接口体验

### 技术特点
- **低延迟**: 实时信号处理能力
- **高精度**: 24位ADC确保信号质量
- **可扩展**: 支持多种传感器和外设
- **开源生态**: 完整的软件工具链 