from a2_support import *



class Tile():
    """ abstract class for tiles
    """
    def __init__(self) -> None:
        """ attributes of Tile
        """
        pass

    def is_blocking(self) -> bool:
        """ a tile default to be NOT blocked

        Outputs:
            : the attribute of blocking moving instances (bool)
        """
        return False
    
    def get_type(self) -> str:
        """ get the type of a tile

        Outputs:
            : the type of a tile (str)
        """
        if type(self).__name__ == 'Tile':
            return 'Abstract Tile'
        else:
            return type(self).__name__[0]
    
    def __str__(self) -> str:
        """ same as get_type(self)
        """
        return self.get_type()
    
    def __repr__(self) -> str:
        """ same as get_type(self)
        """
        return self.get_type()
    


class Floor(Tile):
    """ tiles as empty spaces which do not block moving instances
    """
    def get_type(self) -> str:
        return ' '



class Wall(Tile):
    """ tiles as walls which block moving instances
    """
    def is_blocking(self) -> bool:
        """ a wall default to be blocking

        Outputs:
            : the attribute of blocking moving instances (bool)
        """
        return True
    


class Goal(Tile):
    """ tiles as a goal location for a crate
    """
    def __init__(self) -> None:
        """ attributes of Goal: _filled: whether a goal is filled
        """
        super().__init__()
        self._filled = False
    
    def fill(self) -> None:
        """ set a goal to be filled
        """
        self._filled = True
    
    def is_filled(self) -> bool:
        """ returns True when the goal is filled, else False

        Outputs:
            : the state of whether a goal is filled (bool)
        """
        if self._filled:
            return True
        else:
            return False

    def __str__(self) -> str:
        """ returns FILLED_GOAL if a goal tile is filled, otherwise GOAL

        Outputs:
            : string representation of a goal (str)
        """
        if self._filled:
            return FILLED_GOAL
        else:
            return GOAL
        
    def __repr__(self) -> str:
        """ same as __str__(self)
        """
        return str(self)
    
    def unfill(self) -> None:
        """ unfill a goal
        """ 
        self._filled = False



class Entity():
    """ abstract class for entities
    """
    def __init__(self) -> None:
        """ entities has no attributes beyond self
        """
        pass

    def get_type(self) -> str:
        """ get the type of an entity

        Outputs:
            : the type of an entity (str)
        """
        if type(self).__name__ == 'Entity':
            return 'Abstract Entity'
        else:
            return type(self).__name__[0]        

    def is_movable(self) -> bool:
        """ entities are not movable by default

        Outputs:
            : the movability of an entity (bool)
        """
        return False

    def __str__(self) -> str:
        """ same as get_type(self)
        """
        return self.get_type()

    def __repr__(self) -> str:
        """ same as get_type(self)
        """
        return self.get_type()



class Crate(Entity):
    """ entities as crates
    """
    def __init__(self, strength: int) -> None:
        """ attributes of crates

        Inputs:
            strength: the strength required to move a crate (int)
        """
        self._strength = strength
    
    def get_strength(self) -> int:
        """ get the strength required to move a crate

        Outputs:
            : the strength required to move a crate (int)
        """
        return self._strength
    
    def is_movable(self) -> bool:
        """ a crate is movable

        Outputs:
            : the movability of a crate (bool)
        """
        return True
    
    def __str__(self) -> str:
        """ the string representation of a crate

        Outputs:
            : the strength required to move a crate (str)
        """
        return str(self._strength)
            
    def __repr__(self) -> str:
        """ same as __str__(self)
        """
        return str(self)



class Potion(Entity):
    """ entities as potions
    """
    def __init__(self) -> None:
        """ potions has no attributes beyond self
        """
        pass

    def get_type(self) -> str:
        """ get the type of a potion

        Outputs:
            : the type of a potion (str)
        """
        if type(self).__name__ == 'Potion':
            return 'Potion'
        else:
            return type(self).__name__[0]

    def effect(self) -> dict[str, int]:
        """ set a holder for the effects of different potions

        Outputs:
            : an empty holder for the effects (dict[str, int]) 
        """
        return dict()



class StrengthPotion(Potion):
    """ entities as potions of type StrengthPotion
    """
    def effect(self) -> dict[str, int]:
        """ a strength potion adds 2 'strength's

        Output:
            : the effect of a strength potion (dict[str, int])
        """
        return {'strength': 2}



