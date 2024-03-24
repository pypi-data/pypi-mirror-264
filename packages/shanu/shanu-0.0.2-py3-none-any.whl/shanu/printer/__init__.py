from rangeen import (
    info as _blue,
    warning as _yellow,
    danger as _red,
    colorify,
    colors,
)


def _green(text):
    return colorify(text, fg=colors.GREEN)


def blue(*args, **kwargs):
    return print(*[_blue(arg) for arg in args], **kwargs)


def yellow(*args, **kwargs):
    return print(*[_yellow(arg) for arg in args], **kwargs)


def red(*args, **kwargs):
    return print(*[_red(arg) for arg in args], **kwargs)


def green(*args, **kwargs):
    return print(*[_green(arg) for arg in args], **kwargs)
