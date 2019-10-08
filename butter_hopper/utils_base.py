from .headers import BASE_PATHS


def extract_distros(u):
    return {
        k: v
        for (k, v) in u.items()
        if not k.startswith('new') and not k.startswith('rescue')
    }
