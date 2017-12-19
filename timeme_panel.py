# Nikita Akimov
# interplanety@interplanety.org

import bpy
from . import timeme


class TimeMeCatsList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        layout.label("", icon="COLOR")
        layout.prop(item, "catname", '')
        layout.prop(item, "cattime", '')


class TimeMe_panel(bpy.types.Panel):
    bl_idname = 'timeme.panel'
    bl_label = 'TimeMe'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'

    def draw(self, context):
        # self.layout.operator('uv_int.separate_meshloops', icon = 'UNLINKED', text = 'Blast')
        # self.layout.operator('uv_int.separate_meshloops_by_edge', icon = 'UNLINKED', text = 'Seam by edge')
        self.layout.prop(bpy.context.scene.timeMeVars, 'cats')

        self.layout.template_list('TimeMeCatsList', 'Time Categories', bpy.context.scene.timeMeVars1, 'cats', bpy.context.scene.timeMeVars1, 'activecat', type='DEFAULT')

        self.layout.operator('timeme.print', icon = 'LINKED', text = 'Print')
        pass


def register():
    bpy.utils.register_class(TimeMe_panel)
    bpy.utils.register_class(TimeMeCatsList)


def unregister():
    bpy.utils.unregister_class(TimeMe_panel)
    bpy.utils.unregister_class(TimeMeCatsList)
