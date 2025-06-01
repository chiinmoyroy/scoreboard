# GitHub Actions - Free Executable Builder

## Step-by-Step Guide to Get Your .exe File

### Step 1: Create GitHub Account
1. Go to github.com
2. Click "Sign up" (completely free)
3. Choose a username and create account

### Step 2: Create New Repository
1. Click the "+" icon in top right
2. Select "New repository"
3. Name it: `cricket-scoreboard`
4. Make it Public (required for free builds)
5. Click "Create repository"

### Step 3: Upload Your Files
Upload these files to your repository:
- `gui_app.py`
- `main.py`
- `run_app.bat`
- `run_app.sh`
- `sample_match.yaml`
- `README_DISTRIBUTION.md`
- `.github/workflows/build-executable.yml` (I created this for you)

**How to Upload:**
1. Click "uploading an existing file"
2. Drag and drop all files
3. Type commit message: "Add cricket scoreboard application"
4. Click "Commit changes"

### Step 4: Automatic Build Process
Once files are uploaded:
1. GitHub automatically detects the workflow file
2. Starts building your Windows executable
3. Takes about 5-10 minutes to complete

### Step 5: Download Your .exe File

**Option A - From Actions Tab:**
1. Click "Actions" tab in your repository
2. Click the latest build (green checkmark)
3. Scroll down to "Artifacts"
4. Download "CricketScoreboard-Windows"
5. Unzip to get your .exe file

**Option B - From Releases:**
1. Click "Releases" on the right side
2. Download the latest release
3. Contains your ready-to-use .exe file

### What You Get
- `CricketScoreboard.exe` (about 50-100 MB)
- Standalone executable that runs on any Windows computer
- No Python installation required
- Professional cricket analysis software

### File Structure for Upload
```
your-repository/
├── gui_app.py
├── main.py
├── run_app.bat
├── run_app.sh
├── sample_match.yaml
├── README_DISTRIBUTION.md
└── .github/
    └── workflows/
        └── build-executable.yml
```

### Troubleshooting
- Build fails? Check that all files are uploaded correctly
- No exe file? Wait for build to complete (green checkmark in Actions)
- Can't find download? Look in Actions tab under Artifacts

This process is completely free and will give you the compiled Windows executable you need for your lower-end PC.