# Bongo Cat Auto Typer

A fun and user-friendly automatic typing application featuring a Bongo Cat theme. This tool simulates pressing the F13 key at configurable intervals to automate repetitive keyboard tasks.

## Features

- Modern, gentle UI design with a Bongo Cat theme
- Configurable typing parameters:
  - Number of types to perform
  - Interval between types (in seconds)
- Real-time progress tracking
- Estimated completion time with both duration and end time
- Visual progress bar
- Start and stop controls
- Warning about F13 macro conflicts

## Requirements

- Windows OS (since F13 key support is needed)
- Python 3.6+

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/bongo-cat-auto-typer.git
   cd bongo-cat-auto-typer
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

To run the application directly with Python:
```
python auto_click_gui.py
```

### Building the Executable

To build a standalone executable:
```
pyinstaller build.spec
```

Or use the batch script:
```
build_exe.bat
```

The executable will be created in the `dist/` folder as `BongoCat_AutoTyper.exe`.

## Files in the Repository

- `auto_click_gui.py` - Main application source code with GUI and typing logic
- `build.spec` - PyInstaller configuration file for building the executable
- `build_exe.bat` - Batch script to build the executable
- `requirements.txt` - List of dependencies needed for the application
- `bongo_cat.png` and `bongo_cat.ico` - Application assets (images/icons)
- `README.md` - This file

## Dependencies

The application relies on the following Python packages:
- `pynput==1.7.6` - For simulating keyboard inputs
- `PIL (Pillow)` - For image processing
- `tkinter` - For the GUI (built-in with Python)

## How It Works

The application creates a graphical interface that allows users to configure how many times to simulate pressing the F13 key and at what intervals. When started, it uses the pynput library to programmatically press and release the F13 key according to the user's settings.

## Important Notes

- This application is designed specifically for Windows systems that support the F13 key
- Make sure to avoid using F13 as a macro while running this application
- The program simulates keyboard input, which may trigger other applications or macros

## Contributing

Feel free to submit issues and enhancement requests. Pull requests are welcome!

## License

[Specify your license here]