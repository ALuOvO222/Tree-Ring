"""
🎵🌳 简单优美的自然音乐生成器
修复版本 - 专注于创建真正悦耳的音乐，而不是噪音
"""

import numpy as np
import wave
import math
import os

class SimpleNatureMusicGenerator:
    """简单自然音乐生成器 - 专注于音质"""
    
    def __init__(self):
        self.sample_rate = 44100
        self.duration = 120  # 2分钟
        self.total_samples = int(self.sample_rate * self.duration)
        
    def generate_simple_melody(self):
        """生成简单优美的旋律"""
        print("🎵 生成简单优美的自然音乐...")
        
        # 创建时间轴
        t = np.linspace(0, self.duration, self.total_samples, False)
        
        # === 使用简单的音符序列创建旋律 ===
        
        # C大调音阶频率 (简单美妙)
        notes = {
            'C4': 261.63,
            'D4': 293.66,
            'E4': 329.63,
            'F4': 349.23,
            'G4': 392.00,
            'A4': 440.00,
            'B4': 493.88,
            'C5': 523.25
        }
        
        # 创建一个简单的旋律序列
        melody_sequence = ['C4', 'E4', 'G4', 'C5', 'G4', 'E4', 'F4', 'A4', 'G4', 'E4', 'D4', 'C4']
        note_duration = 8.0  # 每个音符8秒
        
        music = np.zeros_like(t)
        
        for i, note_name in enumerate(melody_sequence):
            if i * note_duration >= self.duration:
                break
                
            freq = notes[note_name]
            start_time = i * note_duration
            end_time = min((i + 1) * note_duration, self.duration)
            
            # 找到对应时间段
            note_mask = (t >= start_time) & (t < end_time)
            note_t = t[note_mask] - start_time
            note_length = end_time - start_time
            
            # 生成清晰的正弦波音符
            note_wave = 0.3 * np.sin(2 * np.pi * freq * note_t)
            
            # 添加和声 (五度)
            harmony_freq = freq * 1.5
            note_wave += 0.15 * np.sin(2 * np.pi * harmony_freq * note_t)
            
            # 添加柔和的包络
            envelope = np.sin(np.pi * note_t / note_length)  # 柔和的起伏
            note_wave *= envelope
            
            music[note_mask] += note_wave
        
        # === 添加简单的背景层 ===
        
        # 低频背景 (模拟轻柔的无人机音)
        background = 0.08 * np.sin(2 * np.pi * 65.41 * t)  # C2
        background += 0.06 * np.sin(2 * np.pi * 98.00 * t)  # G2
        
        # 应用缓慢变化的包络
        background_envelope = 0.5 + 0.3 * np.sin(2 * np.pi * 0.1 * t)
        background *= background_envelope
        
        music += background
        
        # === 添加非常轻柔的高频装饰 ===
        
        # 简单的高频装饰音 (模拟风铃)
        decoration = np.zeros_like(t)
        decoration_freq = 1046.50  # C6
        
        # 每20秒一个装饰音
        for i in range(0, int(self.duration), 20):
            if i + 2 < self.duration:
                dec_mask = (t >= i) & (t < i + 2)
                dec_t = t[dec_mask] - i
                
                dec_wave = 0.05 * np.sin(2 * np.pi * decoration_freq * dec_t)
                dec_envelope = np.exp(-dec_t / 1.0)  # 快速衰减
                dec_wave *= dec_envelope
                
                decoration[dec_mask] += dec_wave
        
        music += decoration
        
        # === 音频后处理 ===
        
        # 应用主包络 (淡入淡出)
        fade_duration = 3.0  # 3秒淡入淡出
        fade_samples = int(fade_duration * self.sample_rate)
        
        # 淡入
        if len(music) > fade_samples:
            fade_in = np.linspace(0, 1, fade_samples)
            music[:fade_samples] *= fade_in
        
        # 淡出
        if len(music) > fade_samples:
            fade_out = np.linspace(1, 0, fade_samples)
            music[-fade_samples:] *= fade_out
        
        # 标准化音量 (避免削峰和过小声音)
        max_amplitude = np.max(np.abs(music))
        if max_amplitude > 0:
            music = music / max_amplitude * 0.6  # 60%音量，避免削峰
        
        print(f"✅ 音乐生成完成，最大振幅: {max_amplitude:.3f}")
        
        return music
    
    def save_as_wav(self, audio_data, filename):
        """保存为WAV文件"""
        print(f"💾 保存音频文件: {filename}")
        
        # 确保音频数据在有效范围内
        audio_data = np.clip(audio_data, -1.0, 1.0)
        
        # 转换为16位整数
        audio_int16 = (audio_data * 32767).astype(np.int16)
        
        # 创建立体声 (双声道相同内容)
        stereo_audio = np.column_stack((audio_int16, audio_int16))
        
        # 保存WAV文件
        with wave.open(filename, 'w') as wav_file:
            wav_file.setnchannels(2)  # 立体声
            wav_file.setsampwidth(2)  # 16位
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(stereo_audio.tobytes())
        
        print(f"✅ 音频文件已保存: {filename}")
        
        # 显示文件信息
        file_size = os.path.getsize(filename) / (1024 * 1024)
        print(f"📊 文件大小: {file_size:.1f} MB")
        print(f"⏱️ 时长: {self.duration} 秒")
        print(f"🎵 采样率: {self.sample_rate} Hz")
        print(f"🔊 16位立体声WAV格式")
    
    def generate_music(self, output_path="music/nature_simple.wav"):
        """生成完整的音乐"""
        print("🎵🌳 生成简单优美的自然音乐")
        print("=" * 50)
        
        # 确保music目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 生成音乐
        audio = self.generate_simple_melody()
        
        # 保存文件
        self.save_as_wav(audio, output_path)
        
        print("=" * 50)
        print("🌟 简单自然音乐生成完成！")
        print("🎵 清晰的C大调旋律")
        print("🌿 柔和的背景音")
        print("✨ 轻柔的装饰音")
        print("💎 无噪音，纯净音质")
        
        return output_path

def main():
    """主函数"""
    print("🌳🎵 简单自然音乐生成器 (修复版)")
    print("专门解决噪音问题，生成纯净音乐")
    print("-" * 40)
    
    try:
        generator = SimpleNatureMusicGenerator()
        audio_file = generator.generate_music()
        
        print(f"\n🎉 成功！纯净音乐文件已生成:")
        print(f"📁 {audio_file}")
        print(f"\n💡 这次应该是清晰的音乐，不再是噪音！")
        
    except Exception as e:
        print(f"❌ 生成音乐时出错: {e}")

if __name__ == "__main__":
    main()