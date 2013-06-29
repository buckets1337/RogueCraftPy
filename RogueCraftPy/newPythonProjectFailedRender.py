"""my initial idea for this project is to create a turn-based, roguelike-style game that focuses less on combat, and more on crafting and construction.
This is going to be a bit harder for me to implement than the roguelike, but I'm going to try and build this using TDD methods and borrowing code from
the roguelike I just "finished".  I'll add more to this comment section later as new ideas and stuff occur to me."""


import libtcodpy as libtcod
import config_newPythonProject as config
import math
import textwrap
import random




class Rect:     #a rectangle on the map.  used to characterize a room.
    def __init__(self,x,y,w,h, is_rectangle=True):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
        
    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return (center_x, center_y)
        
    def intersect(self, other):
        #returns true if this rectangle intersects with another rectangle
        return(self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1)

class Tile:     #a tile of the map and it's properties

    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked
        self.explored = False
        
        #by default, if a tile is blocked, it also blocks los
        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight
        
class Map:      #a map object.  Represents the level map, must call new_map after initialization

    def __init__(self, x, y, name, blocked):
        global map_list, current_map_name
        self.x = x
        self.y = y
        self.blocked = blocked
        self.name = name
        
        current_map_name = name    #will eventually be removed with multi levels
        
        map_list.append(self)
        
    def indoors_map(self, x, y, blocked, no_of_rooms, no_of_intersects, room_min_size, room_max_size):
        global current_map, current_map_name, current_rooms
        self.x = x
        self.y = y
        self.blocked = blocked
        self.no_of_rooms = no_of_rooms
        self.room_min_size = room_min_size
        self.room_max_size = room_max_size
        
        #fill the map with blocked tiles
        map = [[Tile(self.blocked)
            for y in range(self.y) ]
                for x in range(self.x) ]
        current_map = map

        #carves the rooms
        num_rooms = 0
        room_intersects = 0
        for map in map_list:
            if map.name == current_map_name:
                this_map = map

        for r in range(no_of_rooms):
            room = self.generate_room(x, y, no_of_intersects, room_min_size, room_max_size)
            num_rooms += 1
            if num_rooms > 1:
                old_room = current_rooms[num_rooms - 2]
                new_room = current_rooms[num_rooms - 1]
                self.connect_with_tunnels(old_room, new_room)
            elif num_rooms == 1:
                (new_x, new_y) = room.center()
                player.x = new_x
                player.y = new_y
        
    def generate_room(self, map_x_length, map_y_length, no_of_intersects, room_min_size, room_max_size):  #chooses random coords for the room and defines the shape of the room
        global current_rooms
        #random width and height
        w = libtcod.random_get_int(0,room_min_size, room_max_size)
        h = libtcod.random_get_int(0,room_min_size, room_max_size)
        #random position in bounds on the map
        x = libtcod.random_get_int(0,0,map_x_length - w - 1)
        y = libtcod.random_get_int(0,0,map_y_length - h - 1)
        #makes the room
        new_room = Rect(x,y,w,h)
        #check other rooms for an intersection
        failed = False
        
        
        room_intersects = 0
        for other_room in current_rooms:
            if new_room.intersect(other_room):
                room_intersects +=1
                if room_intersects >= no_of_intersects:
                    failed = True
                    break
                break
        if not failed:  #not over max number of intersections, so clear to build
            self.create_room(new_room)
            return new_room
        
    def create_room(self, room):  #creates rooms on the map
        global current_map, current_rooms
        #go through the tiles in the rectangle and make them passable
        for x in range(room.x1+1, room.x2):
            for y in range(room.y1+1, room.y2):
                current_map[x][y].blocked = False
                current_map[x][y].block_sight = False
        current_rooms.append(room)
                
    def connect_with_tunnels(self, old_room, new_room):   #connects an old room to a new room with a tunnel through their center points

            if libtcod.random_get_int(0,0,1) == 1:
                self.create_h_tunnel(old_room.x1, new_room.x1, old_room.y1)
                self.create_v_tunnel(old_room.y1, new_room.y1, new_room.x1)
            else:
                self.create_v_tunnel(old_room.y1, new_room.y1, new_room.x1)
                self.create_h_tunnel(old_room.x1, new_room.x1, new_room.y1)
                
    def create_h_tunnel(self, x1, x2, y):     #creates a horizontal segment of hallway
        global current_map
        for x in range(min(x1, x2), max(x1, x2) + 1):
            current_map[x][y].blocked = False
            current_map[x][y].block_sight = False
            
    def create_v_tunnel(self, y1, y2, x):     #creates a vertical segment of hallway
        global current_map
        for y in range(min(y1, y2), max(y1, y2) + 1):
            current_map[x][y].blocked = False
            current_map[x][y].block_sight = False
            
    def list_tile(self, x, y):    #returns a tile on the map
        global current_map
        return current_map[x][y]
        
    def is_blocked(x,y):    #checks if a tile is blocked by something
        #first test the map tile
        if current_map[x][y].blocked:
            return True
            
        #now check for blocking objects
        # for object in objects:
            # if object.blocks and object.x == x and object.y == y:
                # return True
                
        return False
    