class MovePotion(Potion):
    """ entities as potions of type MovePotion
    """
    def effect(self) -> dict[str, int]:
        """ a move potion adds 5 'move's

        Outputs:
            : the effect of a move potion (dict[str, int])
        """
        return {'moves': 5}



class FancyPotion(Potion):
    """ entities as potions of type FancyPotion
    """
    def effect(self) -> dict[str, int]:
        """ a fancy potion adds 2 'strength's and 2 'move's

        Outputs:
            : the effect of a fancy potion (dict[str, int])
        """
        return {'strength': 2, 'moves': 2}



class Player(Entity):
    """ entities as players
    """
    def __init__(self, start_strength: int, moves_remaining: int) -> None:
        """ attributes of a player

        Inputs: 
            start_strength: the initial strength of a player (int)
            moves_remaining: the remaining moves of a player (int)
        """
        self._strength = start_strength
        self._moves_remaining = moves_remaining

    def is_movable(self) -> bool:
        """ a player is movable when his/her has moves available

        Outputs:
            : the movability of a player (bool)
        """
        return self._moves_remaining > 0

    def get_strength(self) -> int:
        """ get the strength of a player

        Outputs:
            : the strength of a player (int)
        """
        return self._strength
    
    def add_strength(self, amount: int) -> None:
        """ add the given strength to a player

        Inputs:
            amount: the amount of strength to be added (int)
        """
        self._strength += amount

    def get_moves_remaining(self) -> int:
        """ get the remaining moves of a player

        Outputs:
            : the remaining moves of a player (int)
        """
        return self._moves_remaining
    
    def add_moves_remaining(self, amount: int) -> None:
        """ add the given moves to a player

        Inputs: 
            amount: the number of moves to be added (int)
        """
        self._moves_remaining += amount

    def apply_effect(self, potion_effect: dict[str, int]) -> None:
        """ add available effects, namely moves and strength, to a player,
            given specific potions

        Inputs:
            potion_effect: available effects with amounts (dict[str, int])
        """
        effects = list(potion_effect.keys())
        
        if 'moves' in effects:
            self.add_moves_remaining(potion_effect['moves'])
        if 'strength' in effects:
            self.add_strength(potion_effect['strength'])



def convert_maze(game: list[list[str]]) -> tuple[Grid, Entities, Position]:
    """ convert string representation of a maze to be an object-oriented one,
        and re-locate entities and player position information from the maze

    Inputs:
        game: the raw maze (list[list[str]])
    
    Outputs:
        : the formatted maze, the entities, and the player's position
        (tuple[Grid, Entities, Position])
    """
    # default settings
    player_row, player_col = -1, -1
    entities = dict()
    
    def make_floor(i: int, j: int) -> None:
        """ helper function to make entity/tile on position (i, j) on the maze
            to be Floor()

        Inputs:
            i: row of the position (int)
            j: col of the position (int)
        """
        game[i][j] = Floor()
        return 

    # handle the raw maze cell by cell
    for i in range(len(game)):
        for j in range(len(game[i])):
            
            # handle the player
            if game[i][j] == 'P':
                player_row, player_col = i, j
                make_floor(i, j)
            
            # handle any crates
            elif not game[i][j] in [WALL, GOAL, FLOOR, STRENGTH_POTION, 
                                    MOVE_POTION, FANCY_POTION]:
                strength = int(game[i][j])
                entities[(i,j)] = Crate(strength)
                make_floor(i, j)
            
            # handle any potions
            elif game[i][j] == STRENGTH_POTION:
                entities[(i,j)] = StrengthPotion()
                make_floor(i, j)
            elif game[i][j] == MOVE_POTION:
                entities[(i,j)] = MovePotion()
                make_floor(i, j)
            elif game[i][j] == FANCY_POTION:
                entities[(i,j)] = FancyPotion()
                make_floor(i, j)
            
            # handle any tiles
            elif game[i][j] == WALL:
                game[i][j] = Wall()
            elif game[i][j] == GOAL:
                game[i][j] = Goal()
            elif game[i][j] == FLOOR:
                make_floor(i, j)
            
    return (game, entities, (player_row, player_col))



