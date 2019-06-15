# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender-timeme

from .addon import Addon
from . import timeme
from . import timeme_panel
import bpy
from bpy.app.handlers import persistent

bl_info = {
    'name': 'TimeMe',
    'category': 'System',
    'author': 'Nikita Akimov',
    'version': (1, 1, 2),
    'blender': (2, 79, 0),
    'location': 'Properties window - Render tab - TimeMe subpanel',
    'wiki_url': 'https://b3d.interplanety.org/en/blender-timeme/',
    'tracker_url': 'https://b3d.interplanety.org/en/blender-timeme/',
    'description': 'TimeMe - add-on to manage the project time'
}


@persistent
def onsceneupdatepost(scene):
    bpy.app.handlers.scene_update_post.remove(onsceneupdatepost)
    bpy.ops.timeme.start()


def register():
    if not Addon.dev_mode():
        timeme.register()
        timeme_panel.register()
        if onsceneupdatepost not in bpy.app.handlers.scene_update_post:
            bpy.app.handlers.scene_update_post.append(onsceneupdatepost)
    else:
        print('It seems you are trying to use the dev version of the ' + bl_info['name'] + ' add-on. It may work not properly. Please download and use the release version!')


def unregister():
    if not Addon.dev_mode():
        if onsceneupdatepost in bpy.app.handlers.scene_update_post:
            bpy.app.handlers.scene_update_post.remove(onsceneupdatepost)
        timeme.unregister()
        timeme_panel.unregister()


if __name__ == '__main__':
    register()
