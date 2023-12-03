import tkinter as tk
from tkinter import messagebox, filedialog
from typing import Callable, Union
from model import *
from a2_support import *
from a3_support import *



class FancyGameView(AbstractGrid):
    """ A grid displaying the game map, incl. all tiles, entities and player.
        Inherits from AbstractGrid
    """
    IMAGES = {
        WALL: 'images/W.png',
        FLOOR: 'images/Floor.png',
        GOAL: 'images/G.png',
        CRATE: 'images/C.png',
        PLAYER: 'images/P.png',
        STRENGTH_POTION: 'images/S.png',
        MOVE_POTION: 'images/M.png',
        FANCY_POTION: 'images/F.png',
        COIN: 'images/$.png'}
    
    def __init__(self, master: tk.Frame | tk.Tk, dimensions: tuple[int, int],
                size: tuple[int, int], **kwargs) -> None:
        """ Initialize FancyGameView. Set up appropriate dimensions, size, and
            an empty dict as the image cache

        Inputs:
            master: The master frame of the game, tk.Frame | tk.Tk
            dimensions: Dim of the game grid as # rows and # columns, 
                tuple[int, int]
            size: width and height in pixels for the game grid, tuple[int, int]
        """
        super().__init__(master, dimensions, size=(MAZE_SIZE, MAZE_SIZE), 
            **kwargs)
        self._cache = dict()

    def display(self, maze: Grid, entities: Entities, player_position: 
                Position) -> None:
        """ Display the grid of the game map

        Inputs:
            maze: A grid with only tiles on it, Grid
            entities: Entities to be placed on the grid, Entities
            player_position: Position of the player, Position
        """
        self.clear()
        cell_size = self.get_cell_size()
        
        # Tiles
        for row in range(self._dimensions[0]):
            for col in range(self._dimensions[1]):
                image = get_image(self.IMAGES[maze[row][col].get_type()], 
                    cell_size, self._cache)
                self.create_image(self.get_midpoint((row, col)), image=image)
        
        # Entities
        for key in entities.keys():
            image = get_image(self.IMAGES[entities[key].get_type()], cell_size,
                self._cache)
            self.create_image(self.get_midpoint(key), image=image)
        
        # Player
        image = get_image(self.IMAGES[PLAYER], cell_size, self._cache)
        self.create_image(self.get_midpoint(player_position), image=image)

    def reset_cache(self) -> None:
        """ Reset the cache for FancyGameView
        """
        self._cache = dict()



class FancyStatsView(AbstractGrid):
    """ A grid displaying the stats of the player, incl. moves remaining,
        strength, and money. Inherits from AbstractGrid
    """
    def __init__(self, master: tk.Tk | tk.Frame) -> None:
        """ Initialize FancyStatsView. Set up appropriate dimensions and size

        Inputs:
            master: The master frame of the game, tk.Frame | tk.Tk
        """
        super().__init__(
            master, 
            dimensions=(3, 3), 
            size=(MAZE_SIZE + SHOP_WIDTH, STATS_HEIGHT))

    def draw_stats(self, moves_remaining: int, strength: int, money: int) \
        -> None:
        """ Display the grid of the player's stats

        Inputs:
            moves_remaining: # moves remains for player, int
            strength: # units of strength remains for player, int
            money: # units of money remains for player, int
        """
        self.clear()

        # Annotate cells
        self.annotate_position((0, 1), 'Player Stats', 
            font=('Arial', 18, 'bold'))
        self.annotate_position((1, 0), 'Moves remaining:', font='TkDefaultFont')
        self.annotate_position((1, 1), 'Strength:', font='TkDefaultFont')
        self.annotate_position((1, 2), 'Money:', font='TkDefaultFont')
        self.annotate_position((2, 0), f"{moves_remaining}", 
            font='TkDefaultFont')
        self.annotate_position((2, 1), f"{strength}", font='TkDefaultFont')
        self.annotate_position((2, 2), f"${money}", font='TkDefaultFont')
        


