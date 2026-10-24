from django.utils import timezone

# downtime calculation
def minutes_between(start, end=None):
    end = end or timezone.now()
    return int((end - start).total_seconds() // 60)

# TODO repair/models.py @prperty calculation with input data