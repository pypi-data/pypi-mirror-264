import keyboard

def capslock_listener():
    capslock_pressed = False

    def on_key_event(event):
        nonlocal capslock_pressed
        if keyboard.is_pressed('capslock'):
            if event.event_type == keyboard.KEY_DOWN:
                capslock_pressed = True
            elif event.event_type == keyboard.KEY_UP:
                capslock_pressed = False
    
    keyboard.on_press(on_key_event)
    keyboard.wait('esc')
    
    return capslock_pressed

while True:
    print(capslock_listener())
    # if capslock_listener():
    #     print("Caps Lock pressed")