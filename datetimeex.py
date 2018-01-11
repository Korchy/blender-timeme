# Nikita Akimov
# interplanety@interplanety.org


class DateTimeEx:

    @staticmethod
    def deltatimetostrDHM(seconds):
        days = divmod(seconds, 86400)
        hours = divmod(days[1], 3600)
        minutes = divmod(hours[1], 60)
        if days[0] > 0:
            return '%s d %s h %s m' % (int(days[0]), int(hours[0]), int(minutes[0]))
        elif hours[0] > 0:
            return '%s h %s m' % (int(hours[0]), int(minutes[0]))
        else:
            return '%s m' % (int(minutes[0]))

    @staticmethod
    def deltatimetostrDHMS(seconds):
        days = divmod(seconds, 86400)
        hours = divmod(days[1], 3600)
        minutes = divmod(hours[1], 60)
        if days[0] > 0:
            return '%s d %s h %s m %s s' % (int(days[0]), int(hours[0]), int(minutes[0]), int(minutes[1]))
        elif hours[0] > 0:
            return '%s h %s m %s s' % (int(hours[0]), int(minutes[0]), int(minutes[1]))
        else:
            return '%s m %s s' % (int(minutes[0]), int(minutes[1]))
