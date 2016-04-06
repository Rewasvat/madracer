﻿#!/usr/bin/python
# -*- coding: utf-8 -*-

import sfml as sf
from scripts.game import Game

################################################################

def executeGame(fullscreen, cheatsEnabled, vsync):
    windowtitle = "Mad Racer"
    if fullscreen:
        windowsize, _ = sf.VideoMode.get_desktop_mode()
        window = sf.RenderWindow(sf.VideoMode(*windowsize), windowtitle, sf.Style.FULLSCREEN)
    else:
        windowsize = (1000, 700)
        window = sf.RenderWindow(sf.VideoMode(*windowsize), windowtitle)
    
    try:
        font = sf.Font.from_file("arial.ttf")
    except IOError: 
        print "error"
        exit(1)
    
    Game.initialize(window, font, cheatsEnabled)
    
    icon = Game.images.player.to_image()
    window.icon = icon.pixels
    window.vertical_synchronization = vsync
    window.mouse_cursor_visible = False
    
    tfps = sf.Text("-", font, character_size=25)
    tfps.color = sf.Color.RED
    tfps.position = (window.width-250, window.height-60)
    showFps = True
    
    clock = sf.Clock()
    clock.restart()
    time_to_update = 0.0
    # start the game loop
    while window.is_open:
        # process events
        for event in window.events:
            # close window: exit
            if type(event) is sf.CloseEvent:
                window.close()
            if type(event) is sf.ResizeEvent:
                #Game.updateGraphics()
                pass
            if type(event) is sf.FocusEvent:
                Game.paused = event.lost
            if type(event) is sf.KeyEvent:
                if (event.code == sf.Keyboard.Q and event.control) or event.code == sf.Keyboard.ESCAPE:
                    window.close();
                elif event.code == sf.Keyboard.RETURN and event.control and event.released:
                    fullscreen = not fullscreen
                    if fullscreen:
                        windowsize, _ = sf.VideoMode.get_desktop_mode()
                        window.recreate(sf.VideoMode(*windowsize), windowtitle, sf.Style.FULLSCREEN)
                    else:
                        windowsize = (1000, 700)
                        window.recreate(sf.VideoMode(*windowsize), windowtitle)
                    window.icon = icon.pixels
                    window.vertical_synchronization = vsync
                    window.mouse_cursor_visible = False
                    Game.updateGraphics()
                    tfps.position = (window.width-250, window.height-60)
                elif event.code == sf.Keyboard.F and event.control and event.released:
                    showFps = not showFps
                else:
                    Game.input(event)
                
        window.clear() # clear screen

        elapsed = clock.restart()
        time_to_update += elapsed.seconds
        if time_to_update > 1.0/Game.fps:
            Game.update()
            time_to_update = 0.0

        Game.draw()
        
        if showFps:
            tfps.string = "WindowFPS: %.2f\nUpdateFPS: %.2f" % (1.0/elapsed.seconds, Game.actual_fps)
            window.draw(tfps)

        window.display() # update the window
                        
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Python implementation of Mad Racer game.")
    parser.add_argument("--fullscreen", "-f", action="store_true", default=False, help="If the window should start fullscreen. self can be toggled during execution (default no)")
    parser.add_argument("--cheats", "-c", action="store_true", default=False, help="If cheats should be enabled.")
    parser.add_argument("--vsync", "-vs", action="store_true", default=False, help="If VSync should be enabled.")
    args = parser.parse_args()
    executeGame(args.fullscreen, args.cheats, args.vsync)