class Shop(tk.Frame):
    """ A frame displaying a shop where player can buy potions, incl. strength 
        potion, move potion, and fancy potion. Inherits from tk.Frame
    """
    def __init__(self, master: tk.Frame) -> None:
        """ Initialize Shop. Set up the shop to act as tk.Frame and to have a
            title label

        Inputs:
            master: The parent class for the shop frame, tk.Frame
        """
        super().__init__(master)
        label = tk.Label(self, text="Shop", font=('Arial', 18, 'bold'))
        label.pack(side=tk.TOP)

    def create_buyable_item(self, item: str, amount: int, callback: 
                            Callable[[], None]) -> None:
        """ List a buyable item in the frame of shop, incl. a label and a button

        Inputs:
            item: a global constant for the string repr of a potion, str
            amount: the amount of money required to buy that potion, int
            callback: a function-like callable where its arguments can be told
                somewhere else
        """
        # One frame for one specific potion
        item_frame = tk.Frame(self)
        item_frame.pack(side=tk.TOP, fill=tk.X)
        
        item_names = {
            STRENGTH_POTION: "Strength Potion",
            MOVE_POTION: "Move Potion", 
            FANCY_POTION: "Fancy Potion"}
        name = item_names.get(item, "")
        
        tk.Label(item_frame, text=f"{name}: ${amount}", font='TkDefaultFont')\
            .pack(side=tk.LEFT)
        tk.Button(item_frame, text="Buy", command=callback).pack(side=tk.RIGHT)



class FancySokobanView:
    """ View of the game, wrapping the smaller GUI widgets incl. 
        FancyGameView, FancyStatsView, and Shop
    """
    def __init__(self, master: tk.Tk, dimensions: tuple[int, int], 
                 size: tuple[int, int]) -> None:
        """ Initialize FancySokobanView. Create a title banner, set the title on
            the window, and instantiate and pack the three widgets

        Inputs:
            master: The master frame of the game, tk.Frame | tk.Tk
            dimensions: Dim of the game grid as # rows and # columns, 
                tuple[int, int]
            size: width and height in pixels for the game grid, tuple[int, int]
        """
        # Instantiate the three widgets
        self._fancy_game_view = FancyGameView(master, dimensions, size)
        self._fancy_stats_view = FancyStatsView(master)
        self._shop = Shop(master)
        self._cache = dict()
        
        # Create and pack the title banner
        banner_width = MAZE_SIZE + SHOP_WIDTH
        banner = get_image(
            'images/banner.png', (banner_width, BANNER_HEIGHT), self._cache)
        banner_label = tk.Label(master, image=banner)
        banner_label.pack(side=tk.TOP)
        
        # Pack the three widgets
        self._fancy_stats_view.pack(side=tk.BOTTOM)
        self._fancy_game_view.pack(side=tk.LEFT)
        self._shop.pack(side=tk.TOP)
        
        master.title("Extra Fancy Sokoban")
        
    def display_game(self, maze: Grid, entities: Entities, 
                     player_position: Position) -> None:
        """ Display the game grid

        Inputs:
            maze: A grid with only tiles on it, Grid
            entities: Entities to be placed on the grid, Entities
            player_position: Position of the player, Position
        """
        self._fancy_game_view.display(maze, entities, player_position)

    def display_stats(self, moves: int, strength: int, money: int) -> None:
        """ Display the stats grid

        Inputs:
            moves: # moves remains for player, int
            strength: # units of strength remains for player, int
            money: # units of money remains for player, int            
        """
        self._fancy_stats_view.draw_stats(moves, strength, money)

    def create_shop_items(self, shop_items: dict[str, int], button_callback: 
                          Callable[[str], None] | None = None) -> None:
        """ Create all the buyable items in the shop, where a lambda function
            callback, which calls button_callback, is given to 
            create_buyable_item in Shop

        Inputs:
            shop_items: Maps item's string repr to price, dict[str, int]
            button_callback: A callable on an item (key) in shop_items, 
                Callable[[str], None] | None = None
        """
        for item, amount in shop_items.items():
            # A lambda function calling button_callback on item
            if button_callback:
                callback = lambda item=item: button_callback(item)
                self._shop.create_buyable_item(item, amount, callback)
            
            else:
                self._shop.create_buyable_item(item, amount, None)
    
    def reset_view(self, new_dims: tuple[int, int]) -> None:
        """ Reset the cache and the dimensions of FancyGameView

        Inputs:
            new_dims: the updated dimensions of FancyGameView, tuple[int, int]
        """
        self._fancy_game_view.reset_cache()
        self._fancy_game_view.set_dimensions(new_dims)

    

