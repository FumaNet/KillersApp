import random
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class Node:
  # nodes used by the Ring linked list, each pointing to the next and to the previous
  def __init__(self, name):
    self.next = None
    self.name = name
    self.previous = None

class Killers:
  # ring linked list
  def __init__(self, names):
    self.head = None
    names = list(set(names)) # make sure there are no duplicates
    random.shuffle(names) # randomly reshuffle the names from the list
    # print(names) # useful for debugging, prints them in the final order
    self.names = names
    for name in names:
      self.add_node(name)
  
  def add_node(self, name):
    # Adds a node at the end of the chain, before head
    newnode = Node(name)
    if self.head is None:
      self.head = newnode
      self.head.next = newnode
      self.head.previous = newnode
    else:
      self.head.previous.next = newnode
      newnode.next = self.head
      newnode.previous = self.head.previous
      self.head.previous = newnode

  def find_victim(self, assassin):
    # returns the node pointed at by the one with the assassin's name
    current_node = self.head
    for _ in self.names:
      if current_node.name == assassin:
        return current_node.next.name
      current_node = current_node.next
    return ("Name not found")


  def __repr__(self):
    current_node = self.head
    toPrint = ""
    for _ in self.names:
      toPrint += "Element: " + str(current_node.name) + "\n"
      current_node = current_node.next
    return toPrint



players = []

class KillersApp(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        self.window.add_widget(Image(source="victim.png"))

        self.greeting = Label(text = "Add Players to start!",
                              font_size = 18,
                              color = "#660000")
        
        self.window.add_widget(self.greeting)
        
        self.user = TextInput(
                    multiline=False,
                    padding_y = (20,20),
                    size_hint = (1, 0.5)
                    )
        self.window.add_widget(self.user)

        self.button = Button(
                      text = "ADD",
                      size_hint = (1, 0.5),
                      bold = True,
                      background_color = "#660000")
        self.button.bind(on_press = self.callback)
        self.window.add_widget(self.button)

        self.start_button = Button(
                      text = "START GAME",
                      size_hint = (1, 0.5),
                      bold = True,
                      background_color = "#000000")
        self.start_button.bind(on_press = self.start_game)
        self.window.add_widget(self.start_button)

        return self.window

    def callback(self, instance):
        players.append(self.user.text.strip())
        full_text = "Current Players:\n"
        for player in players:
          full_text += "- " + player + "\n"
        self.greeting.text = full_text
        self.user.text = ""


    def start_game(self, instance):
        self.killer_list = Killers(players)

        self.start_button.disabled = True
        self.button.disabled = True
        self.user.background_color = [0,0,0,0]

        
        self.greeting = Label(text = "Insert your name to see the designated victim",
                              font_size = 18,
                              color = "#660000")
        self.window.add_widget(self.greeting)
        

        self.user = TextInput(
                    multiline=False,
                    # padding_y = (20,20),
                    size_hint = (1, 0.5)
                    )
        self.window.add_widget(self.user)

        self.button = Button(
                      text = "FIND VICTIM",
                      size_hint = (1, 0.5),
                      bold = True,
                      background_color = "#660000")
        
        self.button.bind(on_press = self.show_victim)
        self.window.add_widget(self.button)

        self.hide_button = Button(
                      text = "HIDE VICTIM",
                      size_hint = (1, 0.5),
                      bold = True,
                      background_color = "#660000")
        
        self.hide_button.bind(on_press = self.hide_victim)
        self.window.add_widget(self.hide_button)

    def show_victim(self, instance):
        victim_text = "You victim is: " + self.killer_list.find_victim(self.user.text.strip())
        self.greeting.text = victim_text

    def hide_victim(self, instance):
        victim_text = "Insert your name to see the designated victim"
        self.greeting.text = victim_text
        self.user.text = ""
    

        



if __name__ == "__main__":
    KillersApp().run()


