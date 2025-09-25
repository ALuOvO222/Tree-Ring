#!/usr/bin/env python3
"""
生成树轮动画的预览图片
包括静态图片和GIF动画
"""

import pygame
import numpy as np
import json
import math
import colorsys
import os
from PIL import Image
import time

class TreeRingPreviewGenerator:
    def __init__(self):
        self.width = 1200
        self.height = 800
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tree Ring Preview Generator")
        
        # 颜色配置
        self.colors = {
            'background': (15, 20, 15),
            'text': (200, 220, 180),
            'panel': (25, 35, 25),
            'panel_border': (60, 80, 45),
            'progress_bg': (40, 50, 30),
            'progress_fill': (120, 160, 80),
            'year_highlight': (255, 255, 200),
            'rhythm_bar': (85, 150, 85),
        }
        
        # 字体
        try:
            self.font = pygame.font.Font(None, 28)
            self.font_large = pygame.font.Font(None, 36)
            self.font_small = pygame.font.Font(None, 20)
        except:
            self.font = pygame.font.SysFont('Arial', 28)
            self.font_large = pygame.font.SysFont('Arial', 36)
            self.font_small = pygame.font.SysFont('Arial', 20)
        
        # 载入数据
        self.load_tree_data()
        
    def load_tree_data(self):
        """加载树轮数据"""
        try:
            with open('tree_ring_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.tree_data = data
            print(f"✅ 载入 {len(self.tree_data)} 年树轮数据")
        except Exception as e:
            print(f"❌ 数据载入失败: {e}")
            self.tree_data = []
    
    def generate_natural_colors(self, data_point, time_factor=0.5):
        """生成自然的树木色彩"""
        # 基础色调 - 自然的棕色和绿色
        base_hue = 0.15 + data_point.get('weather_factor', 0.5) * 0.1  # 棕色到绿色
        
        # 饱和度基于密度
        saturation = 0.3 + data_point.get('density', 0.5) * 0.4
        
        # 亮度基于厚度
        value = 0.4 + data_point.get('thickness', 15) / 50.0
        value = min(0.8, value)
        
        # 添加时间变化
        hue_shift = math.sin(time_factor * math.pi * 2) * 0.05
        final_hue = (base_hue + hue_shift) % 1.0
        
        # 转换为RGB
        rgb = colorsys.hsv_to_rgb(final_hue, saturation, value)
        return tuple(int(c * 255) for c in rgb)
    
    def draw_tree_rings(self, current_year_float, time_factor=0.5):
        """绘制树轮"""
        if not self.tree_data:
            return
            
        # 当前应显示的年轮数量
        rings_to_show = int(current_year_float) + 1
        rings_to_show = min(rings_to_show, len(self.tree_data))
        rings_to_show = max(3, rings_to_show)  # 至少显示3个年轮
        
        center_x, center_y = self.width // 3, self.height // 2
        
        # 绘制年轮 - 同心圆设计
        for i in range(rings_to_show):
            if i >= len(self.tree_data):
                break
                
            data_point = self.tree_data[i]
            year = data_point['year']
            
            # 计算半径 - 固定间距的同心圆
            base_radius = 30 + i * 10
            thickness_variation = data_point.get('thickness', 15) / 15.0
            
            # 添加微小的节拍效果
            beat_effect = 1.0 + 0.02 * math.sin(time_factor * 4)
            radius = base_radius * thickness_variation * beat_effect
            
            # 获取颜色
            color = self.generate_natural_colors(data_point, time_factor)
            
            # 计算年轮宽度
            ring_width = 8  # 统一宽度
            
            # 绘制年轮环
            inner_radius = max(1, radius - ring_width // 2)
            outer_radius = radius + ring_width // 2
            
            # 绘制实心圆环
            pygame.draw.circle(self.screen, color, (center_x, center_y), int(outer_radius))
            if inner_radius > 0:
                pygame.draw.circle(self.screen, self.colors['background'], 
                                 (center_x, center_y), int(inner_radius))
            
            # 年份标签
            if i == rings_to_show - 1 or (year % 5 == 0):  # 显示最新的或每5年
                angle = (time_factor * 30) % 360  # 缓慢旋转
                label_radius = outer_radius + 15
                label_x = center_x + label_radius * math.cos(math.radians(angle))
                label_y = center_y + label_radius * math.sin(math.radians(angle))
                
                year_text = self.font_small.render(str(year), True, self.colors['year_highlight'])
                text_rect = year_text.get_rect(center=(label_x, label_y))
                self.screen.blit(year_text, text_rect)
    
    def draw_info_panel(self, current_year_float):
        """绘制信息面板"""
        panel_x = self.width * 2 // 3
        panel_y = 50
        panel_width = self.width - panel_x - 40
        panel_height = 200
        
        # 绘制面板背景
        pygame.draw.rect(self.screen, self.colors['panel'], 
                        (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(self.screen, self.colors['panel_border'], 
                        (panel_x, panel_y, panel_width, panel_height), 2)
        
        # 标题
        title = self.font_large.render("🌳 Tree Ring Animation", True, self.colors['text'])
        self.screen.blit(title, (panel_x + 10, panel_y + 10))
        
        # 当前年份
        current_year_int = int(current_year_float)
        if current_year_int < len(self.tree_data):
            year = self.tree_data[current_year_int]['year']
            year_text = self.font.render(f"Year: {year}", True, self.colors['text'])
            self.screen.blit(year_text, (panel_x + 10, panel_y + 50))
            
            # 进度
            progress = (current_year_int + 1) / len(self.tree_data)
            progress_text = self.font.render(f"Progress: {progress:.1%}", True, self.colors['text'])
            self.screen.blit(progress_text, (panel_x + 10, panel_y + 80))
            
            # 数据信息
            data = self.tree_data[current_year_int]
            thickness_text = self.font_small.render(f"Thickness: {data.get('thickness', 0):.1f}", 
                                                   True, self.colors['text'])
            density_text = self.font_small.render(f"Density: {data.get('density', 0):.2f}", 
                                                 True, self.colors['text'])
            
            self.screen.blit(thickness_text, (panel_x + 10, panel_y + 110))
            self.screen.blit(density_text, (panel_x + 10, panel_y + 130))
        
        # 项目信息
        subtitle = self.font_small.render("34 Years of Growth (1990-2023)", True, self.colors['text'])
        self.screen.blit(subtitle, (panel_x + 10, panel_y + 160))
    
    def draw_rhythm_bars(self, time_factor):
        """绘制韵律条"""
        bar_x = self.width * 2 // 3 + 20
        bar_y = 350
        bar_width = self.width - bar_x - 40
        bar_height = 16
        
        # 模拟节拍强度
        beat_strength = 0.7 + 0.3 * math.sin(time_factor * 4)
        emotion_intensity = 0.6 + 0.4 * math.sin(time_factor * 2)
        
        # 节拍条
        beat_width = int(bar_width * beat_strength)
        pygame.draw.rect(self.screen, self.colors['rhythm_bar'], 
                        (bar_x, bar_y, beat_width, bar_height))
        pygame.draw.rect(self.screen, self.colors['panel_border'], 
                        (bar_x, bar_y, bar_width, bar_height), 2)
        
        # 情感条
        emotion_width = int(bar_width * emotion_intensity)
        pygame.draw.rect(self.screen, self.colors['rhythm_bar'], 
                        (bar_x, bar_y + 24, emotion_width, bar_height))
        pygame.draw.rect(self.screen, self.colors['panel_border'], 
                        (bar_x, bar_y + 24, bar_width, bar_height), 2)
        
        # 标签
        beat_label = self.font_small.render("Beat", True, self.colors['text'])
        emotion_label = self.font_small.render("Emotion", True, self.colors['text'])
        self.screen.blit(beat_label, (bar_x, bar_y - 18))
        self.screen.blit(emotion_label, (bar_x, bar_y + 42))
    
    def generate_static_preview(self):
        """生成静态预览图"""
        print("🎨 生成静态预览图...")
        
        # 清空屏幕
        self.screen.fill(self.colors['background'])
        
        # 绘制完整的树轮（显示所有年轮）
        self.draw_tree_rings(len(self.tree_data) - 1, 0.5)
        
        # 绘制信息面板
        self.draw_info_panel(len(self.tree_data) - 1)
        
        # 绘制韵律条
        self.draw_rhythm_bars(0.5)
        
        # 添加标题
        title = self.font_large.render("🎵🌳 Tree Ring Animation - Flower Playing", True, 
                                      self.colors['year_highlight'])
        title_rect = title.get_rect(center=(self.width // 2, 30))
        self.screen.blit(title, title_rect)
        
        # 保存图片
        pygame.image.save(self.screen, "tree_ring_preview.png")
        print("✅ 静态预览图已保存: tree_ring_preview.png")
    
    def generate_gif_frames(self, num_frames=30, duration_seconds=6):
        """生成GIF动画帧"""
        print(f"🎬 生成GIF动画 ({num_frames}帧)...")
        
        frames = []
        
        for frame in range(num_frames):
            # 时间进度
            time_progress = frame / num_frames
            time_factor = time_progress * duration_seconds
            
            # 年轮生长进度
            year_progress = time_progress * len(self.tree_data)
            
            # 清空屏幕
            self.screen.fill(self.colors['background'])
            
            # 绘制树轮
            self.draw_tree_rings(year_progress, time_factor)
            
            # 绘制信息面板
            self.draw_info_panel(year_progress)
            
            # 绘制韵律条
            self.draw_rhythm_bars(time_factor)
            
            # 添加标题
            title = self.font_large.render("🎵🌳 Tree Ring Animation - Flower Playing", True, 
                                          self.colors['year_highlight'])
            title_rect = title.get_rect(center=(self.width // 2, 30))
            self.screen.blit(title, title_rect)
            
            # 转换为PIL图像
            pygame_image = pygame.surfarray.array3d(self.screen)
            pygame_image = pygame_image.swapaxes(0, 1)  # pygame uses (width, height), PIL uses (height, width)
            pil_image = Image.fromarray(pygame_image)
            frames.append(pil_image)
            
            print(f"  帧 {frame + 1}/{num_frames} 完成")
        
        # 保存GIF
        frames[0].save(
            "tree_ring_animation.gif",
            save_all=True,
            append_images=frames[1:],
            duration=200,  # 每帧200ms
            loop=0  # 无限循环
        )
        
        print("✅ GIF动画已保存: tree_ring_animation.gif")
    
    def generate_all_previews(self):
        """生成所有预览文件"""
        print("🌳 开始生成树轮动画预览文件...")
        
        # 生成静态图片
        self.generate_static_preview()
        
        # 生成GIF动画
        self.generate_gif_frames()
        
        print("🎉 所有预览文件生成完成！")
        
        # 清理
        pygame.quit()

def main():
    """主函数"""
    generator = TreeRingPreviewGenerator()
    generator.generate_all_previews()

if __name__ == "__main__":
    main()