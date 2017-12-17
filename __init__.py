# Nikita Akimov
# interplanety@interplanety.org

bl_info = {
    'name': 'TimeMe',
    'category': 'System',
    'author': 'Nikita Akimov',
    'version': (1, 0, 0),
    'blender': (2, 79, 0),
    'location': '',
    'wiki_url': '',
    'tracker_url': '',
    'description': 'TimeMe - add-on to manage work time'
}

from . import timeme
from . import timeme_panel


def register():
    timeme.register()
    timeme_panel.register()


def unregister():
    timeme.unregister()
    timeme_panel.unregister()


if __name__ == "__main__":
    register()
