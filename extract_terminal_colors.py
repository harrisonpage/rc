#!/usr/bin/env python3
#
# Extract terminal colors used in Terminal.app
#

import plistlib
import os

plist_path = os.path.expanduser('~/Library/Preferences/com.apple.Terminal.plist')

with open(plist_path, 'rb') as f:
    plist_data = plistlib.load(f)

themes_with_colors = []

if 'Window Settings' in plist_data:
    for theme_name, settings in plist_data['Window Settings'].items():
        if 'BackgroundColor' in settings:
            try:
                # The BackgroundColor is itself a binary plist (NSKeyedArchiver format)
                color_plist = settings['BackgroundColor']
                color_data = plistlib.loads(color_plist)

                # Navigate the NSKeyedArchiver structure
                if '$objects' in color_data:
                    for obj in color_data['$objects']:
                        if isinstance(obj, dict) and 'NSRGB' in obj:
                            rgb_bytes = obj['NSRGB']
                            # It's bytes, decode to string
                            rgb_str = rgb_bytes.decode('utf-8').strip('\x00')
                            # Parse "0.123 0.456 0.789" format
                            parts = rgb_str.split()
                            if len(parts) >= 3:
                                r = int(float(parts[0]) * 255)
                                g = int(float(parts[1]) * 255)
                                b = int(float(parts[2]) * 255)
                                hex_color = f"{r:02X}{g:02X}{b:02X}"
                                themes_with_colors.append((theme_name, hex_color))
                                break
            except Exception as e:
                pass

# Get unique colors
seen_colors = {}
for theme, color in sorted(themes_with_colors):
    if color not in seen_colors:
        seen_colors[color] = theme

# Print unique colors sorted by theme name
for color, theme in sorted(seen_colors.items(), key=lambda x: x[1]):
    print(f"{color} - {theme}")
