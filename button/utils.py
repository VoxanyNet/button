def format_elapsed_time(seconds):

    seconds = int(seconds)
    
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    time_parts = []
    if days:
        time_parts.append(f"{days} {'day' if days == 1 else 'days'}")
    if hours:
        time_parts.append(f"{hours} {'hour' if hours == 1 else 'hours'}")
    if minutes:
        time_parts.append(f"{minutes} {'minute' if minutes == 1 else 'minutes'}")
    if seconds:
        time_parts.append(f"{seconds} {'second' if seconds == 1 else 'seconds'}")

    formatted_time = ', '.join(time_parts)

    return formatted_time

def format_elapsed_time_short(seconds):

    seconds = int(seconds)

    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    time_parts = []
    if days:
        time_parts.append(f"{days} {'day' if days == 1 else 'days'}")
    elif hours:
        time_parts.append(f"{hours} {'hour' if hours == 1 else 'hours'}")
    elif minutes:
        time_parts.append(f"{minutes} {'minute' if minutes == 1 else 'minutes'}")
    elif seconds:
        time_parts.append(f"{seconds} {'second' if seconds == 1 else 'seconds'}")
    else:
        time_parts.append("0 seconds")

    formatted_time = ', '.join(time_parts)

    return formatted_time

