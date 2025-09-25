#!/usr/bin/env python3
"""
树轮动画快速启动脚本
自动检查环境并启动程序
"""

import sys
import subprocess
import os

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ 需要Python 3.7或更高版本")
        print(f"   当前版本: Python {version.major}.{version.minor}.{version.micro}")
        return False
    else:
        print(f"✅ Python版本检查通过: {version.major}.{version.minor}.{version.micro}")
        return True

def check_module(module_name):
    """检查模块是否安装"""
    try:
        __import__(module_name)
        print(f"✅ {module_name} 已安装")
        return True
    except ImportError:
        print(f"❌ {module_name} 未安装")
        return False

def install_module(module_name):
    """安装模块"""
    print(f"🔧 正在安装 {module_name}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
        print(f"✅ {module_name} 安装成功")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ {module_name} 安装失败")
        return False

def check_files():
    """检查必要文件是否存在"""
    required_files = [
        "gui_tree_ring.py",
        "tree_ring_data.json",
        "music/nature_simple.wav"
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} 文件存在")
        else:
            print(f"❌ {file} 文件缺失")
            all_exist = False
    
    return all_exist

def main():
    """主函数"""
    print("🌳 树轮动画启动检查")
    print("=" * 40)
    
    # 检查Python版本
    if not check_python_version():
        input("按回车键退出...")
        return
    
    # 检查必要模块
    modules_to_check = ["pygame", "numpy", "json", "math"]
    missing_modules = []
    
    for module in modules_to_check:
        if not check_module(module):
            if module not in ["json", "math"]:  # 这些是内置模块
                missing_modules.append(module)
    
    # 安装缺失的模块
    if missing_modules:
        print(f"\n🔧 需要安装 {len(missing_modules)} 个模块:")
        for module in missing_modules:
            if not install_module(module):
                print("❌ 模块安装失败，程序无法继续")
                input("按回车键退出...")
                return
    
    # 检查文件
    print("\n📁 检查项目文件...")
    if not check_files():
        print("❌ 部分文件缺失，请确保完整下载了项目")
        input("按回车键退出...")
        return
    
    # 启动程序
    print("\n🚀 环境检查完成，正在启动树轮动画...")
    print("💡 提示：建议选择选项2（纯自然音乐）获得最佳体验")
    print()
    
    try:
        # 导入并运行主程序
        import gui_tree_ring
        gui_tree_ring.main()
    except Exception as e:
        print(f"❌ 程序运行出错: {e}")
        input("按回车键退出...")

if __name__ == "__main__":
    main()