from django import template
from common.utils import calc_downtime

register = template.Library()

@register.filter
def downtime(repair):
    return calc_downtime(repair.detected_on, repair.downtime_end)