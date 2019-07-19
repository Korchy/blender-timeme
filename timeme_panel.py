# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender-timeme

from bpy.types import Panel, UIList
from bpy.utils import register_class, unregister_class


class TIMEME_UL_cats_list(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index=0, flt_flag=0):
        layout.label(text=item.category_name)
        layout.label(text=item.category_time_str)


class TIMEME_PT_panel(Panel):
    bl_idname = 'TIMEME_PT_panel'
    bl_label = 'TimeMe'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'

    def draw(self, context):
        if hasattr(context.scene, 'timeme_vars'):
            layout = self.layout
            layout.template_list('TIMEME_UL_cats_list', 'Time Categories', context.scene.timeme_vars, 'categories', context.scene.timeme_vars, 'active_category', rows=3, type='DEFAULT')
            row = layout.row()
            row.operator('timeme.print', icon='FILE_TEXT', text='To Text')
            row.operator('timeme.toclipboard', icon='COPYDOWN', text='To Clipboard')
            row.operator('timeme.reset', icon='X', text='Reset')


def register():
    register_class(TIMEME_PT_panel)
    register_class(TIMEME_UL_cats_list)


def unregister():
    unregister_class(TIMEME_PT_panel)
    unregister_class(TIMEME_UL_cats_list)
