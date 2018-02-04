# Nikita Akimov
# interplanety@interplanety.org

bl_info = {
    'name': 'TimeMe',
    'category': 'System',
    'author': 'Nikita Akimov',
    'version': (1, 1, 1),
    'blender': (2, 79, 0),
    'location': 'Properties window - Render tab - TimeMe subpanel',
    'wiki_url': 'https://b3d.interplanety.org/en/blender-timeme/',
    'tracker_url': 'https://b3d.interplanety.org/en/blender-timeme/',
    'description': 'TimeMe - add-on to manage the project time'
}

from . import timeme
from . import timeme_panel
import bpy
from bpy.app.handlers import persistent

@persistent
def onsceneupdatepost(scene):
    bpy.app.handlers.scene_update_post.remove(onsceneupdatepost)
    bpy.ops.timeme.start()


def register():
    timeme.register()
    timeme_panel.register()
    if onsceneupdatepost not in bpy.app.handlers.scene_update_post:
        bpy.app.handlers.scene_update_post.append(onsceneupdatepost)


def unregister():
    if onsceneupdatepost in bpy.app.handlers.scene_update_post:
        bpy.app.handlers.scene_update_post.remove(onsceneupdatepost)
    timeme.unregister()
    timeme_panel.unregister()


if __name__ == '__main__':
    register()
