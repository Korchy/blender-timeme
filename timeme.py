# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender-timeme

import bpy
import datetime
from .datetimeex import DateTimeEx
from bpy.app.handlers import persistent
from bpy.props import FloatProperty, StringProperty, IntProperty, CollectionProperty, PointerProperty
from bpy.types import Operator, PropertyGroup
from bpy.utils import register_class, unregister_class
import os


class TIMEME_OT_start(Operator):
    bl_idname = 'timeme.start'
    bl_label = 'TimeMe: Start'
    bl_description = 'Start TimeMe monitor'

    _status = None
    _events_list = []
    _current_time = datetime.datetime.now()
    _current_window_active = True
    _current_render_time = None
    _current_autosave_time = datetime.datetime.now()
    _check_interval = 1  # sec
    _work_time_damping = 10  # sec

    def execute(self, context):
        if self._status:     # prevent double run
            return {'FINISHED'}
        __class__.start()
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if self._status:
            if event.type not in self._events_list:
                self._events_list.append(event.type)
            # check window deactivation - activation
            if event.type == 'WINDOW_DEACTIVATE':
                self._current_window_active = False
            elif (not self._current_window_active) and event.type not in ['MOUSEMOVE', 'INBETWEEN_MOUSEMOVE', 'NONE'] and event.type[:5] not in ['TIMER', 'NDOF_']:
                self._current_window_active = True
            # count time by categories
            if datetime.datetime.now() - datetime.timedelta(seconds=self._check_interval) > self._current_time:
                # ALL TIME
                __class__._increase_category_time(context=context, category_name='ALL TIME', time_interval=(datetime.datetime.now() - self._current_time))
                # ACTIVE TIME
                if self._current_window_active:
                    __class__._increase_category_time(context=context, category_name='ACTIVE TIME', time_interval=(datetime.datetime.now() - self._current_time))
                # WORK TIME
                work_event = any((event not in ['NONE', 'WINDOW_DEACTIVATE'] and event[:5] not in ['TIMER', 'NDOF_']) for event in self._events_list)
                if work_event and self._current_window_active:
                    if datetime.datetime.now() - datetime.timedelta(seconds=self._work_time_damping) > self._current_time:
                        time = datetime.timedelta(seconds=self._work_time_damping)
                    else:
                        time = datetime.datetime.now() - self._current_time
                    __class__._increase_category_time(context=context, category_name='WORK TIME', time_interval=time)
                # wait for new events
                self._current_time = datetime.datetime.now()
                del self._events_list[:]
                # redraw
                __class__._redraw(context=context)
                # check autosave
                if context.preferences.filepaths.use_auto_save_temporary_files and context.preferences.addons[__package__].preferences.use_timeme_auto_save:
                    if datetime.datetime.now() - datetime.timedelta(minutes=context.preferences.filepaths.auto_save_time) > self._current_autosave_time:
                        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(context.preferences.filepaths.temporary_directory, __class__.project_name()), copy=True, check_existing=False)
                        self._current_autosave_time = datetime.datetime.now()
            return {'PASS_THROUGH'}
        else:
            return {'FINISHED'}

    @staticmethod
    def start():
        if not __class__._status:
            __class__._reset()
            if __class__._timeme_render_init not in bpy.app.handlers.render_init:
                bpy.app.handlers.render_init.append(__class__._timeme_render_init)
            if __class__._timeme_render_complete not in bpy.app.handlers.render_complete:
                bpy.app.handlers.render_complete.append(__class__._timeme_render_complete)
            if __class__._timeme_render_cancel not in bpy.app.handlers.render_cancel:
                bpy.app.handlers.render_cancel.append(__class__._timeme_render_cancel)
            __class__._status = 'RUNNING'

    @staticmethod
    def stop(context):
        if __class__._status:
            __class__._status = None
            if hasattr(bpy.types.Scene, 'timeme_vars'):
                __class__.clear(context=context)
                del bpy.types.Scene.timeme_vars
        if __class__._timeme_render_init in bpy.app.handlers.render_init:
            bpy.app.handlers.render_init.remove(__class__._timeme_render_init)
        if __class__._timeme_render_complete in bpy.app.handlers.render_complete:
            bpy.app.handlers.render_complete.remove(__class__._timeme_render_complete)
        if __class__._timeme_render_cancel in bpy.app.handlers.render_cancel:
            bpy.app.handlers.render_cancel.remove(__class__._timeme_render_cancel)

    @staticmethod
    def _reset():
        # reset timeme data
        bpy.types.Scene.timeme_vars = PointerProperty(type=TimeMeVars)
        __class__._current_time = datetime.datetime.now()

    @staticmethod
    def clear(context):
        # remove all categories from list
        context.scene.timeme_vars.categories.clear()

    @staticmethod
    def _redraw(context=None):
        areas = context.screen.areas if context and context.screen else bpy.data.window_managers[0].windows[0].screen.areas
        for area in areas:
            if area.type == 'PROPERTIES':
                area.tag_redraw()

    @staticmethod
    def _add_category(context, category_name):
        # add new category to list
        new_category = context.scene.timeme_vars.categories.add()
        new_category.category_name = category_name
        new_category.category_time = datetime.timedelta().total_seconds()
        new_category.category_time_str = DateTimeEx.deltatimetostrDHMS(new_category.category_time)
        return new_category

    @staticmethod
    def _get_category(context, category_name):
        # return category from list by name (creates if not exists)
        category = next((c_category for c_category in context.scene.timeme_vars.categories if c_category.category_name == category_name), None)
        if not category:
            category = __class__._add_category(context=context, category_name=category_name)
        return category

    @staticmethod
    def _increase_category_time(context, category_name, time_interval):
        # increase category time
        if category_name and time_interval:
            category = __class__._get_category(context=context, category_name=category_name)
            category.category_time += time_interval.total_seconds()
            category.category_time_str = DateTimeEx.deltatimetostrDHMS(seconds=category.category_time)

    @staticmethod
    def _timeme_render_init(scene):
        __class__._current_render_time = datetime.datetime.now()

    @staticmethod
    def _timeme_render_complete(scene):
        if __class__._current_render_time:
            __class__._increase_category_time(context=bpy.context, category_name='RENDER TIME', time_interval=(datetime.datetime.now() - __class__._current_render_time))
            __class__._redraw()
            __class__._current_render_time = None

    @staticmethod
    def _timeme_render_cancel(scene):
        if bpy.context.preferences.addons[__package__].preferences.consider_canceled_rendering_time:
            __class__._timeme_render_complete(scene=scene)

    @staticmethod
    def get_text(context):
        text = '='*50 + '\n'
        text += '= Monitoring this project time by TimeMe = \n'
        text += '='*50 + '\n'
        text += 'PROJECT: ' + os.path.splitext(os.path.basename(bpy.data.filepath))[0] + '\n'
        for category in context.scene.timeme_vars.categories:
            text += (category.category_name + ': ' + category.category_time_str)+'\n'
        text += '='*50
        return text

    @staticmethod
    def project_name():
        # returns current project name
        if bpy.data.filepath:
            return os.path.splitext(os.path.basename(bpy.data.filepath))[0] + '.blend'
        else:
            return 'untitled.blend'

