import os

def print_tabular(data):
    keys_to_print = ['dataset_name', 'id']
    print('\t '.join(keys_to_print))
    # Print rows
    for item in data:
        print('\t '.join(str(item[key]) for key in keys_to_print if key in item))

def format_time(seconds):
    time_str = ""
    hours, remainder = divmod(seconds, 3600)
    if hours:
        time_str += f"{int(hours)}h "
    minutes, seconds = divmod(remainder, 60)
    if minutes or time_str:
        time_str += f"{int(minutes)}m "
    if not time_str:  # if time_str is empty, it means the duration is less than a minute
        time_str = f"{seconds:.2f}s"
    return time_str.strip()