# 🌳 Tree Ring Animation - "Flower Playing"

一个优雅的树轮生长动画程序，结合自然音乐和真实环境数据，呈现树木34年（1990-2023）的生长历程。

## 📸 预览展示

### 🎬 动画效果
![Tree Ring Animation](tree_ring_animation.gif)

### 🖼️ 静态预览
![Tree Ring Preview](tree_ring_preview.png)

## ✨ 核心特色

### 🎵 音乐与动画同步
- **纯自然音乐**：C大调和谐旋律，120秒循环播放
- **节拍同步**：树轮生长与音乐节拍完美同步
- **情感表达**：音乐情感强度影响树轮颜色变化

### 🌈 自然色彩系统
- **仿真色调**：棕色、绿色等自然树木色彩
- **同心圆设计**：清晰的年轮层次，无重叠
- **动态渐变**：基于环境因子的柔和颜色过渡

### 📊 真实数据模拟
- **34年数据**：1990-2023年树轮生长记录
- **环境因子**：厚度、密度、生长率、气候压力
- **年份同步**：与音乐节拍同步的年份显示

### 🖥️ 优化界面
- **1200x800分辨率**：清晰的视觉体验
- **实时信息面板**：年份、进度、生长数据
- **韵律可视化**：Beat和Emotion强度条（已修复重叠问题）
- **简单操作**：[空格]播放/暂停 [R]重启 [Q]退出

## 🚀 快速开始

### 📥 从GitHub获取项目

#### 方法1：Git克隆（推荐）
```bash
# 克隆项目到本地
git clone https://github.com/ALuOvO222/Tree-Ring.git

# 进入项目目录
cd Tree-Ring
```

#### 方法2：直接下载
1. 访问 https://github.com/ALuOvO222/Tree-Ring
2. 点击绿色的 "Code" 按钮
3. 选择 "Download ZIP"
4. 解压下载的文件

### 🔧 环境配置

#### 安装Python依赖
```bash
# 安装核心依赖
pip install pygame numpy

# 或者使用requirements文件（如果有的话）
pip install -r requirements.txt
```

#### Python版本要求
- Python 3.7+ （推荐Python 3.9+）
- 已测试版本：Python 3.13.5

### 🎮 运行程序

```bash
# 在项目目录中运行
python gui_tree_ring.py
```

#### 🎵 音频选项说明
程序启动后会显示4个选项：
1. **无音频** - 仅显示动画和节拍模拟
2. **纯自然音乐** ⭐ **推荐** - 120秒C大调自然音乐
3. **森林环境音** - 环境音效（如果可用）
4. **自定义路径** - 使用您自己的音乐文件

**建议选择选项2获得最佳体验！**

## 📁 项目文件

```
🌳 Tree-Ring/
├── gui_tree_ring.py           # 🎯 主程序 - 完整GUI界面
├── tree_ring_data.json        # 📊 34年真实树轮数据
├── simple_music_generator.py  # 🎵 自然音乐生成器
├── music/
│   └── nature_simple.wav      # 🎼 自然音乐文件(120s)
├── requirements.txt           # 📦 Python依赖
└── README.md                  # 📖 项目文档
```

## 🎯 技术实现

- **pygame 2.6.1**：流畅的2D图形渲染
- **同心圆算法**：10px间距的清晰年轮结构  
- **HSV色彩空间**：自然的棕绿色调过渡
- **实时音频同步**：pygame.mixer音频引擎
- **数据驱动动画**：JSON格式的结构化数据

## � 操作控制

### 程序运行后的控制方式：
- **空格键 (SPACE)** - 播放/暂停动画
- **R键** - 重新开始动画
- **Q键 或 ESC** - 退出程序
- **鼠标点击关闭按钮** - 正常退出

### 🖥️ 界面说明
- **左侧区域** - 树轮动画主显示区域
- **右上面板** - 当前年份、进度、树轮数据信息
- **右下韵律条** - Beat(节拍)和Emotion(情感)强度可视化

## 🔧 故障排除

### 常见问题解决

#### ❌ 提示"ModuleNotFoundError: No module named 'pygame'"
```bash
# 解决方案：安装pygame
pip install pygame
```

#### ❌ 提示"ModuleNotFoundError: No module named 'numpy'"  
```bash
# 解决方案：安装numpy
pip install numpy
```

#### ❌ 音频无法播放
- 检查系统音频设备是否正常
- 尝试选择选项1（无音频模式）
- 确保`music/nature_simple.wav`文件存在

#### ❌ 窗口显示异常
- 确保显示器分辨率支持1200x800
- 检查显卡驱动是否更新
- 尝试更新pygame版本：`pip install --upgrade pygame`

#### ❌ Python版本兼容性问题
- 推荐使用Python 3.9+
- 检查Python版本：`python --version`
- 如使用较老版本，可能需要更新

### 📱 系统要求
- **操作系统**: Windows 10+, macOS 10.14+, Linux
- **Python**: 3.7+ (推荐3.9+)
- **内存**: 至少512MB可用内存
- **显示器**: 支持1200x800分辨率
- **音频**: 支持WAV格式播放（可选）

## �🌟 项目亮点

✅ **视觉优化完成** - 自然色彩同心圆，无重叠问题  
✅ **音频同步完成** - 节拍与年轮生长精确同步  
✅ **界面布局完成** - Beat/Emotion标签间距优化  
✅ **数据展示完成** - 34年真实环境数据可视化  
✅ **项目清理完成** - 仅保留核心功能文件  
✅ **跨平台支持** - Windows/macOS/Linux全平台兼容
✅ **开箱即用** - 下载即可运行，无复杂配置

## 📞 支持与反馈

如果在使用过程中遇到问题，请：
1. 检查上述故障排除章节
2. 确认所有依赖已正确安装
3. 在GitHub仓库提交Issue报告问题

---

*在数字世界中聆听生命的年轮故事* 🌳🎵✨  
**享受您的树轮动画之旅！**