class Object:       #this is a generic object (item, monster, etc) that is always drawn to screen
    def __init__(self, x, y, char, name, color, dungeon_level=0, status='', blocks=False, always_visible=False, alert=None, fighter=None, ai=None, item=None, equipment=None):
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.color = color
        self.blocks = blocks        #blocks movement
        self.fighter = fighter      #fighter component, adds ability to attack and take damage
        self.always_visible = always_visible
        self.alert = alert      #alert is a set of coordinates indicating last known place of player, or None indicating no state of alert
        self.dungeon_level = dungeon_level      #dungeon level item was created on
        
        
        if self.fighter:    #let the fighter component know who owns it
            self.fighter.owner = self
            
        self.ai = ai
        if self.ai: #let the AI component know who owns it
            self.ai.owner = self
            
        self.item = item
        if self.item:   #let the item component know who owns it
            self.item.owner = self
            
        self.equipment = equipment
        if self.equipment:  #let equipment component know who owns it
            self.equipment.owner = self
            #Equipment is an item
            self.item = Item()
            self.item.owner = self
        
    def move (self, dx, dy):
        #check for blocked
        if not is_blocked(self.x + dx, self.y + dy):
            #move by the given amount
            self.x += dx
            self.y += dy
            
    def moveai (self):
        #behavior for monster movement when a direct line to the player is not available
        not_moved = True
        while not_moved:
            direction = libtcod.random_get_int(0,1,5)   #pick a random direction
            if direction == 1:  #north
                if not is_blocked(self.x, self.y - 1) and (player.distance(self.x, self.y - 1) <= self.distance_to(player)):
                    self.y -= 1
                    not_moved = False
            elif direction == 2:    #east
                if not is_blocked(self.x + 1, self.y) and (player.distance(self.x + 1, self.y) <= self.distance_to(player)):
                    self.x += 1
                    not_moved = False
            elif direction == 3:    #south
                if not is_blocked(self.x, self.y + 1) and (player.distance(self.x, self.y + 1) <= self.distance_to(player)):
                    self.y += 1
                    not_moved = False
            elif direction == 4:    #west
                if not is_blocked(self.x - 1, self.y) and (player.distance(self.x - 1, self.y) <= self.distance_to(player)):
                    self.x -= 1
                    not_moved = False
            else:   #randomly move in some direction if the space is clear, or else wait a turn if it is not.
                dx = libtcod.random_get_int(0, -1, 1)
                dy = libtcod.random_get_int(0, -1, 1)
                if not is_blocked(self.x + dx, self.y):
                    self.x = self.x + dx
                if not is_blocked(self.x, self.y + dy):
                    self.y = self.y + dy
                not_moved = False

        
    def draw(self):
        #only show if it's visible to the player
        if libtcod.map_is_in_fov(fov_map, self.x, self.y):
            (x, y) = to_camera_coordinates(self.x, self.y)
            
            if x is not None:
                #sets the color and then draws the character
                libtcod.console_set_default_foreground(con,self.color)
                libtcod.console_put_char(con,x,y,self.char,libtcod.BKGND_NONE)
    
    def clear(self):
        #erase the character that represents the object
        (x, y) = to_camera_coordinates(self.x, self.y)
        if x is not None:
            libtcod.console_put_char(con, x, y, ' ', libtcod.BKGND_NONE)
            
    def move_towards(self, target_x, target_y):
        #vector from this object to the target, and distance
        dx = target_x - self.x
        dy = target_y - self.y
        
        #below is old move_towards code (hangs on walls)
            #distance = math.sqrt(dx**2 + dy**2)
            ##normalize vector to length 1, keeping direction, then round
            ##and convert to integer so movement is restricted to the map
            #dx = int(round(dx/distance))
            #dy = int(round(dy/distance))
            
        if dx>0:
            dx = 1
        if dx<0:
            dx = -1
        if dy>0:
            dy = 1
        if dy<0:
            dy = -1
            
        if is_blocked(self.x + dx, self.y + dy):
            self.moveai()
        self.move(dx, dy)

        
    def distance_to(self, other):
        #return the distance to another object
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx**2 + dy**2)
        
    def send_to_back(self):
        #make this object drawn first, so everything else appears above it
        global objects
        objects.remove(self)
        objects.insert(0, self)
        
    def distance(self, x, y):
    #return the distance to some coords
        return math.sqrt((x-self.x)**2 + (y-self.y)**2)
        
        
