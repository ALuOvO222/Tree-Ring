# Tree Ring Animation - "Flower Playing"

An elegant tree ring growth animation program that combines natural music with real environmental data, presenting 34 years (1990-2023) of tree growth.

## Preview

### Animation Demo
![Tree Ring Animation](tree_ring_animation.gif)

### Static Preview
![Tree Ring Preview](tree_ring_preview.png)

## Features

### Music-Animation Synchronization
- Pure natural music: C major harmony, 120-second loop
- Beat synchronization: Tree ring growth perfectly synced with music beats
- Emotional expression: Music emotional intensity affects ring color changes

### Natural Color System
- Realistic tones: Brown and green natural tree colors
- Concentric design: Clear ring layers without overlap
- Dynamic gradients: Smooth color transitions based on environmental factors

### Real Data Simulation
- 34 years of data: Tree ring growth records from 1990-2023
- Environmental factors: Thickness, density, growth rate, climate pressure
- Year synchronization: Year display synchronized with music beats

### Optimized Interface
- 1200x800 resolution: Clear visual experience
- Real-time info panel: Year, progress, growth data
- Rhythm visualization: Beat and Emotion intensity bars (overlap issue fixed)
- Simple controls: [SPACE] Play/Pause [R] Restart [Q] Exit

## Quick Start

### Download from GitHub

#### Method 1: Git Clone (Recommended)
```bash
# Clone project locally
git clone https://github.com/ALuOvO222/Tree-Ring.git

# Enter project directory
cd Tree-Ring
```

#### Method 2: Direct Download
1. Visit https://github.com/ALuOvO222/Tree-Ring
2. Click the green "Code" button
3. Select "Download ZIP"
4. Extract the downloaded file

### Environment Setup

#### Install Python Dependencies
```bash
# Install core dependencies
pip install pygame numpy

# Or use requirements file (if available)
pip install -r requirements.txt
```

#### Python Version Requirements
- Python 3.7+ (Python 3.9+ recommended)
- Tested version: Python 3.13.5

### Run Program

```bash
# Run in project directory
python gui_tree_ring.py
```

#### Audio Options
The program will display 4 options on startup:
1. **No audio** - Animation and beat simulation only
2. **Pure natural music** (Recommended) - 120-second C major natural music
3. **Forest ambient** - Environmental sounds (if available)
4. **Custom path** - Use your own music file

**Option 2 is recommended for the best experience!**

## Project Files

```
Tree-Ring/
├── gui_tree_ring.py           # Main program - Complete GUI interface
├── tree_ring_data.json        # 34 years of real tree ring data
├── simple_music_generator.py  # Natural music generator
├── music/
│   └── nature_simple.wav      # Natural music file (120s)
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

## Controls

### Program Controls:
- **SPACE** - Play/pause animation
- **R** - Restart animation
- **Q or ESC** - Exit program
- **Mouse click close button** - Normal exit

### Interface Description
- **Left area** - Tree ring animation main display
- **Top right panel** - Current year, progress, tree ring data info
- **Bottom right bars** - Beat and Emotion intensity visualization

## Troubleshooting

### Common Issues

#### "ModuleNotFoundError: No module named 'pygame'"
```bash
# Solution: Install pygame
pip install pygame
```

#### "ModuleNotFoundError: No module named 'numpy'"
```bash
# Solution: Install numpy
pip install numpy
```

#### Audio playback issues
- Check system audio devices are working
- Try option 1 (no audio mode)
- Ensure `music/nature_simple.wav` file exists

#### Window display issues
- Ensure monitor resolution supports 1200x800
- Check graphics driver updates
- Try updating pygame: `pip install --upgrade pygame`

#### Python version compatibility
- Use Python 3.9+ recommended
- Check Python version: `python --version`
- Update if using older versions

### System Requirements
- **OS**: Windows 10+, macOS 10.14+, Linux
- **Python**: 3.7+ (3.9+ recommended)
- **Memory**: At least 512MB available memory
- **Display**: Support 1200x800 resolution
- **Audio**: WAV format support (optional)

## Technical Implementation

- **pygame 2.6.1**: Smooth 2D graphics rendering
- **Concentric algorithm**: Clear 10px spaced ring structure
- **HSV color space**: Natural brown-green tone transitions
- **Real-time audio sync**: pygame.mixer audio engine
- **Data-driven animation**: JSON structured data format

## Project Highlights

- Visual optimization complete - Natural colored concentric rings, no overlap
- Audio synchronization complete - Beat and ring growth precisely synced
- Interface layout complete - Beat/Emotion label spacing optimized
- Data display complete - 34 years real environmental data visualization
- Project cleanup complete - Core functionality files only
- Cross-platform support - Windows/macOS/Linux compatible
- Ready to use - Download and run, no complex configuration

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Ensure all dependencies are correctly installed
3. Submit an Issue in the GitHub repository

---

*Listen to the story of life's rings in the digital world*  
**Enjoy your tree ring animation journey!**