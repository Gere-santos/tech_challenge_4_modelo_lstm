from datetime import timedelta

def next_business_day(date):
    next_day = date + timedelta(days=1)

    while next_day.weekday() >= 5: 
        next_day += timedelta(days=1)

    return next_day