def handle_keys():      #handles keyboard input
    global fov_recompute
    global keys
    
    if key.vk == libtcod.KEY_ESCAPE:
        return 'exit'   #executes 'exit' in main loop
#rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
#       Rendering-Related Functions
#rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
        
def render_all():    #renders the screen
    global color_dark_wall, color_light_wall, color_dark_ground, color_light_ground
    global fov_recompute, fov_map
    global game_state, map_list, current_map, current_map_name
    
    move_camera(player.x, player.y)
    
    if fov_recompute:       #recomputes FOV if needed (player move, etc)
        fov_recompute = False
        libtcod.map_compute_fov(fov_map, player.x, player.y, config.TORCH_RADIUS, config.FOV_LIGHT_WALLS, config.FOV_ALGO)
        # for object in objects:
            # if libtcod.map_is_in_fov(fov_map, object.x, object.y):
                # if object.item:
                    # object.always_visible = True
                # if object.name == 'stairs':
                    # object.always_visible = True
        libtcod.console_clear(con)
        
    #draw the map
    for y in range(config.CAMERA_HEIGHT):
        for x in range(config.CAMERA_WIDTH):
            (map_x, map_y) = (camera_x + x, camera_y + y)
            visible = libtcod.map_is_in_fov(fov_map, map_x, map_y)
            wall = current_map[map_x][map_y].block_sight
            if game_state == 'dead':    #reveals the map when player dies
                if wall:
                    libtcod.console_set_char_background(con,x,y,color_nolight_wall,libtcod.BKGND_SET)
                else:
                    libtcod.console_set_char_background(con, x, y, color_nolight_ground, libtcod.BKGND_SET)
                    
            if not visible:
                if current_map[map_x][map_y].explored:
                    if wall:
                        libtcod.console_set_char_background(con,x,y,color_not_in_view_wall,libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, color_not_in_view_ground, libtcod.BKGND_SET)
            elif game_state == 'dead':      #turns off the lights if the player is dead
                if wall:
                    libtcod.console_set_char_background(con,x,y,color_not_in_view_wall,libtcod.BKGND_SET)
                else:
                    libtcod.console_set_char_background(con, x, y, color_not_in_view_ground, libtcod.BKGND_SET)
                    
            else:
                if wall:    #sets wall color and renders them
                    indx = [0, config.TORCH_RADIUS - 4, config.TORCH_RADIUS - 2, config.TORCH_RADIUS]
                    key = [config.color_light_wall, config.color_dark_wall, config.color_nolight_wall, config.color_nolight_wall]
                    light_map =  libtcod.color_gen_map(key, indx)
                    distance_from_light = abs(int(player.distance(camera_x +x, camera_y + y)))
                    if distance_from_light != 0:
                        wallcolor =  light_map[distance_from_light-1]
                    else:
                        wallcolor = config.color_dark_wall
                    libtcod.console_set_char_background(con, x, y, wallcolor, libtcod.BKGND_SET)
                else:       #sets tile color and renders them
                    indx = [0, config.TORCH_RADIUS - 4, config.TORCH_RADIUS - 2, config.TORCH_RADIUS]
                    key = [config.color_light_ground, config.color_dark_ground, config.color_nolight_ground, config.color_nolight_ground]
                    light_map =  libtcod.color_gen_map(key, indx)
                    distance_from_light = abs(int(player.distance(camera_x +x, camera_y + y)))
                    if distance_from_light != 0:
                        groundcolor =  light_map[distance_from_light-1]
                    else:
                        groundcolor = config.color_dark_ground
                    libtcod.console_set_char_background(con,x,y,groundcolor,libtcod.BKGND_SET)
                #since visible, explores tile
                current_map[map_x][map_y].explored = True
                
    player.draw()
        
    #writes "con" console to the root console
    map_width = get_map_dimensions(current_map_name)[0]
    map_height = get_map_dimensions(current_map_name)[1]
    libtcod.console_blit(con,0,0,map_width,map_height,0,0,0)
    
    #prepare to render the GUI panel
    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)
    
    #print the game messages, one line at a time
    y = 1
    for (line, color) in game_msgs:
        libtcod.console_set_default_foreground(panel, color)
        libtcod.console_print_ex(panel, config.MSG_X, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
        y += 1
    
    #show dungeon level 
    libtcod.console_print_ex(panel, 1, 5, libtcod.BKGND_NONE, libtcod.LEFT, 'Dungeon level ' + str(dungeon_level))
    
    #blit the contents of "panel" to root console
    libtcod.console_blit(panel, 0, 0, config.SCREEN_WIDTH, config.PANEL_HEIGHT, 0, 0, config.PANEL_Y)
    
def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color): #render a bar (HP, EXP, ETC) 
    #first calculate the width of the bar
    bar_width = int(float(value) / maximum *total_width)
    
    #render the background first
    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)
    
    #now render the bar on top
    libtcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)
        
    #centered text with values on bar
    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, x + total_width / 2, y, libtcod.BKGND_NONE, libtcod.CENTER,
        name + ': ' + str(value) + '/' + str(maximum))
        
