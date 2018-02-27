#!/usr/bin/env python3
'''
@author  Michele Tomaiuolo - http://www.ce.unipr.it/people/tomamic
@license This software is free - http://www.gnu.org/licenses/gpl.html
'''

from sys import argv

from kivy.app import runTouchApp, stopTouchApp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.properties import ListProperty
 
from x7_fifteen import Fifteen, Game


class GridButton(Button):
    grid_pos = ListProperty((0, 0))


class GameGui(GridLayout):
    def __init__(self, game):
        self.__game = game
        self.__cols, self.__rows = game.size()
        GridLayout.__init__(self, cols=self.__cols)
        
        for y in xrange(0, self.__rows):
            for x in xrange(0, self.__cols):
                btn = GridButton(grid_pos=(x, y))
                btn.bind(on_release=self.handle_click)
                self.add_widget(btn)
        self.update_all_buttons()

    def update_button(self, x, y):
        val = self.__game.get_val(x, y)
        b = self.children[-1 - y * self.__cols - x]
        b.text = val  # children are reversed, in Kivy

    def update_all_buttons(self):
        for y in range(self.__rows):
            for x in range(self.__cols):
                self.update_button(x, y)
                
    def handle_click(self, btn):
        self.__game.play_at(*btn.grid_pos)  # args unpacking
        self.update_all_buttons()

        if self.__game.finished():
            popup = Popup(title='Game finished',
                          content=Button(text=self.__game.message()))
            popup.content.bind(on_release=popup.dismiss)
            popup.open()
            stopTouchApp()

            
if __name__ == '__main__':
    game = Fifteen(4, 4)
    runTouchApp(GameGui(game))
