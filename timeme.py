# Nikita Akimov
# interplanety@interplanety.org

import bpy
import sys
import datetime
from . import datetime as dt

class TimeMe(bpy.types.Operator):
    bl_idname = 'timeme.start'
    bl_label = 'TimeMe: Start'
    bl_description = 'Start monitor my time'

    # timer = None
    status = None
    eventslist = []
    time = datetime.datetime.now()

    def modal(self, context, event):

        if event.type not in self.eventslist:
            self.eventslist.append(event.type)

        if event.type == 'Q':
            self.cancel(context)

        # whole time
        cat_whole = __class__.getcat('WHOLE TIME')
        # cat_whole.cattime = str(datetime.datetime.strptime(cat_whole.cattime, '%d:%H:%M') + (datetime.datetime.now() - self.time))

        if self.status:
            if datetime.datetime.now() - datetime.timedelta(seconds=10) > self.time:
                self.time = datetime.datetime.now()

                for event in self.eventslist:
                    pass

                # modified = False
                # for cat in bpy.context.scene.timeMeVars.cats:
                #     if cat.catname == event.type:
                #         cat.cattime = 'aa' # timedelta(microseconds=-1)
                #         modified = True
                # if not modified:
                #     newitem = bpy.context.scene.timeMeVars.cats.add()
                #     newitem.catname = event.type
                #     newitem.cattime = '00:00:00'

                del self.eventslist[:]


            return {'PASS_THROUGH'}
        else:
            return {'FINISHED'}

    def execute(self, context):
        context.window_manager.modal_handler_add(self)
        # self.timer = context.window_manager.event_timer_add(time_step=60)
        # self.timer = context.window_manager.event_timer_add(time_step=0.01)
        self.status = 'RUNNING'
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        __class__.clear()
        # context.window_manager.event_timer_remove(self.timer)
        self.status = None
        return {'CANCELLED'}

    # @classmethod
    # def geteventslist(cls):
    #     print(__class__.eventslist)
    #     return cls.eventslist

    # @staticmethod
    # def getCats(self, context):
    #     itemlist = []
    #     for i, key in enumerate(TimeMe.cats.keys()):
    #         itemlist.append((key, key, '', TimeMe.cats[key]))
    #     return itemlist

    # @staticmethod
    @classmethod
    def clear(cls):
        bpy.context.scene.timeMeVars.cats.clear()

    @classmethod
    def stop(cls):
        cls.status = None

    @staticmethod
    def getcat(catname):
        for cat in bpy.context.scene.timeMeVars.cats:
            if cat.catname == catname:
                return cat
        newcat = bpy.context.scene.timeMeVars.cats.add()
        newcat.catname = catname
        newcat.cattime = datetime.timedelta().total_seconds()
        newcat.cattime_str = dt.DateTime.deltatimetostr(newcat.cattime)
        return newcat


class TimeMePrint(bpy.types.Operator):
    bl_idname = 'timeme.print'
    bl_label = 'TimeMe: Print'

    def execute(self, context):
        print(TimeMe.eventslist)
        # print(TimeMe.geteventslist())
        # print(TimeMe.cats)
        # print('---')
        # for item in bpy.context.scene.timeMeVars.cats:
        #     print(item.catname, item.cattime)
        return {'FINISHED'}


class TimeMeCatsItem(bpy.types.PropertyGroup):
    catname = bpy.props.StringProperty(name='catname', default='')
    cattime = bpy.props.FloatProperty(name="cattime")
    cattime_str = bpy.props.StringProperty(name="cattime")


class TimeMeVars(bpy.types.PropertyGroup):
    cats = bpy.props.CollectionProperty(type=TimeMeCatsItem, name='cats')
    activecat = bpy.props.IntProperty(name='activecat', default=-1)


def register():
    bpy.utils.register_class(TimeMe)
    bpy.utils.register_class(TimeMePrint)
    bpy.utils.register_class(TimeMeCatsItem)
    bpy.utils.register_class(TimeMeVars)
    bpy.types.Scene.timeMeVars = bpy.props.PointerProperty(type=TimeMeVars)


def unregister():
    TimeMe.stop()
    TimeMe.clear()
    del bpy.types.Scene.timeMeVars
    bpy.utils.unregister_class(TimeMe)
    bpy.utils.unregister_class(TimeMePrint)
    bpy.utils.unregister_class(TimeMeCatsItem)
    bpy.utils.unregister_class(TimeMeVars)
