from os import system
import util


class BattleGround:
    class MineNode:

        def __init__(self):
            self.value = 0
            self.facade = "*"
            self.x = 0
            self.y = 0

        def create_node(self, x, y, value=0):
            self.x = x
            self.y = y
            self.value = value

        def __repr__(self):
            return "{}".format(self.facade)

    def __init__(self, n=8):
        self.grid = list()
        self.side = n
        self.moves = list()
        self.status = "hot"

    def initialize_grid(self):
        for i in range(self.side):
            row = list()
            for j in range(self.side):
                # print("\ni={}\tj={}".format(i, j))
                new_node = self.MineNode()
                new_node.create_node(i, j)
                row.append(new_node)
            self.grid.append(row)

    def deploy_mines(self):
        mines = util.define_mines(self.side)
        neighbors = list()
        for mine in mines:
            x, y = mine
            self.grid[x][y].value = "m"
            neighbors.extend(util.get_neighbours(mine, self.side))
        for node in neighbors:
            r, c = node
            node_value = self.grid[r][c].value
            if isinstance(node_value, int):
                self.grid[r][c].value += 1

    def display(self):
        output = util.print_grid_skeleton(self)
        print(output)


if __name__ == "__main__":
    while True:
        try:
            system(util.clear_console())
            ground_size = input("\nEnter the size of the field (a whole number"
                                " greater than 4 but not more than 10)?: ")
            if ground_size.isnumeric():
                ground_size = int(ground_size.strip())
                if ground_size not in range(4, 11):
                    print("\nField size either too small or too large! "
                          "Please try again.\n")
            else:
                print("\nInvalid input - defaulting to a field size of 8")
                ground_size = 8
            new_ground = BattleGround(ground_size)
            new_ground.initialize_grid()
            new_ground.deploy_mines()
            win_count = ground_size * (ground_size - 1)
            print("\nThe mines are deployed in the field! "
                  "Proceed with caution!\n")
            new_ground.display()
            while new_ground.status == "hot":
                if len(new_ground.moves) == win_count:
                    new_ground.status = "cold"
                    break
                user_selection = input("Type in the cell you want to reveal \n("
                                       "example - A8 will reveal the first cell"
                                       " in the 8th row): ")
                user_selection = user_selection.strip()
                if user_selection:
                    if user_selection in new_ground.moves:
                        print("\nThis cell was already played. "
                              "Please try again!\n")
                        continue
                    selection_valid = util.validate_user_selection(
                        user_selection, ground_size)
                    if selection_valid:
                        new_ground.moves.append(user_selection)
                        new_ground.display()
                    else:
                        print("Invalid selection! Try again.\n")
                        new_ground.display()
                        continue
                else:
                    print("\nSorry, no input received! Give it another go.\n")
                    new_ground.display()
                    continue
            if new_ground.status == "detonated":
                banner = "#" * 50
                if util.re_prompt(preface=banner):
                    break
            if new_ground.status == "cold":
                banner = "*" * 50
                print("{}\nYou won!\n{}".format(banner, banner))
                if util.re_prompt():
                    break
        except Exception as e:
            if util.re_prompt(preface="Oops! An exception occurred: {}".format(e)):
                break