def get_map_dimensions(map_name):       #get dimensions of a map
    global map_list, current_map, current_map_name
    
    #get height and width of map
    for map in map_list:
        if map.name == current_map_name:
            map_width = map.x
            map_height = map.y
            return (map_width, map_height)
    
def message(new_msg, color = libtcod.white):    #console message
    global game_msgs
    
    #split the message if necessary, among multiple lines
    new_msg_lines = textwrap.wrap(new_msg, config.MSG_WIDTH)
    
    for line in new_msg_lines:
        #if the buffer is full, remove the first line to make room 
        #for the new line
        if len(game_msgs) == config.MSG_HEIGHT:
            del game_msgs[0]
            
        #add the new line as a tuple, with the text and the color
        game_msgs.append( (line,color) )
        
def move_camera(target_x, target_y):    #moves the camera
    global camera_x, camera_y, fov_recompute, map_list, current_map
    #new camera coords(from top left relative to map)
    x = target_x - config.CAMERA_WIDTH / 2 #coordinates so that target is at center of screen
    y = target_y - config.CAMERA_HEIGHT / 2
    map_dimensions = get_map_dimensions(current_map_name)
    map_width = map_dimensions[0]
    map_height = map_dimensions[1]
            
    
    #make sure camera doesn't see outside the map
    if x < 0: x = 0
    if y < 0: y = 0
    if x > map_width - config.CAMERA_WIDTH : x = map_width - config.CAMERA_WIDTH 
    if y > map_height - config.CAMERA_HEIGHT : y= map_height - config.CAMERA_HEIGHT 
    
    if x != camera_x or y != camera_y: fov_recompute = True
    
    (camera_x, camera_y) = (x, y)
        
