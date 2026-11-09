#!/usr/bin/env python3
"""Envía WM_DELETE_WINDOW sólo a ventanas del PID pedido en el display privado."""
import ctypes as c
import re
import subprocess
import sys


class ClientMessage(c.Structure):
    # XClientMessageEvent en la ABI de libX11.
    _fields_ = [('type', c.c_int), ('serial', c.c_ulong), ('send_event', c.c_int),
                ('display', c.c_void_p), ('window', c.c_ulong), ('message_type', c.c_ulong),
                ('format', c.c_int), ('data', c.c_long * 5)]


class XEvent(c.Union):
    _fields_ = [('client', ClientMessage), ('padding', c.c_long * 24)]


def close_windows(pid):
    x11 = c.CDLL('libX11.so.6')
    window = c.c_ulong
    display_ptr = c.c_void_p
    window_list = c.POINTER(window)
    x11.XOpenDisplay.argtypes = [c.c_char_p]
    x11.XOpenDisplay.restype = display_ptr
    x11.XDefaultRootWindow.argtypes = [display_ptr]
    x11.XDefaultRootWindow.restype = window
    x11.XQueryTree.argtypes = [display_ptr, window, c.POINTER(window), c.POINTER(window),
                              c.POINTER(window_list), c.POINTER(c.c_uint)]
    x11.XInternAtom.argtypes = [display_ptr, c.c_char_p, c.c_int]
    x11.XInternAtom.restype = c.c_ulong
    x11.XSendEvent.argtypes = [display_ptr, window, c.c_int, c.c_long, c.POINTER(XEvent)]
    x11.XFree.argtypes = [c.c_void_p]
    x11.XCloseDisplay.argtypes = [display_ptr]
    display = x11.XOpenDisplay(None)
    if not display:
        return False
    children = window_list()
    try:
        root, parent, size = window(), window(), c.c_uint()
        if not x11.XQueryTree(display, x11.XDefaultRootWindow(display), c.byref(root),
                              c.byref(parent), c.byref(children), c.byref(size)):
            return False
        protocols = x11.XInternAtom(display, b'WM_PROTOCOLS', 0)
        delete_window = x11.XInternAtom(display, b'WM_DELETE_WINDOW', 0)
        sent = False
        # El Xvfb del visor no tiene un gestor de ventanas que las reparentalice.
        for window_id in children[:size.value] if children else ():
            properties = subprocess.run(['/usr/bin/xprop', '-id', hex(window_id),
                                         '_NET_WM_PID', 'WM_PROTOCOLS'],
                                        capture_output=True, text=True, timeout=3)
            if properties.returncode or not re.search(rf'^_NET_WM_PID\(CARDINAL\) = {pid}$',
                                                       properties.stdout, re.MULTILINE):
                continue
            if not re.search(r'^WM_PROTOCOLS\(ATOM\):.*\bWM_DELETE_WINDOW\b',
                             properties.stdout, re.MULTILINE):
                continue
            event = XEvent()
            event.client = ClientMessage(33, 0, 1, display, window_id, protocols, 32,
                                         (c.c_long * 5)(delete_window))
            sent = bool(x11.XSendEvent(display, window_id, 0, 0, c.byref(event))) or sent
        return sent
    finally:
        if children:
            x11.XFree(children)
        x11.XCloseDisplay(display)


if __name__ == '__main__':
    sys.exit(0 if close_windows(int(sys.argv[1])) else 1)
