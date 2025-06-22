---
title: "ardEEG - Arduino脑机接口扩展板"
description: "ardEEG是专为Arduino设计的扩展板，可采集EEG、EMG和ECG等生物电信号，支持多达8个EEG通道"
image: "images/ardeeg.png"
weight: 30
---

# ardEEG - Arduino脑机接口扩展板

## 基础信息

ardEEG – 使用 Arduino 实现 EEG 信号采集。

通过这款专为 Arduino 设计的扩展板，您可以采集 EEG、EMG 和 ECG 等生物电信号，支持多达 8 个 EEG 通道。

⚠️ **重要提示**: ardEEG 不是医疗器械，未获得任何政府监管机构关于人体使用的认证。购买和使用完全由用户自行承担风险，请务必阅读[《免责声明》](/disclaimer/)。

## 产品特性及参数

- **兼容性**: 兼容 Arduino UNO R4 WiFi
- **通道数**: 支持 8 个通道，可连接湿电极或干电极
- **数据传输**: 采用 SPI 协议进行数据传输，采样频率范围为 250 SPS 到 16 kSPS，每通道分辨率 24 位
- **信号增益**: 可编程信号增益：1、2、4、6、8、12、24 倍
- **阻抗测量**: 支持阻抗测量功能
- **软件支持**: 提供开源软件，支持使用 Python 进行数据读取与处理
- **开源**: 所有技术细节详见 GitHub 与 YouTube

## 为什么选择ardEEG

如果你熟悉 Arduino 在电子学习中的作用，那么 ardEEG 是你从电子入门迈向神经科学的理想工具。

Arduino 是全球最受欢迎的微控制器学习平台之一，操作简便、拓展性强。而将 ardEEG 与 Arduino 连接使用，可以轻松跨入生物电信号采集与脑科学研究的领域。其显著优势在于超低功耗、体积小、重量轻，因此非常适合打造可穿戴设备，适用于如脑控机械臂、健康监测等高需求场景。

我们为 ardEEG 用户提供完整的软件包、详尽的技术文档及全方位的技术支持，助力每一位脑电探索者高效实现创意与研究目标。

## 潜在应用场景

### 学术研究
- [基于 EEG 的 Arduino 实时脑控系统，用于交互控制](https://www.sciencedirect.com/science/article/pii/S1877050917319919)
- [使用脑电头戴设备与 Arduino 微控制器控制的脑控轮椅](https://ieeexplore.ieee.org/abstract/document/7095887)

### 实际应用
- [基于脑电信号的 Arduino 疲劳驾驶早期检测系统](https://d1wqtxts1xzle7.cloudfront.net/64492028/ijatcse200922020-libre.pdf)
- [脑电驱动的义肢控制系统](https://ieeexplore.ieee.org/abstract/document/7746219)

## 支持文件及软件

- **GitHub仓库**: [https://github.com/pieeg-club/ardEEG](https://github.com/pieeg-club/ardEEG)
- **技术文档**: [https://pieeg.cn/docs/docs/ardeeg/](https://pieeg.cn/docs/docs/ardeeg/)

## 技术规格

| 规格项 | 参数 |
|--------|------|
| 兼容平台 | Arduino UNO R4 WiFi |
| 通道数 | 8通道 |
| 电极类型 | 湿电极/干电极 |
| 分辨率 | 24位 |
| 采样频率 | 250 SPS - 16 kSPS |
| 信号增益 | 1, 2, 4, 6, 8, 12, 24 |
| 通信协议 | SPI |
| 功耗 | 超低功耗 |

## 产品优势

### 可穿戴设计
- **超低功耗**: 适合电池供电的长时间使用
- **小体积**: 便于集成到可穿戴设备中
- **轻重量**: 用户佩戴舒适度高

### Arduino生态
- **易学易用**: 基于流行的Arduino平台
- **丰富资源**: 大量的教程和社区支持
- **快速原型**: 适合快速验证想法和概念

### 应用场景
- 脑控机械臂
- 健康监测设备
- 情绪识别系统
- 疲劳检测应用
- 教育和学习项目 