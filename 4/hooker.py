import pythoncom, pyHook

def OnKeyboardEvent(event):
    print('MessageName:' + event.MessageName)
    print('Message:' + str(event.Message))
    print('Time:' + str(event.Time))
    print('Window:' + str(event.Window))
    print('WindowName:' + str(event.WindowName))
    print('Ascii:' + str(event.Ascii) + ' ' + str(chr(event.Ascii)))
    print('Key:' + str(event.Key))
    print('KeyID:' + str(event.KeyID))
    print('ScanCode:' + str(event.ScanCode))
    print('Extended:' + str(event.Extended))
    print('Injected:' + str(event.Injected))
    print('Alt' + str(event.Alt))
    print('Transition' + str(event.Transition))
    print('---')

# return True to pass the event to other handlers
    return True

# create a hook manager
hm = pyHook.HookManager()
# watch for all mouse events
hm.KeyDown = OnKeyboardEvent
# set the hook
hm.HookKeyboard()
# wait forever
pythoncom.PumpMessages()
