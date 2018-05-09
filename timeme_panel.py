# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender-timeme

import bpy


class TimeMeCatsList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        layout.label(item.catname)
        layout.label(item.cattime_str)


class TimeMe_panel(bpy.types.Panel):
    bl_idname = 'timeme.panel'
    bl_label = 'TimeMe'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'

    def draw(self, context):
        if hasattr(bpy.context.scene, 'timeMeVars'):
            self.layout.template_list('TimeMeCatsList', 'Time Categories', bpy.context.scene.timeMeVars, 'cats', bpy.context.scene.timeMeVars, 'activecat', rows=3, type='DEFAULT')
            row = self.layout.row()
            row.operator('timeme.print', icon='FILE_TEXT', text='To Text')
            row.operator('timeme.toclipboard', icon='COPYDOWN', text='To Clipboard')
            row.operator('timeme.reset', icon='X', text='Reset')
        pass


def register():
    bpy.utils.register_class(TimeMe_panel)
    bpy.utils.register_class(TimeMeCatsList)


def unregister():
    bpy.utils.unregister_class(TimeMe_panel)
    bpy.utils.unregister_class(TimeMeCatsList)