class ExtraFancySokoban:
    """ Controller of the game, which creates, maintains and communicates the 
        instances of the model and the view classes
    """    
    def __init__(self, root: tk.Tk, maze_file: str) -> None:
        """ Initialize ExtraFancySokoban. Create instances of SokobanModel and 
            FancySokobanView. Create shop items. Bind keypress events to the 
            relevant handler. Redraw the display

        Inputs:
            root: The master frame of the game, tk.Tk
            maze_file: The directory of a raw maze txt file, str
        """
        # Model of the game
        self._sokoban_model = SokobanModel(maze_file)
        
        # View of the game
        self._root = root
        dimensions = self._sokoban_model.get_dimensions()
        size = (MAZE_SIZE+SHOP_WIDTH, BANNER_HEIGHT+MAZE_SIZE+STATS_HEIGHT)
        self._sokoban_view = FancySokobanView(self._root, dimensions, size)
        
        shop_items = self._sokoban_model.get_shop_items()
        self._sokoban_view.create_shop_items(shop_items, self.buy_effect)

        self._root.bind("<KeyPress>", self.handle_keypress)

        self.redraw()

    def buy_effect(self, item: str) -> None:
        """ Helper function to be passed to create_shop_item when creating shop
            items in __init__
        """
        self._sokoban_model.attempt_purchase(item)
        self.redraw()

    def redraw(self) -> None:
        """ Redraw the game view and stats view based on the current model state
        """
        self._sokoban_view.display_game(
            self._sokoban_model.get_maze(),
            self._sokoban_model.get_entities(),
            self._sokoban_model.get_player_position()
        )
        self._sokoban_view.display_stats(
            self._sokoban_model.get_player_moves_remaining(),
            self._sokoban_model.get_player_strength(),
            self._sokoban_model.get_player_money()
        )

    def handle_msgbox(self, msg: str) -> None:
        """ Handle the game replay behavior by a messagebox when a win or a lost
            is in place. If True, the game will be reset; if False, the program
            will terminate

        Inputs:
            msg: The binary message indicating win or loss of the game, str
        """
        msg_box = messagebox.askyesno(title=None, message=msg)
        
        if msg_box == True:
            self._sokoban_model.reset()
            self.redraw()
        else:
            self._root.destroy()

    def handle_keypress(self, event: tk.Event) -> None:
        """ A keypress event handler. When a keypress event occurs, the model 
            attempts move as per the event, and the view is redrawn. If a game
            is won or lost, ask player if he/she will replay it

        Inputs:
            event: A keypress event, tk.Event
        """
        self._sokoban_model.attempt_move(event.char)
        self.redraw()

        # Message box after win or lost
        if self._sokoban_model.has_won() == True:
            self.handle_msgbox("You won! Play again?")
        elif self._sokoban_model.has_won() == False \
            and self._sokoban_model.get_player_moves_remaining() <= 0:
            self.handle_msgbox("You lost! Play again?")

    def save_file(self) -> None:
        """ Save the current game state incl. tiles and entities on maze, and
            player's strength and moves remaining, to a txt file
        """
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt", 
            filetypes=[("Text files", "*.txt")])
        
        # If a filename is provided
        if filepath:
            with open(filepath, 'w') as file:

                # Write player stats to txt
                file.write(
                    f"{self._sokoban_model.get_player_strength()}" + " " +
                    f"{self._sokoban_model.get_player_moves_remaining()}\n")
                
                # Write entities, player, tiles to txt
                maze = self._sokoban_model.get_maze()
                maze_rows, maze_cols = self._sokoban_model.get_dimensions()
                entities = self._sokoban_model.get_entities()
                for i in range(maze_rows):
                    for j in range(maze_cols):
                        if (i,j) in entities.keys():
                            file.write(str(entities[(i,j)]))
                        elif (i,j) == self._sokoban_model.get_player_position():
                            file.write(PLAYER)
                        else:
                            file.write(str(maze[i][j]))
                    file.write("\n")
                    
    def read_file(self) -> None:
        """ Read and restore a saved game state from a txt file, formatted as
            the line 0 of two integers (strength, moves remaining), and a
            maze from line 1 (tiles, entities, player position)
        """
        filename = filedialog.askopenfilename(
                title="Select file",
                filetypes=[("Text files", "*.txt")],
                defaultextension=".txt")
        
        # All info from txt file are handled by SokobanModel
        self._sokoban_model = SokobanModel(filename)

        dimensions = self._sokoban_model.get_dimensions()
        self._sokoban_view.reset_view(dimensions)

        self.redraw()



def play_game(root: tk.Tk, maze_file: str) -> None:
    """ Construct the controller instance, set up the file menu for saving and
        reading current game state, and ensure the root window stays listening
        for events
    
    Inputs:
        root: The master frame of the game, tk.Tk
        maze_file: The directory of a raw maze txt file, str
    """
    controller = ExtraFancySokoban(root, maze_file)

    # File menu
    menu = tk.Menu(root)
    root.config(menu=menu)
    file_menu = tk.Menu(menu)
    menu.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Save", command=controller.save_file)    
    file_menu.add_command(label="Load", command=controller.read_file)

    controller._root.mainloop()



def main() -> None:
    """ Set up the root of the game and play the game
    """
    root = tk.Tk()
    play_game(root, 'maze_files/coin_maze.txt')



if __name__ == "__main__":
    main()