

def lerp(start, end, multiplier):
    return start + (end - start) * multiplier

def lerp_color(start, target, amount):
    if len(start) != len(target):
        raise ValueError("Colors must have the same number of channels")

    return tuple(round(lerp(start_channel, target_channel, amount)) for start_channel, target_channel in zip(start, target))