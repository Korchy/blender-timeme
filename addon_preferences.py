# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender-timeme

from bpy.types import AddonPreferences
from bpy.props import BoolProperty
from bpy.utils import register_class, unregister_class


class TIMEME_addon_preferences(AddonPreferences):
    bl_idname = __package__

    # consider cancelled render time
    consider_canceled_rendering_time: BoolProperty(
        name='Consider canceled rendering time',
        default=False
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'consider_canceled_rendering_time')


def register():
    register_class(TIMEME_addon_preferences)


def unregister():
    unregister_class(TIMEME_addon_preferences)
