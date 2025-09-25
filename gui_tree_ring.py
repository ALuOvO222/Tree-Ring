"""
🎵🌳 "Flower Playing" Tree Ring Animation - GUI Window Version
True graphical interface, not console text
"""

import pygame
import numpy as np
import math
import time
import json
import os
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class RhythmData:
    """Rhythm data structure"""
    beat_strength: float
    emotional_intensity: float
    section: str
    mood: str
    progress: float
    is_strong_beat: bool
    current_beat: int
    bpm: int
    time_elapsed: float

class GUITreeRingVisualizer:
    """图形化年轮可视化器"""
    
    def __init__(self, audio_path: Optional[str] = None):
        """初始化GUI可视化器"""
        # Initialize pygame (including audio)
        pygame.init()
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=1024)
        pygame.mixer.init()
        
        # 窗口设置
        self.width = 1200
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("[♪][🌳] Flower Playing - Tree Ring Growth Animation")
        
        # Audio settings
        self.audio_path = audio_path
        self.audio_loaded = False
        self.load_audio()
        
        # Font settings - Use system fonts
        pygame.font.init()
        try:
            # Try to use system fonts
            self.font_large = pygame.font.SysFont("arial", 20)
            self.font_medium = pygame.font.SysFont("arial", 16)
            self.font_small = pygame.font.SysFont("arial", 12)
            print("[✓] System fonts loaded successfully")
        except:
            try:
                # Fallback: Use default system font
                self.font_large = pygame.font.SysFont("arial", 20)
                self.font_medium = pygame.font.SysFont("arial", 16)
                self.font_small = pygame.font.SysFont("arial", 12)
                print("[!] Using English fonts")
            except:
                # Last resort: pygame default font
                self.font_large = pygame.font.Font(None, 24)
                self.font_medium = pygame.font.Font(None, 18)
                self.font_small = pygame.font.Font(None, 14)
                print("[!] Using default fonts")
        
        # 时钟
        self.clock = pygame.time.Clock()
        
        # 年轮数据
        self.load_tree_data()
        
        # 色彩主题 - 自然森林风格
        self.colors = {
            'background': (25, 35, 30),        # 深绿色背景，像森林
            'tree_center': (101, 67, 33),      # 保持树心的棕色
            'text': (240, 235, 210),           # 米色文字，更温和
            'highlight': (205, 170, 125),      # 浅棕色高亮
            'info_bg': (40, 50, 45, 180),      # 深绿色背景
            'panel_border': (120, 100, 80),    # 棕色边框
            'rhythm_bar': (85, 150, 85),       # 柔和的绿色
            'ring_colors': []
        }
        
        # 生成柔和的彩色年轮色彩
        self.generate_color_palette()
        
        # 动画状态
        self.is_playing = True
        self.start_time = time.time()
        self.current_year = 0.0
    
    def generate_color_palette(self):
        """生成自然柔和的树木色调年轮调色板"""
        colors = []
        num_rings = len(self.tree_data)
        
        # 定义自然的树木色调，模拟不同生长条件
        seasonal_colors = [
            (45, 0.40, 0.45),   # 深棕色 - 干旱年份
            (35, 0.35, 0.50),   # 浅棕色 - 正常年份  
            (25, 0.30, 0.55),   # 橙棕色 - 温暖年份
            (60, 0.25, 0.45),   # 黄棕色 - 成熟木质
            (90, 0.30, 0.40),   # 橄榄绿 - 生长旺盛
            (120, 0.25, 0.35),  # 森林绿 - 雨水充足
            (30, 0.35, 0.50),   # 赭石色 - 秋季生长
            (40, 0.30, 0.45),   # 琥珀色 - 成熟期
        ]
        
        for i in range(num_rings):
            # 根据年份数据选择颜色倾向
            if i < len(self.tree_data):
                growth_rate = self.tree_data[i]['growth_rate']
                weather_factor = self.tree_data[i]['weather_factor']
                stress_factor = self.tree_data[i]['stress_factor']
                
                # 根据生长条件选择基础色调
                if stress_factor > 0.3:  # 高压力年份，偏棕色
                    color_index = 0 if growth_rate < 1.0 else 1
                elif weather_factor > 1.2:  # 好天气，偏绿色
                    color_index = 4 if growth_rate > 1.2 else 5
                else:  # 正常年份
                    color_index = (i % 4) + 2
            else:
                color_index = i % len(seasonal_colors)
            
            hue, saturation, value = seasonal_colors[color_index]
            
            # 添加轻微的随机变化
            hue_variation = (i * 11) % 15 - 7  # -7到+7的变化
            hue = (hue + hue_variation) % 360
            
            # 转换为RGB
            h = hue / 60.0
            c = value * saturation
            x = c * (1 - abs((h % 2) - 1))
            m = value - c
            
            if 0 <= h < 1:
                r, g, b = c, x, 0
            elif 1 <= h < 2:
                r, g, b = x, c, 0
            elif 2 <= h < 3:
                r, g, b = 0, c, x
            elif 3 <= h < 4:
                r, g, b = 0, x, c
            elif 4 <= h < 5:
                r, g, b = x, 0, c
            else:
                r, g, b = c, 0, x
            
            # 添加偏移量得到最终RGB值
            final_r = int((r + m) * 255)
            final_g = int((g + m) * 255)
            final_b = int((b + m) * 255)
            
            colors.append((final_r, final_g, final_b))
        
        self.colors['ring_colors'] = colors
    
    def load_tree_data(self):
        """Load tree ring data"""
        try:
            with open('tree_ring_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            # Check data format
            if isinstance(data, list):
                self.tree_data = data
            elif isinstance(data, dict) and 'years' in data:
                self.tree_data = data['years']
            else:
                raise ValueError("Incorrect data format")
            print(f"[✓] Loaded {len(self.tree_data)} years of tree ring data (1990-2023)")
        except FileNotFoundError:
            print("[!] tree_ring_data.json not found, using mock data")
            self.tree_data = self.generate_mock_data()
        except Exception as e:
            print(f"[!] Error loading data: {e}")
            self.tree_data = self.generate_mock_data()
    
    def generate_mock_data(self):
        """Generate mock tree ring data"""
        years = []
        for year in range(1990, 2024):
            years.append({
                'year': year,
                'thickness': 3 + 2 * math.sin(year * 0.1),
                'density': 0.7 + 0.3 * math.cos(year * 0.15),
                'growth_rate': 1.0 + 0.3 * math.sin(year * 0.2),
                'weather_factor': 0.8 + 0.4 * math.cos(year * 0.25),
                'stress_factor': 0.1 + 0.2 * abs(math.sin(year * 0.3))
            })
        return years
    
    def load_audio(self):
        """Load audio file"""
        if not self.audio_path:
            print("[!] No audio file specified")
            return
        
        if not os.path.exists(self.audio_path):
            print(f"[!] Audio file does not exist: {self.audio_path}")
            return
        
        try:
            pygame.mixer.music.load(self.audio_path)
            self.audio_loaded = True
            print(f"[✓] Audio file loaded successfully: {os.path.basename(self.audio_path)}")
        except Exception as e:
            print(f"[!] Audio loading failed: {e}")
            self.audio_loaded = False
    
    def play_audio(self):
        """Play audio"""
        if self.audio_loaded:
            try:
                pygame.mixer.music.play(-1)  # -1 表示循环播放
                print("[✓] Audio playback started")
            except Exception as e:
                print(f"[!] Audio playback failed: {e}")
    
    def pause_audio(self):
        """Pause/resume audio"""
        if self.audio_loaded:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                print("[♪] Audio paused")
            else:
                pygame.mixer.music.unpause()
                print("[♪] Audio resumed")
    
    def stop_audio(self):
        """Stop audio"""
        if self.audio_loaded:
            pygame.mixer.music.stop()
            print("[♪] Audio stopped")
    
    def get_rhythm_data(self, current_time: float) -> RhythmData:
        """获取当前时间的韵律数据"""
        # 模拟120 BPM的节拍
        bpm = 120
        beat_interval = 60.0 / bpm
        current_beat = int(current_time / beat_interval)
        beat_progress = (current_time % beat_interval) / beat_interval
        
        # 强弱拍模式（4/4拍）
        is_strong_beat = (current_beat % 4) == 0
        beat_strength = 1.0 if is_strong_beat else 0.6
        
        # 情感强度随时间变化
        emotional_intensity = 0.7 + 0.3 * math.sin(current_time * 0.1)
        
        # Music sections
        section_time = current_time % 32  # 32秒一个循环
        if section_time < 8:
            section = "intro"
            mood = "gentle"
        elif section_time < 16:
            section = "verse"
            mood = "building"
        elif section_time < 24:
            section = "chorus"
            mood = "energetic"
        else:
            section = "outro"
            mood = "calm"
        
        return RhythmData(
            beat_strength=beat_strength,
            emotional_intensity=emotional_intensity,
            section=section,
            mood=mood,
            progress=beat_progress,
            is_strong_beat=is_strong_beat,
            current_beat=current_beat,
            bpm=bpm,
            time_elapsed=current_time
        )
    
    def update_animation(self, rhythm_data: RhythmData):
        """更新动画状态"""
        if not self.is_playing:
            return
        
        # 根据节拍更新年份进度
        year_duration = 2.5  # 每年2.5秒，稍微加快生长速度
        self.current_year = min(
            len(self.tree_data) - 1,
            rhythm_data.time_elapsed / year_duration
        )
    
    def draw_tree_rings(self, rhythm_data: RhythmData):
        """绘制彩色年轮"""
        center_x = self.width // 3
        center_y = self.height // 2
        
        # 当前应显示的年轮数量
        current_rings = int(self.current_year) + 1
        
        # 确保至少显示3个年轮以获得更好的视觉效果
        current_rings = max(3, current_rings)
        
        # 绘制年轮 - 重新设计为清晰的同心圆环
        for i in range(current_rings):
            if i >= len(self.tree_data):
                break
            
            ring_data = self.tree_data[i]
            
            # 固定且均匀的年轮半径分布，确保同心圆效果
            base_radius = 30 + i * 10  # 从30开始，每个年轮间距10像素，更紧凑但清晰
            
            # 轻微的厚度变化，但不影响同心圆结构
            thickness_variation = 1.0 + (ring_data['thickness'] - 3.0) * 0.1  # 轻微调整
            radius = base_radius * thickness_variation
            
            # 轻微的节拍效果，不影响整体结构
            beat_effect = 1.0 + rhythm_data.beat_strength * 0.08 * math.sin(rhythm_data.time_elapsed * 4)
            radius *= beat_effect
            
            # 获取颜色
            color = self.colors['ring_colors'][i % len(self.colors['ring_colors'])]
            
            # 计算年轮宽度 - 统一且更细
            if i == 0:
                # 中心圆 - 固定大小的树心
                inner_radius = 0
                ring_width = int(radius)
            else:
                # 年轮环 - 固定宽度，确保清晰分离
                inner_radius = 30 + (i-1) * 10 * thickness_variation * beat_effect
                ring_width = min(6, max(3, int(radius - inner_radius)))  # 宽度限制在3-6像素，更细更均匀
            
            # 绘制年轮环
            if i == 0:
                # 中心圆
                pygame.draw.circle(self.screen, color, (center_x, center_y), int(radius))
                # 添加柔和的中心高光
                highlight_color = tuple(min(255, int(c * 1.15)) for c in color)
                pygame.draw.circle(self.screen, highlight_color, (center_x, center_y), int(radius * 0.6))
            else:
                # 年轮环 - 确保有间隙，不相互遮挡
                # 先绘制一个细的间隙（用背景色）
                gap_width = 1
                gap_radius = inner_radius + ring_width + gap_width
                pygame.draw.circle(self.screen, self.colors['background'], (center_x, center_y), int(gap_radius), gap_width)
                
                # 然后绘制年轮环
                pygame.draw.circle(self.screen, color, (center_x, center_y), int(radius), ring_width)
                
                # 添加内边界线增强分离效果
                border_color = tuple(max(15, int(c * 0.6)) for c in color)
                pygame.draw.circle(self.screen, border_color, (center_x, center_y), int(inner_radius + 1), 1)
            
            # 年份标签 - 与年轮生长同步显示
            should_show_label = False
            
            # 显示逻辑：
            # 1. 已完全生长的年轮每3年显示一次
            # 2. 正在生长的年轮始终显示年份
            # 3. 最近几年的年轮更频繁显示
            
            if i < int(self.current_year):
                # 已完全生长的年轮
                should_show_label = (i % 3 == 0) or (i >= len(self.tree_data) - 5)
            elif i == int(self.current_year):
                # 正在生长的年轮 - 始终显示，并且有节拍闪烁效果
                should_show_label = True
            
            if should_show_label and radius > 35:
                year_text = str(ring_data['year'])
                
                # 正在生长的年轮使用高亮颜色并有节拍效果
                if i == int(self.current_year):
                    # Beat flash effect - synchronized with music strong beats
                    base_intensity = 0.8
                    beat_pulse = 0.2 * rhythm_data.beat_strength
                    emotion_pulse = 0.1 * rhythm_data.emotional_intensity
                    flash_intensity = base_intensity + beat_pulse + emotion_pulse
                    
                    text_color = tuple(min(255, int(c * flash_intensity)) for c in self.colors['highlight'])
                    font_to_use = self.font_medium  # 使用更大的字体
                    
                    # 强拍时字体更大
                    if rhythm_data.is_strong_beat:
                        font_to_use = self.font_large
                else:
                    text_color = self.colors['text']
                    font_to_use = self.font_small
                
                text_surface = font_to_use.render(year_text, True, text_color)
                
                # 计算标签位置（在年轮之间的间隙中）
                # 基础角度 + 缓慢旋转 + 节拍摆动
                base_angle = i * 45
                slow_rotation = rhythm_data.time_elapsed * 5  # 缓慢旋转
                beat_swing = math.sin(rhythm_data.current_beat * 0.5) * 10  # 节拍摆动
                angle = (base_angle + slow_rotation + beat_swing) % 360
                
                label_radius = radius + 12  # 距离年轮外边缘12像素
                text_x = center_x + label_radius * math.cos(math.radians(angle))
                text_y = center_y + label_radius * math.sin(math.radians(angle))
                
                # 添加自然色调的半透明背景
                text_rect = text_surface.get_rect(center=(text_x, text_y))
                bg_surface = pygame.Surface((text_rect.width + 6, text_rect.height + 4), pygame.SRCALPHA)
                
                if i == int(self.current_year):
                    # 正在生长的年份使用更明显的背景
                    bg_color = (40, 50, 35, 200)
                else:
                    bg_color = (25, 35, 30, 160)
                
                bg_surface.fill(bg_color)
                bg_rect = bg_surface.get_rect(center=(text_x, text_y))
                self.screen.blit(bg_surface, bg_rect)
                self.screen.blit(text_surface, text_rect)
    
    def draw_info_panel(self, rhythm_data: RhythmData):
        """绘制信息面板"""
        # 右侧信息面板 - 优化尺寸避免重叠
        panel_x = self.width * 2 // 3 + 20
        panel_y = 80  # 向下移动，避免与顶部进度条重叠
        panel_width = self.width - panel_x - 20
        panel_height = 250  # 减小高度，避免与韵律条重叠
        
        # 绘制面板背景
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill(self.colors['info_bg'])
        self.screen.blit(panel_surface, (panel_x, panel_y))
        
        # 绘制边框
        pygame.draw.rect(self.screen, self.colors['panel_border'], 
                        (panel_x, panel_y, panel_width, panel_height), 2)
        
        # 当前年份信息 - 简化显示，避免重叠
        current_year_int = int(self.current_year)
        year_progress = self.current_year - current_year_int
        
        if current_year_int < len(self.tree_data):
            current_data = self.tree_data[current_year_int]
            
            # Core data information in English
            info_texts = [
                f"Year: {current_data['year']}",
                f"Progress: {year_progress*100:.0f}%",
                f"Completed: {current_year_int}/{len(self.tree_data)}",
                "",
                f"Thickness: {current_data['thickness']:.1f}mm",
                f"Density: {current_data['density']:.2f}",
                f"Growth Rate: {current_data['growth_rate']:.2f}",
                f"Weather: {current_data['weather_factor']:.2f}",
                f"Stress: {current_data['stress_factor']:.2f}",
                "",
                f"Beat: {rhythm_data.current_beat}",
                f"BPM: {rhythm_data.bpm}"
            ]
            
            # 渲染文本 - 调整行距避免重叠
            y_offset = panel_y + 15
            line_height = 16  # 减小行高避免重叠
            
            for i, text in enumerate(info_texts):
                if text:  # 跳过空行
                    # Title uses highlight color
                    if i == 0 or text.startswith("Year"):
                        color = self.colors['highlight']
                        font = self.font_medium
                    else:
                        color = self.colors['text']
                        font = self.font_small
                    
                    text_surface = font.render(text, True, color)
                    self.screen.blit(text_surface, (panel_x + 10, y_offset))
                
                y_offset += line_height
    
    def draw_rhythm_bars(self, rhythm_data: RhythmData):
        """绘制韵律条"""
        # 韵律可视化条 - 调整位置避免重叠
        bar_x = self.width * 2 // 3 + 20
        bar_y = 350  # 向上移动，避免与其他元素重叠
        bar_width = self.width - bar_x - 40
        bar_height = 16  # 稍微减小高度
        
        # 节拍强度条 - 使用柔和的绿色
        beat_width = int(bar_width * rhythm_data.beat_strength)
        pygame.draw.rect(self.screen, (90, 140, 90), 
                        (bar_x, bar_y, beat_width, bar_height))
        pygame.draw.rect(self.screen, self.colors['panel_border'], 
                        (bar_x, bar_y, bar_width, bar_height), 2)
        
        # 情感强度条 - 使用温暖的棕色，调整间距
        emotion_width = int(bar_width * rhythm_data.emotional_intensity)
        pygame.draw.rect(self.screen, (160, 120, 90), 
                        (bar_x, bar_y + 24, emotion_width, bar_height))
        pygame.draw.rect(self.screen, self.colors['panel_border'], 
                        (bar_x, bar_y + 24, bar_width, bar_height), 2)
        
        # Labels - English text with proper spacing
        beat_label = self.font_small.render("Beat", True, self.colors['text'])
        emotion_label = self.font_small.render("Emotion", True, self.colors['text'])
        self.screen.blit(beat_label, (bar_x, bar_y - 18))
        self.screen.blit(emotion_label, (bar_x, bar_y + 42))
    
    def draw_year_progress(self, rhythm_data: RhythmData):
        """绘制年份进度条和当前年份显示"""
        # 年份进度条位置 - 优化布局
        progress_x = self.width // 6
        progress_y = 15
        progress_width = self.width * 2 // 3
        progress_height = 10
        
        # 计算进度
        total_years = len(self.tree_data)
        current_progress = self.current_year / total_years
        
        # 绘制进度条背景
        pygame.draw.rect(self.screen, (60, 70, 65), 
                        (progress_x, progress_y, progress_width, progress_height))
        
        # 绘制进度
        filled_width = int(progress_width * current_progress)
        if filled_width > 0:
            pygame.draw.rect(self.screen, (120, 140, 100), 
                            (progress_x, progress_y, filled_width, progress_height))
        
        # 绘制边框
        pygame.draw.rect(self.screen, self.colors['panel_border'], 
                        (progress_x, progress_y, progress_width, progress_height), 2)
        
        # 当前年份显示 - 大字体，居中，有节拍效果
        current_year_int = int(self.current_year)
        if current_year_int < len(self.tree_data):
            current_data = self.tree_data[current_year_int]
            year_progress = self.current_year - current_year_int
            
            # 节拍闪烁效果
            flash_intensity = 0.8 + 0.2 * rhythm_data.beat_strength
            year_color = tuple(int(c * flash_intensity) for c in self.colors['highlight'])
            
            # 显示当前年份和进度 - 优化位置
            year_text = f"{current_data['year']} ({year_progress*100:.0f}%)"
            year_surface = self.font_large.render(year_text, True, year_color)
            year_rect = year_surface.get_rect(center=(self.width // 2, progress_y + progress_height + 20))
            
            # 添加背景
            bg_surface = pygame.Surface((year_rect.width + 8, year_rect.height + 4), pygame.SRCALPHA)
            bg_surface.fill((25, 35, 30, 180))
            bg_rect = bg_surface.get_rect(center=year_rect.center)
            self.screen.blit(bg_surface, bg_rect)
            self.screen.blit(year_surface, year_rect)
            
            # 显示总进度信息 - 精简显示
            progress_text = f"{current_year_int + 1}/{total_years}"
            progress_surface = self.font_small.render(progress_text, True, self.colors['text'])
            progress_rect = progress_surface.get_rect(center=(self.width // 2, progress_y + progress_height + 40))
            self.screen.blit(progress_surface, progress_rect)
    
    def draw_controls_help(self):
        """Draw control instructions"""
        # Simplified control instructions to save space
        help_texts = [
            "[SPACE]Play [R]Restart [Q]Exit"
        ]
        
        y_start = self.height - 40  # Move to bottom edge
        for text in help_texts:
            text_surface = self.font_small.render(text, True, self.colors['text'])
            self.screen.blit(text_surface, (20, y_start))
    
    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("[!] User closed window")
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.is_playing = not self.is_playing
                    print(f"[♪] {'Playing' if self.is_playing else 'Paused'}")
                elif event.key == pygame.K_r:
                    self.current_year = 0.0
                    self.start_time = time.time()
                    if self.audio_loaded:
                        self.stop_audio()
                        self.play_audio()
                    print("[↻] Restarted")
                elif event.key == pygame.K_p:
                    self.pause_audio()
                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    print("[!] User requested exit")
                    return False
        return True
    
    def run(self, duration=None):
        """Run animation"""
        print("[Start] Tree ring animation starting...")
        
        # Start playing audio
        if self.audio_loaded:
            self.play_audio()
        
        running = True
        start_time = time.time()
        
        try:
            while running:
                # Check timeout if duration limit is set
                if duration and (time.time() - start_time > duration):
                    print(f"[Time] Duration limit {duration} seconds reached, exiting")
                    break
                
                # Handle events
                running = self.handle_events()
                if not running:
                    print("[Exit] User requested exit")
                    break
                
                # 获取当前时间和韵律数据
                current_time = time.time() - self.start_time
                rhythm_data = self.get_rhythm_data(current_time)
                
                # 更新动画
                self.update_animation(rhythm_data)
                
                # 清屏
                self.screen.fill(self.colors['background'])
                
                # 绘制年轮
                self.draw_tree_rings(rhythm_data)
                
                # 绘制信息面板
                self.draw_info_panel(rhythm_data)
                
                # 绘制韵律条
                self.draw_rhythm_bars(rhythm_data)
                
                # 绘制控制说明
                self.draw_controls_help()
                
                # Draw playback status
                status_text = "[Playing]" if self.is_playing else "[Paused]"
                status_surface = self.font_medium.render(status_text, True, self.colors['highlight'])
                status_rect = status_surface.get_rect(center=(self.width // 2, 50))
                self.screen.blit(status_surface, status_rect)
                
                # 绘制年份进度条和当前年份
                self.draw_year_progress(rhythm_data)
                
                # 更新显示
                pygame.display.flip()
                self.clock.tick(60)  # 60 FPS
                
        except KeyboardInterrupt:
            print("[Interrupt] Keyboard interrupt detected")
        except Exception as e:
            print(f"[Error] Runtime error: {e}")
        
        # Stop audio and exit
        print("[Cleanup] Cleaning up resources...")
        self.stop_audio()
        pygame.quit()
        print("[♪][🌳] GUI animation ended")
        print("[♥] Thank you for experiencing the tree ring animation!")

def main():
    """Main function"""
    print("[♪][🌳] 'Flower Playing' Tree Ring Animation - GUI Version")
    print("=" * 50)
    
    # Audio file options
    audio_options = [
        None,
        r"D:\Peekaboooo\music\nature_simple.wav",
        r"D:\Peekaboooo\music\nature_forest.wav",
        r"D:\Peekaboooo\music\flower_playing_generated.wav"
    ]
    
    print("[♪] Audio Options:")
    print("1. No audio (rhythm simulation only)")
    print("2. [✨] Pure nature music (fixed version) [✨]")  
    print("3. Forest ambient music")
    print("4. Custom path")
    
    try:
        choice = input("Please choose (1-4, Enter for default option 2): ").strip()
        
        if choice == "1":
            audio_path = None
        elif choice == "3":
            audio_path = audio_options[2]
        elif choice == "4":
            audio_path = input("Please enter audio file path: ").strip()
        else:  # Default option 2 - Pure nature music
            audio_path = audio_options[1]
        
        print("Opening graphical window...")
        
        visualizer = GUITreeRingVisualizer(audio_path)
        visualizer.run()  # Infinite loop until user presses Q to exit
        
    except KeyboardInterrupt:
        print("\n[Goodbye] Program exited")
    except Exception as e:
        print(f"[Error] Error: {e}")
        print("Please ensure pygame is properly installed")

if __name__ == "__main__":
    main()