class SokobanModel():
    """ the model for the game
    """
    def __init__(self, maze_file: str) -> None:
        """ the attributes of the model
            player_last_met can be CRATE or 'CRATE then GOAL' or 'Potion' or -1
        
        Inputs:
            maze_file: the directory of a raw maze
        """
        raw_maze, player_stats = read_file(maze_file)
        strength, moves = player_stats[0], player_stats[1]
        
        # attributes for normal gameplay
        self._maze, self._entities, self._player_position = \
            convert_maze(raw_maze)
        self._player = Player(strength, moves)
        
        # attributes for undo
        self._player_position_history = [self._player_position]
        self._gone_crate_history, self._gone_potion_history = dict(), []
        self._player_last_hit = -1

    def get_maze(self) -> Grid:
        """ get a formatted maze

        Outputs:
            : the formatted maze (Grid)
        """
        return self._maze
    
    def get_entities(self) -> Entities:
        """ get the entities of the model

        Outputs: 
            : the entities of the model (Entities)
        """
        return self._entities

    def get_player_position(self) -> tuple[int, int]:
        """ get the position of the player

        Outputs:
            : the position of the player (tuple[int, int])
        """
        return self._player_position
    
    def get_player_moves_remaining(self) -> int:
        """ get the remaining moves of the player

        Outputs: the remaining moves of the player (int)
        """
        return self._player.get_moves_remaining()
    
    def get_player_strength(self) -> int:
        """ get the strength of the player

        Outputs: the strength of the player (int)
        """
        return self._player.get_strength() 

    def attempt_move(self, direction: str) -> bool:
        """ move the player in case of crates (incl. ones next to goals),
            potions, and tiles, given user's prompt. Invalid moves cannot 
            move the player. Undo of the last valid move is accessible

        Inputs: 
            direction: the direction to move the player (str)
        
        Outputs:
            : the validity of the move (bool)
        """
        
        def get_next_position(current_position: tuple) -> tuple[int, int]:
            """ helper function to get next position of player, given direction
                Warning
                 get_next_position(), next(), and next_tile() are nested within
                 attempt_move(direction), since they are dependent on direction

            Inputs:
                current_position: the current position of the player (tuple)
            
            Outputs:
                : his/her next position (tuple[int, int])
            """
            row, col = current_position
            
            # branching by direction
            if direction == UP:
                return (row-1, col)
            elif direction == DOWN:
                return (row+1, col)
            elif direction == LEFT:
                return (row, col-1)
            elif direction == RIGHT:
                return (row, col+1)

        def next(row_or_col: str) -> int:
            """ helper function to get the row or column of the next position
                of the player

            Inputs: 
                row_or_col: 'row' or 'col' (str)

            Outputs:
                row|col: the row or the column (int)
            """
            row, col = get_next_position(self._player_position)
            if row_or_col == 'row':
                return row
            elif row_or_col == 'col':
                return col

        def next_tile():
            """ helper function to get the tile that the player will meet in the
                next step

            Outputs:
                : the tile (Wall|Floor|Goal)
            """
            row, col = get_next_position(self._player_position)
            return self.get_maze()[row][col]
        
        # method variable that simplifies many codes
        next_position = get_next_position(self._player_position)

        # if the move is invalid
        if direction not in [UP, DOWN, LEFT, RIGHT]:
            return False
        elif isinstance(next_tile(), Wall):
            return False

        # if next position of player is an entity
        elif next_position in self._entities.keys():
        
            # if next position of player stands a crate 
            if type(self._entities[next_position]) == Crate:
                
                # if the crate cannot be moved
                if self.get_player_strength() < self._entities[next_position]\
                    .get_strength()\
                    or next('row') not in range(len(self._maze)) \
                    or next('col') not in range(len(self._maze[0])):
                    return False
                
                else:
                    # move the crate
                    self._player_last_hit = CRATE
                    row_2, col_2 = get_next_position(next_position)
                    self._entities[(row_2, col_2)] = \
                        self._entities[next_position]
                    del self._entities[next_position]
                    
                    # if next position of a crate stands an unfilled goal
                    if type(self._maze[row_2][col_2]) == Goal and \
                        not self._maze[row_2][col_2].is_filled():
                        self._player_last_hit = 'CRATE then GOAL'
                        self._gone_crate_history[(row_2, col_2)] = \
                            self._entities[(row_2, col_2)]
                        del self._entities[(row_2, col_2)]
                        self._maze[row_2][col_2].fill()

            # if next position of player stands a potion
            elif type(self._entities[next_position]) in \
                [StrengthPotion, MovePotion, FancyPotion]:
                # apply the potion to the player and remove it from entities
                self._player_last_hit = 'Potion'
                self._gone_potion_history += [self._entities[next_position]]
                potion = self._entities[next_position]
                self._player.apply_effect(potion.effect())
                del self._entities[next_position]

        # if next position of player stands anything unrelated to undo
        else:
            self._player_last_hit = -1
        
        # update player information about moves
        self._player._moves_remaining -= 1
        self._player_position = next_position
        self._player_position_history += [self._player_position]
        return True

    def has_won(self) -> bool:
        """ judge if the game has been won given the current maze. A game has
            been won if having all goals be filled

        Outputs:
            : if the game has been won (bool)
        """
        return not any(isinstance(tile, Goal) and not tile.is_filled()
                       for row in self._maze for tile in row)
    
    def undo(self) -> None:
        """ undo all the effects by the last valid move, w.r.t. crates, goals,
            potions, and the player
        """        
        # reverse player information about moves
        self._player._moves_remaining += 1
        self._player_position = self._player_position_history[-2]
        row_move, col_move = [self._player_position_history[-1][i] - 
                              self._player_position_history[-2][i] 
                              for i in range(2)]
        
        # if a crate was moved to a goal, recover both
        if self._player_last_hit == 'CRATE then GOAL':
            position_crate, crate = list(self._gone_crate_history.items())[-1]
            row, col = position_crate
            self._entities[(row-row_move, col-col_move)] = crate
            self._maze[row][col].unfill()

        # if next position of player stood a crate 
        elif self._player_last_hit == CRATE:
            row, col = self._player_position_history[-1]
            self._entities[(row, col)] = \
                self._entities[(row+row_move, col+col_move)]
            del self._entities[(row+row_move, col+col_move)]
        
        # if next position of player stood a potion
        elif self._player_last_hit == 'Potion':
            last_potion = self._gone_potion_history[-1]
            self._entities[self._player_position_history[-1]] = last_potion
            if type(last_potion) == StrengthPotion:
                self._player._strength -= 2
            elif type(last_potion) == MovePotion:
                self._player._strength -= 5
            elif type(last_potion) == FancyPotion:
                self._player._strength -= 2
                self._player._moves_remaining -= 2



