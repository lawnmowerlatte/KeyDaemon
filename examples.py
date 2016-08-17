from KeyDaemon import KeyDaemon

kd = KeyDaemon("10.0.11.230")

# Send text and immediately delete it
kd.subliminal("Wake up, Neo...")

# Send text and then scramble it
kd.send("Hello world")
kd.scramble(5)

# Type some words, select all and delete it
kd.send("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")
kd.select_all()
kd.special("DELETE")

# Hit Control-Alt-Delete
kd.ctrl_alt_del()

# Hit Alt-Tab
kd.alt_tab()
# Hit Alt-Tab 10 times
kd.alt_tab(10)

# Click the mouse
kd.mouse_click("left")
kd.mouse_click("right")

# Growing/shrinking circles
for i in range(2, 6):
    kd.tiny_circles(i*5)
for i in range(4, 1, -1):
    kd.tiny_circles(i*5)

# Interactive mode!
kd.interactive()
# /Send this text directly
# enter
# backspace
# press alt
# tab
# release alt
# mouse move 100 100 0
# mouse click left
# mouse press right
# .tiny_circles(10)
# .ctrl('x')
# .virtual_console(); .xwindows()
# eof