# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender-timeme

from .addon import Addon
from . import addon_preferences
from . import timeme
from . import timeme_panel

bl_info = {
    'name': 'TimeMe',
    'category': 'System',
    'author': 'Nikita Akimov',
    'version': (1, 3, 0),
    'blender': (2, 80, 0),
    'location': 'Properties window - Render tab - TimeMe subpanel',
    'wiki_url': 'https://b3d.interplanety.org/en/blender-timeme/',
    'tracker_url': 'https://b3d.interplanety.org/en/blender-timeme/',
    'description': 'TimeMe - add-on to manage the project time'
}


def register():
    if not Addon.dev_mode():
        addon_preferences.register()
        timeme.register()
        timeme_panel.register()
    else:
        print('It seems you are trying to use the dev version of the ' + bl_info['name'] + ' add-on. It may work not properly. Please download and use the release version!')


def unregister():
    if not Addon.dev_mode():
        timeme.unregister()
        timeme_panel.unregister()
        addon_preferences.unregister()


if __name__ == '__main__':
    register()
