from datetime import timedelta
from django.utils import timezone


# downtime calculation
def calc_downtime(start, end=None):
    end = end or timezone.now()
    total_minutes = int((end - start).total_seconds() // 60)
    if total_minutes >= 24 * 60:
        return f'{total_minutes // (24 * 60)}d'
    hours = total_minutes // 60
    minutes = total_minutes % 60
    if hours == 0:
        return f'{minutes}m'
    if minutes == 0:
        return f'{hours}h'
    return f'{hours}h {minutes}m'

# def minutes_between(start, end=None):
#     end = end or timezone.now()
#     return round((end - start).total_seconds() / 3600, 1)

# TODO repair/models.py @prperty calculation with input data.


def repair_stats(repairs):
    now = timezone.now()
    total_downtime = timedelta()
    total_cost = 0
    open_count = 0

    for repair in repairs:
        total_downtime += (repair.downtime_end or now) - repair.detected_on
        total_cost += repair.cost
        if repair.status == 'Open':
            open_count += 1

    return {
        'repairs_count': len(repairs),
        'open_repairs_count': open_count,
        'total_downtime': calc_downtime(now - total_downtime, now),
        'total_cost': total_cost,
    }