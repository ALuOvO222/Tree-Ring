#!/usr/bin/env python3
"""
项目清理脚本 - 删除与树轮动画项目无关的文件
保留核心项目文件，清理多余和错误的文件
"""

import os
import shutil

def main():
    print("🌳 开始清理树轮动画项目...")
    
    # 需要保留的核心文件
    keep_files = {
        'gui_tree_ring.py',           # 主GUI程序
        'simple_music_generator.py',   # 音乐生成器
        'tree_ring_data.json',        # 树轮数据
        'README.md',                  # 项目说明
        'requirements.txt',           # 依赖文件
        'cleanup_project.py'          # 这个清理脚本本身
    }
    
    # 需要保留的文件夹
    keep_dirs = {
        'music',                      # 音乐文件夹
        '.git',                       # Git版本控制
        '.conda',                     # Conda环境
        '.vscode'                     # VS Code配置
    }
    
    # 需要删除的文件（明确指定）
    delete_files = {
        'gui_tree_ring_broken.py',    # 损坏的版本
        'data_generator.py',          # 数据生成器（已不需要）
        'tree_ring_animator.py',      # 旧动画器
        'tree_ring.gif',              # 旧图片文件
        'tree_ring.png'               # 旧图片文件
    }
    
    current_dir = os.getcwd()
    print(f"清理目录: {current_dir}")
    
    # 删除指定的无关文件
    deleted_count = 0
    for filename in delete_files:
        filepath = os.path.join(current_dir, filename)
        if os.path.exists(filepath):
            try:
                if os.path.isfile(filepath):
                    os.remove(filepath)
                    print(f"✅ 已删除文件: {filename}")
                    deleted_count += 1
                elif os.path.isdir(filepath):
                    shutil.rmtree(filepath)
                    print(f"✅ 已删除文件夹: {filename}")
                    deleted_count += 1
            except Exception as e:
                print(f"❌ 删除失败 {filename}: {e}")
    
    # 检查剩余文件
    print("\n📋 清理后保留的文件:")
    for item in os.listdir(current_dir):
        if os.path.isfile(item):
            if item in keep_files:
                print(f"✅ 核心文件: {item}")
            else:
                print(f"⚠️  其他文件: {item}")
        elif os.path.isdir(item):
            if item in keep_dirs:
                print(f"📁 核心目录: {item}/")
            else:
                print(f"📁 其他目录: {item}/")
    
    print(f"\n🎯 清理完成！删除了 {deleted_count} 个文件/文件夹")
    print("🌳 项目现在只包含树轮动画的核心文件！")

if __name__ == "__main__":
    main()