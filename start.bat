@echo off
chcp 65001 >nul
echo 🌳 Tree Ring Animation - 树轮动画启动器
echo ==========================================
echo.

echo 🔍 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，请先安装Python 3.7+
    echo 💡 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python环境检查通过
echo.

echo 🚀 启动树轮动画程序...
echo 💡 提示：建议选择选项2（纯自然音乐）获得最佳体验
echo.

python gui_tree_ring.py

if errorlevel 1 (
    echo.
    echo ❌ 程序运行遇到问题
    echo 🔧 尝试安装依赖: pip install pygame numpy
    echo.
    pause
)