class TimeMePrint(Operator):
    bl_idname = 'timeme.print'
    bl_label = 'TimeMe: Print'
    bl_description = 'Print TimeMe statistic'

    def execute(self, context):
        text_obj = bpy.data.texts['TimeMe'] if 'TimeMe' in bpy.data.texts else bpy.data.texts.new(name='TimeMe')
        text_obj.from_string(TIMEME_OT_start.get_text(context=context))
        show_in_area = next((area for area in context.screen.areas if area.type == 'TEXT_EDITOR'), None)
        if not show_in_area:
            show_in_area = next((area for area in context.screen.areas if area.type not in ['PROPERTIES', 'INFO', 'OUTLINER']), None)
            if show_in_area:
                show_in_area.type = 'TEXT_EDITOR'
        if show_in_area:
            show_in_area.spaces.active.text = bpy.data.texts['TimeMe']
            bpy.data.texts['TimeMe'].current_line_index = 0
        return {'FINISHED'}


class TimeMeToClipboard(Operator):
    bl_idname = 'timeme.toclipboard'
    bl_label = 'TimeMe: ToClipboard'
    bl_description = 'Copy TimeMe statistic to clipboard'

    def execute(self, context):
        context.window_manager.clipboard = TIMEME_OT_start.get_text(context=context)
        return {'FINISHED'}


class TimeMeReset(Operator):
    bl_idname = 'timeme.reset'
    bl_label = 'Are you sure?'
    bl_description = 'Reset TimeMe statistic'

    def execute(self, context):
        TIMEME_OT_start.clear(context=context)
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=90)


class TimeMeCategoryItem(PropertyGroup):
    category_name: StringProperty(
        name='category_name',
        default=''
    )
    category_time: FloatProperty(
        name='category_time'
    )
    category_time_str: StringProperty(
        name='category_time'
    )


class TimeMeVars(PropertyGroup):
    categories: CollectionProperty(
        type=TimeMeCategoryItem,
        name='categories'
    )
    active_category: IntProperty(
        name='active_category',
        default=-1
    )


# starting an add-on (delayed to prevent errors)
@persistent
def timeme_depsgraph_update_post(scene):
    bpy.app.handlers.depsgraph_update_post.remove(timeme_depsgraph_update_post)
    bpy.ops.timeme.start()


@persistent
def timeme_timer_depsgraph_update():
        bpy.context.scene.cursor.location[0] = bpy.context.scene.cursor.location[0]

# restarting while reloading scene
@persistent
def timeme_load_pre(scene):
    TIMEME_OT_start.stop(context=bpy.context)


@persistent
def timeme_load_post(scene):
    bpy.ops.timeme.start()


# registering
def register():
    register_class(TimeMeCategoryItem)
    register_class(TimeMeVars)
    register_class(TIMEME_OT_start)
    register_class(TimeMePrint)
    register_class(TimeMeToClipboard)
    register_class(TimeMeReset)
    if timeme_load_pre not in bpy.app.handlers.load_pre:
        bpy.app.handlers.load_pre.append(timeme_load_pre)
    if timeme_load_post not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(timeme_load_post)
    # start
    if timeme_depsgraph_update_post not in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(timeme_depsgraph_update_post)
    bpy.app.timers.register(timeme_timer_depsgraph_update, first_interval=1.0)


def unregister():
    TIMEME_OT_start.stop(context=bpy.context)
    if timeme_load_pre in bpy.app.handlers.load_pre:
        bpy.app.handlers.load_pre.remove(timeme_load_pre)
    if timeme_load_post in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(timeme_load_post)
    unregister_class(TimeMeReset)
    unregister_class(TimeMeToClipboard)
    unregister_class(TimeMePrint)
    unregister_class(TIMEME_OT_start)
    unregister_class(TimeMeVars)
    unregister_class(TimeMeCategoryItem)
