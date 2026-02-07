YourClient v2.6
A modular, lightweight interface framework designed for process-based injection and real-time HUD rendering. Built with Python and PyQt5, focusing on performance and a clean user experience.

Features
Process Detection: Automatic scanning for target instances using psutil.

Modular GUI: Categorized panels (Combat, Misc, Render, etc.) with foldable headers for space management.

Active HUD: A sleek, right-aligned overlay that lists enabled modules with status indicators.

Draggable Interface: Custom window management allowing users to arrange the workspace freely.

Self-Destruct: Clean exit and resource cleanup functionality.

Getting Started
Prerequisites
Python 3.x

PyQt5

psutil

Bash
pip install PyQt5 psutil
Installation
Clone the repository:

Bash
git clone https://github.com/YourUsername/YourClient.git
Navigate to the directory:

Bash
cd YourClient
Run the application:

Bash
python main.py
Configuration
To customize the client name or add new modules, modify the self.data dictionary in the CheatMenu class:

Python
self.data = {
    "NEW_CATEGORY": ["Module 1", "Module 2"],
    # ...
}
Build
To compile the project into a standalone executable:

Bash
pyinstaller --noconsole --onefile --icon=icon.ico main.py
License
Distributed under the MIT License. See LICENSE for more information.
