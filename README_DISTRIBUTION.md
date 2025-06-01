# Cricket Scoreboard Analyzer - Free Distribution

## Download and Run (No Installation Required)

### Quick Start
1. Download all project files
2. Make sure you have Python installed (free from python.org)
3. Open command prompt/terminal in the project folder
4. Run: `pip install pyyaml`
5. Run: `python gui_app.py`

### What You Get
- Professional cricket statistics analyzer
- Modern tabbed interface
- Comprehensive batting and bowling analysis
- Team totals and match information
- Support for standard cricket YAML data files

## System Requirements
- Windows, macOS, or Linux
- Python 3.7 or higher (free download)
- 50 MB free disk space
- Internet connection for initial setup only

## File Structure
```
CricketScoreboard/
├── gui_app.py              # Main application
├── main.py                 # Cricket analysis engine
├── sample_match.yaml       # Test data file
├── README_DISTRIBUTION.md  # This file
├── INSTALLATION.md         # Detailed setup guide
└── build_executable.py     # Optional: Create .exe file
```

## Usage Instructions

### 1. Basic Setup
```bash
# Install Python dependency
pip install pyyaml

# Run the application
python gui_app.py
```

### 2. Loading Cricket Data
- Click "Load YAML File" in the application
- Browse to your cricket match YAML file
- View comprehensive statistics in the tabs

### 3. Creating Windows Executable (Optional)
If you want a standalone .exe file:
```bash
pip install pyinstaller
python build_executable.py
```
This creates a single .exe file that runs without Python installation.

## Distribution Options

### Option 1: Share Project Files
- Zip all files and share
- Recipients follow Quick Start instructions
- Works on all operating systems

### Option 2: GitHub/GitLab
- Upload files to free repository
- Users can download and run
- Includes version control

### Option 3: Direct Sharing
- Share via email, USB, or cloud storage
- Include this README file
- Recipients get full application

## Features Included

### Cricket Analysis
- Ball-by-ball statistics processing
- Batting performance with strike rates
- Bowling figures with economy rates
- Dismissal details and how-out information
- Team totals and run rates

### User Interface
- Professional desktop application
- File browser for data selection
- Progress indicators during loading
- Error handling with clear messages
- Tabbed navigation between statistics

### Data Support
- Standard cricket YAML format
- Comprehensive error checking
- Support for ODI, T20, and Test matches
- Compatible with CricHQ and similar platforms

## Troubleshooting

### Python Not Found
- Download Python from python.org (free)
- During installation, check "Add Python to PATH"
- Restart command prompt after installation

### Missing PyYAML
```bash
pip install pyyaml
```

### Application Won't Start
- Ensure all files are in the same folder
- Check Python version: `python --version`
- Try: `python3 gui_app.py` on macOS/Linux

## Support
This is free software. For issues:
1. Check your YAML file format
2. Verify Python installation
3. Ensure all project files are present

## License
Free to use, modify, and distribute for cricket analysis purposes.