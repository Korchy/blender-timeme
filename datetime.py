# Nikita Akimov
# interplanety@interplanety.org


class DateTime:

    @staticmethod
    def deltatimetostr(seconds):
        days = divmod(seconds, 86400)
        hours = divmod(days[1], 3600)
        minutes = divmod(hours[1], 60)
        if days[0] > 0:
            return '%s d %s h %s m' % (days[0], hours[0], minutes[0])
        elif hours[0] > 0:
            return '%s h %s m' % (hours[0], minutes[0])
        else:
            return '%s m' % (minutes[0])