def to_camera_coordinates(x, y):        #convert coordinates on the map to coordinates on the screen
    (x, y) = (x - camera_x, y - camera_y)
    
    if (x < 0 or y < 0 or x >= config.CAMERA_WIDTH or y>= config.CAMERA_HEIGHT):
        return (None, None) #if it's outside the view
    return (x, y)
    
"""''''''''''''''''''''''''''''''''''''
    Game Initialization Functions
''''''''''''''''''''''''''''''''''''"""
    
def initialize_fov():   #initialize the FOV
        global fov_recompute, fov_map, current_map, current_map_name
        fov_recompute = True
        map_dimensions = get_map_dimensions(current_map_name)
        map_width = map_dimensions[0]
        map_height = map_dimensions[1]
    
        ######## FOV
        fov_map = libtcod.map_new(map_width, map_height)
        for y in range(map_height):
            for x in range(map_width):
                libtcod.map_set_properties(fov_map, x, y, not current_map[x][y].block_sight, not current_map[x][y].blocked)
        
        libtcod.console_clear(con)  #unexplored areas start black

def play_game():    #play the game!
    global camera_x, camera_y, key, mouse
            
    player_action = None
            
    #intializes controls
    mouse = libtcod.Mouse()
    key = libtcod.Key()
    
    (camera_x, camera_y) = (0,0)
    
    while not libtcod.console_is_window_closed():
    
        #checks for mouse or keypress events
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE,key,mouse)
    
        #renders the console
        render_all()
    
        #update the console
        libtcod.console_flush()
        
        # check for a level up for player
        # check_level_up()
    
        #clears old position
        # for object in objects:
            # object.clear()
    
        #handle keys and exit game if needed
        player_action = handle_keys()
        if player_action == 'exit':
            #save_game()
            break

        #let monsters take their turn
        # if game_state == 'playing' and player_action != 'didnt-take-turn':
            # for object in master_monsters:
                # if object.ai:
                    # object.ai.take_turn()
            # turn_passed()
    
#------------------------------------------------------------------------
#   Global Variables
#------------------------------------------------------------------------
def new_game():
    global current_map, current_rooms, map_list, starting_map, dungeon_level
    global game_msgs, game_state, mouse, key, player
    current_map = []
    current_map_name = ''
    current_rooms = []
    map_list = []

    player = Object(0,0,'@', 'player', libtcod.white, blocks=True)
    
    starting_map = Map(100,100,"starting map", True)
    starting_map.indoors_map(starting_map.x, starting_map.y, starting_map.blocked, 10, 4, 5, 20)
    dungeon_level = 1
    
    game_msgs =[]



    

    game_state = 'playing'



#XXXXXXXXXXXXXXXXXXXXXXXX
#       Initialization
#XXXXXXXXXXXXXXXXXXXXXXXX

#gets game font
libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

new_game()

#initializes the console
map_dimensions = get_map_dimensions(current_map_name)
map_width = map_dimensions[0]
map_height = map_dimensions[1]

libtcod.console_init_root (config.SCREEN_WIDTH, config.SCREEN_HEIGHT, config.PROJECT_NAME, False)
con = libtcod.console_new(map_width, map_height)    #canvas, draws to console
panel = libtcod.console_new(config.SCREEN_WIDTH, config.PANEL_HEIGHT) #GUI panel

initialize_fov()
#sets framerate
libtcod.sys_set_fps(config.LIMIT_FPS)

play_game()