class Sokoban():
    """ the controller of the game
    """
    def __init__(self, maze_file: str) -> None:
        """ attributes of Sokoban

        Inputs:
            maze_file: the directory of a maze file (str)
        """
        self._model = SokobanModel(maze_file)
        self._view = SokobanView()

    def display(self) -> None:
        """ display the game and the statistics of the player
        """
        self._view.display_game(self._model._maze, self._model._entities, 
                                self._model._player_position)
        self._view.display_stats(self._model.get_player_moves_remaining(),
                                 self._model.get_player_strength())
        
    def play_game(self) -> None:
        """ the whole process of the game
        """
        while self._model.has_won() == False:
            
            # if the game has been lost
            if self._model.has_won() == False and \
                self._model.get_player_moves_remaining() <= 0:
                print('You lost!')
                return 
            
            # display the game state
            self._view.display_game(self._model._maze, self._model._entities, 
                                    self._model._player_position)
            self._view.display_stats(self._model.get_player_moves_remaining(),
                                     self._model.get_player_strength())
            
            # prompt a user for a move
            move = input('Enter move: ')
            if move == 'u':
                self._model.undo()
            elif move == 'q':
                return 
            elif self._model.attempt_move(move):
                pass
            else:
                print('Invalid move\n')
            
            # if the game has been won
            if self._model.has_won() == True:
                self._view.display_game(self._model._maze,
                                        self._model._entities,
                                        self._model._player_position)
                self._view.display_stats(self._model.get_player_moves_remaining\
                                         (), self._model.get_player_strength())
                print('You won!')
                return



def main():
    """ run the maze file and the game
    """
    game = Sokoban('maze_files/maze1.txt')
    game.play_game()
    pass

if __name__ == '__main__':
    main()