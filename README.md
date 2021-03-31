# TimeMe
Blender add-on for fixing the time of making your projects.

Author: Nikita Akimov interplanety@interplanety.org

<a href="https://b3d.interplanety.org/en/blender-timeme/">Add-on web page</a>

<img src="https://b3d.interplanety.org/wp-content/upload_content/2017/12/00-1-400x212.jpg" title="TimeMe">

### Current version

**1.4.0. (for Blender 2.8x, 2,9x)**

Version 1.1.2. for Blender 2.7x is frozen. You can get the last release <a href = "https://github.com/Korchy/blender-timeme/releases/tag/v1.1.2">here</a>. 

### Installation

User Preferences - Add-ons - Install Add-on from File - select distributive archive

### Location

"Properties" window - "Render" tab - "TimeMe" subtab

### Usage

The add-on works in the background, fixing the project developing time.

<img src="https://b3d.interplanety.org/wp-content/upload_content/2018/01/02-400x212.jpg">

### Options

***Enable autosave with TimeMe***

System autosave doesn't work with running TimeMe. To fix this you can use the built-in TimeMe autosave. To do this - check the "Enable autosave with TimeMe" checkbox in the add-on preferences. 

***Consider canceled rendering time***

Check this option if you want to add time of cancelled renderings to the "RENDER TIME" category. 

### Version history

1.4.0.
- Added custom directory for TimeMe autosaves to fix permissions problems

1.3.0.
- Added the "Pause - Resume" option

1.2.0.
- Ported to Blender 2.80. Version for 2.7x frozen.
- Added new monitoring category "ACTIVE TIME" - time with main Blender window being active
- Fixed broken autosaves with built-in autosave option

1.1.2
- Enable counting the mouse move event in work time category
- Work time damping time added 

1.1.1
- Added project name to statistic text

1.1.0
- Seconds accuracy enabled
- Added Copy to clipboard function
- Added Reset time function

1.0.0
- This release
