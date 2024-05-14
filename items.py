import random

from variables import UniversalVariables
BLOCK_SIZE = UniversalVariables.block_size

class Item:
    def __init__(self, name: str, id: int, **kwargs):
        self.name = name
        self.id = id
        for key, value in kwargs.items():
            setattr(self, key, value)




class ObjectItem(Item):
    """ World items, not pickable, breakable. """
    instances = []

    def __init__(self, name: str, id: int, collision_box: list, width: int, height: int, render_when: None, **kwargs):  # hp: int
        super().__init__(name, id, **kwargs)
        self.image = f"Images/Items/Object_Item/{name}.png"
        self.type = "Object"
        self.collision_box = collision_box 
        self.width = width
        self.height = height
        self.render_when = render_when
        ObjectItem.instances.append(self)


class MineralItem(Item):
    """ Objects that are breakable, pickable. """
    instances = []

    def __init__(self, name: str, id: int, width: int, height: int, render_when: None, **kwargs):    # recipes: list[dict[str, dict[str, int], dict[str, int]]]
        super().__init__(name, id, **kwargs)
        self.image = f"Images/Items/Mineral_Item/{name}.png"                                              # self.recipes = recipes
        self.type = "Mineral"
        self.width = width
        self.height = height
        self.render_when = render_when
        MineralItem.instances.append(self)


class ToolItem(Item):
    instances = []

    def __init__(self, name: str, id: int, **kwargs):  # recipes: list[dict[str, dict[str, int], dict[str, int]]], **kwargs):
        super().__init__(name, id, **kwargs)           
        self.image = f"Images/Items/Tool_Item/{name}.png"   # self.recipes = recipes
        self.type = "Tool"
        ToolItem.instances.append(self)

###################################################### WORLD OBJECTS ######################################################

water = ObjectItem(
    name="Water_0",
    id=0,
    collision_box=[0, 0, 1, 1],
    width=int(BLOCK_SIZE * 1),
    height=int(BLOCK_SIZE * 1),
    render_when=None,  
)
grass = ObjectItem(
    name="Ground",
    id=1,
    collision_box=[0, 0, 1, 1],
    width=int(BLOCK_SIZE * 1),
    height=int(BLOCK_SIZE * 1),
    render_when=None,  
)


# oak_planks = ObjectItem(
#     name="Oak_Planks",
#     id=3,
#     width=int(BLOCK_SIZE * 1),
#     height=int(BLOCK_SIZE * 1),
#     render_when=None,  
# )

farmland = ObjectItem(
    name="Farmland",
    id=6,
    collision_box=[0, 0, 1, 1],
    width=int(BLOCK_SIZE * 1),
    height=int(BLOCK_SIZE * 1),
    render_when=None,  
)

wall_background = ObjectItem(
    name="Maze_Ground",
    id=98,
    collision_box=[0, 0, 1, 1],
    width=int(BLOCK_SIZE * 1),
    height=int(BLOCK_SIZE * 1),
    render_when=None,  
)

wall = ObjectItem(
    name="Maze_Wall",
    id=99,
    collision_box=[0, 0, 1, 1],
    width=int(BLOCK_SIZE * 1),
    height=int(BLOCK_SIZE * 1),
    render_when=None,  
)

Maze_Start_Top = ObjectItem(
    name="Maze_Start_Top",
    id=91,
    collision_box=[0, 0, 1, 1],
    width=int(BLOCK_SIZE * 1),
    height=int(BLOCK_SIZE * 1),
    render_when=0,
)

Maze_Start_Right = ObjectItem(
    name="Maze_Start_Right",
    id=92,
    collision_box=[0, 0, 1, 1],
    width=int(BLOCK_SIZE * 1),
    height=int(BLOCK_SIZE * 1),
    render_when=0,
)

Maze_Start_Bottom = ObjectItem(
    name="Maze_Start_Bottom",
    id=93,
    collision_box=[0, 0, 1, 1],
    width=int(BLOCK_SIZE * 1),
    height=int(BLOCK_SIZE * 1),
    render_when=0,
)

Maze_Start_Bottom_Glade = ObjectItem(
    name="Maze_Start_Bottom",
    id=933,
    collision_box=[0, 0, 1, 1],
    width=int(BLOCK_SIZE * 1),
    height=int(BLOCK_SIZE * 1),
    render_when=0,
)

Maze_End_Left = ObjectItem(
    name="Maze_End_Left",
    id=94,
    collision_box=[0, 0, 1, 1],
    width=int(BLOCK_SIZE * 1),
    height=int(BLOCK_SIZE * 1),
    render_when=0,
)

Maze_End_Top = ObjectItem(
    name="Maze_End_Top",
    id=95,
    collision_box=[0, 0, 1, 1],
    width=int(BLOCK_SIZE * 1),
    height=int(BLOCK_SIZE * 1),
    render_when=0,
)

Maze_End_Right = ObjectItem(
    name="Maze_End_Right",
    id=96,
    collision_box=[0, 0, 1, 1],
    width=int(BLOCK_SIZE * 1),
    height=int(BLOCK_SIZE * 1),
    render_when=0,
)

Maze_End_Bottom = ObjectItem(
    name="Maze_End_Bottom",
    id=97,
    collision_box=[0, 0, 1, 1],
    width=int(BLOCK_SIZE * 1),
    height=int(BLOCK_SIZE * 1),
    render_when=0,
)

Maze_End_Bottom_Glade = ObjectItem(
    name="Maze_End_Bottom",
    id=977,
    collision_box=[0, 0, 1, 1],
    width=int(BLOCK_SIZE * 1),
    height=int(BLOCK_SIZE * 1),
    render_when=0,
)

###################################################### MINERALS ###################################################

oak_tree = MineralItem(
    name="Oak_Tree",
    id=4,
    width=int(BLOCK_SIZE * 2),
    height=int(BLOCK_SIZE * 2),
    render_when=None,  
)

rock = MineralItem(
    name="Rock",
    id=2,
    width=int(BLOCK_SIZE * 1),
    height=int(BLOCK_SIZE * 1),
    render_when=None,  
)

# Mineral Items
wheat = MineralItem(
    name="Wheat",
    id=7,
    width=int(BLOCK_SIZE * 1),
    height=int(BLOCK_SIZE * 1),
    render_when=None,  
)

Maze_Key = MineralItem(
    name="Maze_Key",
    id=10,
    width=int(BLOCK_SIZE * 1),
    height=int(BLOCK_SIZE * 1),
    render_when=None,  
)

# stone = MineralItem(
#     name="Stone",
#     id=100,
#     # recipes=[{"Recipe": {"Rock": 1}, "Amount": 2}],
# )

# stone_shard = MineralItem(
#     name="Stone_Shard",
#     id=102,
#     # recipes=[{"Recipe": {"Stone": 4}, "Amount": 1}],
# )
# 
# stick = MineralItem(
#     name="Stick",
#     id=103,
#     # recipes=[{"Recipe": {"Oak_Planks": 1}, "Amount": 2}],
# )

###################################################### TOOLS ######################################################

wooden_pickaxe = ToolItem(
    name="Wooden_Pickaxe",
    id=201,
    # recipes=[{"Recipe": {"Stick": 2, "Oak_Planks": 4}, "Amount": 1}],
    durability=None,  
)

wooden_axe = ToolItem(
    name="Wooden_Axe",
    id=202,
    # recipes=[{"Recipe": {"Stick": 2, "Oak_Planks": 3}, "Amount": 1}],
    durability=None,  
)

wooden_shovel = ToolItem(
    name="Wooden_Shovel",
    id=203,
    # recipes=[{"Recipe": {"Stick": 1, "Oak_Planks": 2}, "Amount": 1}],
    durability=None,  
)

wooden_sword = ToolItem(
    name="Wooden_Sword",
    id=204,
    # recipes=[{"Recipe": {"Stick": 1, "Oak_Planks": 3}, "Amount": 1}],
    durability=None,  
)

stone_pickaxe = ToolItem(
    name="Stone_Pickaxe",
    id=205,
    # recipes=[{"Recipe": {"Stick": 2, "Stone": 4}, "Amount": 1}],
    durability=None,  
)

stone_axe = ToolItem(
    name="Stone_Axe",
    id=206,
    # recipes=[{"Recipe": {"Stick": 2, "Stone": 3}, "Amount": 1}],
    durability=None,  
)

stone_shovel = ToolItem(
    name="Stone_Shovel",
    id=207,
    # recipes=[{"Recipe": {"Stick": 1, "Stone": 2}, "Amount": 1}],
    durability=None,  
)

stone_sword = ToolItem(
    name="Stone_Sword",
    id=208,
    # recipes=[{"Recipe": {"Stick": 1, "Stone": 3}, "Amount": 1}],
    durability=None,  
)

# Testida asju mis on seotud ainult item.py'ga
if __name__ == "__main__":
    
    pass







#################################################################





# items_list = [
#     {
#         "Type": "Object",
#         "Name": "Rock",
#         "ID": 2,
#         "HP": 5,
#         "Breakable": True,
#         # "Breakable": [
#         #     {"hardness": "Wood"},
#         #     {"amount": ("Stone", random.randint(1, 5))},
#         # ],
#         "Object_width": int(block_size * 1),
#         "Object_height": int(block_size * 0.8),
#         "Render_when": -(block_size * 0.1)
#         },
#     {
#         "Type": "Object",
#         "Name": "Farmland",
#         "ID": 3,
#         "Object_width": int(block_size * 0.5),
#         "Object_height": int(block_size * 0.5),
#         },
#     {
#         "Type": "Object",
#         "Name": "Oak_Tree",
#         "ID": 4,
#         "HP": 5,
#         "Breakable": True,

#         "Object_width": int(block_size * 2),
#         "Object_height": int(block_size * 2),
#         "Render_when": block_size * 0.8
#         },
#     {
#         "Type": "Object",
#         "Name": "Flower",
#         "ID": 6,
#         "Breakable": True,
#         "Placeable": True,
#         "Object_width": int(block_size * 0.5),
#         "Object_height": int(block_size * 0.5),
#         "Render_when": -(block_size * 0.23)
#         },
#     {
#         "Type": "Object",
#         "Name": "Mushroom",
#         "ID": 8,
#         "Breakable": True,
#         "Placeable": True,
#         "Object_width": int(block_size * 0.3),
#         "Object_height": int(block_size * 0.3),
#         "Render_when": -(block_size * 0.45)
#         },
#     {
#         "Type": "Object",
#         "Name": "Wheat",
#         "ID": 7,
#         "Breakable": True,
#         "Object_width": int(block_size * 1),
#         "Object_height": int(block_size * 1),
#         "Render_when": (block_size * .2)
#         },

#     {
#         "Type": "Object",
#         "Name": "Big_Bush",
#         "ID": 9,
#         "Breakable": True,
#         "Object_width": int(block_size * .7),
#         "Object_height": int(block_size * .7),
#         "Render_when": (block_size * .2)
#         },
#     {
#         "Type": "Object",
#         "Name": "Maze_Key",
#         "ID": 10,
#         "Breakable": True,
#         "Object_width": int(block_size * 1),
#         "Object_height": int(block_size * 1),
#         "Render_when": (block_size * -1)
#         },

#     # Items

#     {
#         "Type": "Mineral",
#         "Name": "Oak_Wood",
#         "Recipes": [
#             {"Recipe": {"Oak_Tree": 1}, "Amount": 2},
#         ],
#         "Amount": 4,
#         "ID": 20,
#         # "Placeable": True,
#         # "Breakable": True,
#     },
#     {
#         "Type": "Mineral",
#         "Name": "Oak_Planks",
#         "ID": 21,
#         "Recipes": [
#             {"Recipe": {"Oak_Wood": 1}, "Amount": 2}
#         ],
#         },
#     {
#         "Type": "Mineral",
#         "Name": "Stick",
#         "ID": 22,
#         "Recipes": [
#             {"Recipe": {"Oak_Planks": 1}, "Amount": 2},
#         ],
#         },
#     {
#         "Type": "Mineral",
#         "Name": "Stone",
#         "ID": 23,
#     },

#     # TOOLS

#     {
#         "Type": "Tool",
#         "Name": "Wood_Pickaxe",
#         "ID": 24,
#         "Recipes": [
#             {"Recipe": {"Stick": 2, "Oak_Planks": 3}, "Amount": 1},
#         ],
#         "Durability": 128,
#         },
#     {
#         "Type": "Tool",
#         "Name": "Wood_Axe",
#         "ID": 25,
#         "Recipes": [
#             {"Recipe": {"Stick": 2, "Oak_Planks": 3}, "Amount": 1},
#         ],
#         "Durability": 128,
#         },
#     {
#         "Type": "Tool",
#         "Name": "Wood_Shovel",
#         "ID": 26,
#         "Recipes": [
#             {"Recipe": {"Stick": 2, "Oak_Planks": 2}, "Amount": 1,},
#         ],
#         "Durability": 128,
#         },
#     {
#         "Type": "Tool",
#         "Name": "Stone_Shard",
#         "ID": 27,
#         "Recipes": [
#             {"Recipe": {"Rock": 2}, "Amount": 1,},  # Tuleb Stone'iks ära muuta
#         ],
#         "Durability": 128,
#         },
#     {
#         "Type": "Tool",
#         "Name": "Small_Rock_Sword",
#         "ID": 28,
#         "Recipes": [
#             {"Recipe": {"Stick": 2, "Stone_Shard": 1}, "Amount": 1},
#         ],
#         "Durability": 256,
#         },
#     {
#         "Type": "Mineral",
#         "Name": "Coal",
#         "ID": 29,
#         },
#     {
#         "Type": "Tool",
#         "Name": "Torch",
#         "ID": 30,
#         "Recipes": [
#             {"Recipe": {"Stick": 2, "Coal": 1}, "Amount": 4},
#         ],
#         "Durability": 256,
#     },

#     # Unbreakable Blocks - Items

# ### TODO: Blocke lõhkudes peab määrama palju ja mida ta saab näiteks "Oak_Tree"d
# ### TODO: lõhkudes ei ta lic puukest invi, selle asemel saab ta 2 "Oak_Plank"u

# {
#         "Type": "Object",
#         "Name": "Farmland",
#         "ID": 107,
#         "Breakable": False,
#         "Block_vision": False,
#         "Object_width": int(block_size * 1),
#         "Object_height": int(block_size * 1),
#         "Render_when": -block_size
#         },
    
# {
#         "Type": "Object",
#         "Name": "Maze_Ground",
#         "ID": 98,
#         "Breakable": False,
#         "Block_vision": False,
#         "Object_width": int(block_size * 1),
#         "Object_height": int(block_size * 1),
#         "Render_when": -block_size
#         },
#     {
#         "Type": "Object",
#         "Name": "Maze_Wall",
#         "ID": 99,
#         "Breakable": False,
#         "Block_vision": True,
#         "Collision_box": [0, 0, 1, 1],
#         "Object_width": int(block_size * 1),
#         "Object_height": int(block_size * 1),
#         "Render_when": -block_size
#         },
#     {
#         "Type": "Object",
#         "Name": "Maze_Blade",
#         "ID": 9099,
#         "Breakable": False,
#         "Block_vision": True,
#         "Collision_box": [0.5, 0.5, 0.75, 0.75],
#         "Object_width": int(block_size * 0.25),
#         "Object_height": int(block_size * 0.25),
#         "Render_when": -block_size
#         },
#     {
#         "Type": "Object",
#         "Name": "Maze_Blade_Changer_On",
#         "ID": 989,
#         "Breakable": False,
#         "Block_vision": True,
#         "Collision_box": [0, 0, 1, 1],
#         "Object_width": int(block_size * 1),
#         "Object_height": int(block_size * 1),
#         "Render_when": -block_size
#         },
#     {
#         "Type": "Object",
#         "Name": "Maze_Blade_Changer_Off",
#         "ID": 989,
#         "Breakable": False,
#         "Block_vision": True,
#         "Collision_box": [0, 0, 1, 1],
#         "Object_width": int(block_size * 1),
#         "Object_height": int(block_size * 1),
#         "Render_when": -block_size
#         },
#     {
#         "Type": "Object",
#         "Name": "Maze_Blade_Stationary",
#         "ID": 900,
#         "Breakable": False,
#         "Block_vision": True,
#         "Collision_box": [0, 0, 1, 1],
#         "Object_width": int(block_size * 1),
#         "Object_height": int(block_size * 1),
#         "Render_when": -block_size
#         },
#     {
#         "Type": "Object",
#         "Name": "Maze_Start_Left",
#         "ID": 90,
#         "Breakable": False,
#         "Block_vision": True,
#         "Object_width": int(block_size * 1),
#         "Object_height": int(block_size * 1),
#         "Render_when": 0
#         },
#     {
#         "Type": "Object",
#         "Name": "Maze_Start_Top",
#         "ID": 91,
#         "Breakable": False,
#         "Block_vision": True,
#         "Object_width": int(block_size * 1),
#         "Object_height": int(block_size * 1),
#         "Render_when": 0
#         },
#     {
#         "Type": "Object",
#         "Name": "Maze_Start_Right",
#         "ID": 92,
#         "Breakable": False,
#         "Block_vision": True,
#         "Object_width": int(block_size * 1),
#         "Object_height": int(block_size * 1),
#         "Render_when": 0
#         },
#     {
#         "Type": "Object",
#         "Name": "Maze_Start_Bottom",
#         "ID": 93,
#         "Breakable": False,
#         "Block_vision": True,
#         "Object_width": int(block_size * 1),
#         "Object_height": int(block_size * 1),
#         "Render_when": 0
#         },
#     {
#         "Type": "Object",
#         "Name": "Maze_Start_Bottom",
#         "ID": 933,
#         "Breakable": False,
#         "Block_vision": True,
#         "Object_width": int(block_size * 1),
#         "Object_height": int(block_size * 1),
#         "Render_when": 0
#         },
#     {
#         "Type": "Object",
#         "Name": "Maze_End_Left",
#         "ID": 94,
#         "Breakable": False,
#         "Block_vision": True,
#         "Collision_box": [0, 0, 1, 1],
#         "Object_width": int(block_size * 1),
#         "Object_height": int(block_size * 1),
#         "Render_when": 0
#         },
#     {
#         "Type": "Object",
#         "Name": "Maze_End_Top",
#         "ID": 95,
#         "Breakable": False,
#         "Block_vision": True,
#         "Collision_box": [0, 0, 1, 1],
#         "Object_width": int(block_size * 1),
#         "Object_height": int(block_size * 1),
#         "Render_when": 0
#         },
#     {
#         "Type": "Object",
#         "Name": "Maze_End_Right",
#         "ID": 96,
#         "Breakable": False,
#         "Block_vision": True,
#         "Collision_box": [0, 0, 1, 1],
#         "Object_width": int(block_size * 1),
#         "Object_height": int(block_size * 1),
#         "Render_when": 0
#         },
#     {
#         "Type": "Object",
#         "Name": "Maze_End_Bottom",
#         "ID": 97,
#         "Breakable": False,
#         "Block_vision": True,
#         "Collision_box": [0, 0, 1, 1],
#         "Object_width": int(block_size * 1),
#         "Object_height": int(block_size * 1),
#         "Render_when": 0
#         },
#     {
#         "Type": "Object",
#         "Name": "Maze_End_Bottom",
#         "ID": 977,
#         "Breakable": False,
#         "Block_vision": True,
#         "Collision_box": [0, 0, 1, 1],
#         "Object_width": int(block_size * 1),
#         "Object_height": int(block_size * 1),
#         "Render_when": 0
#         },
#     {
#         "Type": "Object",
#         "Name": "Puzzle_Piece",
#         "ID": 89,
#         "Object_width": int(block_size * 1),
#         "Object_height": int(block_size * 1),
#         "Render_when": 0
#         },
#     {
#         "Type": "Object",
#         "Name": "Maze_Ground_Keyhole",
#         "ID": 11,
#         "Breakable": False,
#         "Object_width": int(block_size * 1),
#         "Object_height": int(block_size * 1),
#         "Render_when": (block_size * -1)
#         },
#     {
#         "Type": "Object",
#         "Name": "Keyholder_without_key",
#         "ID": 981,
#         "Breakable": False,
#         "Collision_box": [0, 0, 1, 1],
#         "Object_width": int(block_size * 1),
#         "Object_height": int(block_size * 1),
#         "Render_when": (block_size * -1)
#         },
#     {
#         "Type": "Object",
#         "Name": "Keyholder_with_key",
#         "ID": 982,
#         "Breakable": False,
#         "Collision_box": [0, 0, 1, 1],
#         "Object_width": int(block_size * 1),
#         "Object_height": int(block_size * 1),
#         "Render_when": (block_size * -1)
#         },
#     {
#         "Type": "Object",
#         "Name": "Status_gray",
#         "ID": 500,
#         "Breakable": False,
#         "Object_width": int(block_size * 1),
#         "Object_height": int(block_size * 1),
#         "Render_when": (block_size * -1)
#         },
#     {
#         "Type": "Object",
#         "Name": "Status_yellow",
#         "ID": 550,
#         "Breakable": False,
#         "Object_width": int(block_size * 1),
#         "Object_height": int(block_size * 1),
#         "Render_when": (block_size * -1)
#         },
#     {
#         "Type": "Object",
#         "Name": "Status_green",
#         "ID": 555,
#         "Breakable": False,
#         "Object_width": int(block_size * 1),
#         "Object_height": int(block_size * 1),
#         "Render_when": (block_size * -1)
#         },

#     {
#         "Type": "Object",
#         "Name": "Maze_Wall",
#         "ID": 900,
#         "Breakable": False,
#         "Object_width": int(block_size * 1),
#         "Object_height": int(block_size * 1),
#         "Render_when": (block_size * -1)
#     },

#     {
#         "Type": "Object",
#         "Name": "Maze_Start_Bottom",
#         "ID": 909,
#         "Breakable": False,
#         "Object_width": int(block_size * 1),
#         "Object_height": int(block_size * 1),
#         "Render_when": (block_size * -1)
#     },

#     {
#         "Type": "Object",
#         "Name": "Final_Maze_Ground",
#         "ID": 988,
#         "Breakable": False,
#         "Object_width": int(block_size * 1),
#         "Object_height": int(block_size * 1),
#         "Render_when": (block_size * -1)
#         },

#     {
#         "Type": "Object",
#         "Name": "Void",
#         "ID": 999,
#         "Collision_box": [0, 0, 1, 1],
#         "Breakable": False,
#         "Object_width": int(block_size * 1),
#         "Object_height": int(block_size * 1),
#         "Render_when": (block_size * -1)
#         },

#     {
#         "Type": "Object",
#         "Name": "Endgate",
#         "ID": 1000,
#         "Breakable": False,
#         "Object_width": int(block_size * 2),
#         "Object_height": int(block_size * 2),
#         "Render_when": (block_size * -1)
#         },

# ]

# # Testida asju mis on seotud ainult item'ga
# if __name__ == "__main__":
#     item_name_to_find = "Rock"
#     item_value_to_find = "Collision_box"

#     # Otsib listist itemi nime ja otsitavad valued
#     for item in items_list:
#         try:
#             if item["Name"].capitalize() == item_name_to_find.capitalize():
#                 item_value = item[item_value_to_find]
#                 print(f"The {item_value_to_find} of {item_name_to_find} is {item_value}")
#                 break  # Väljub loopist peale itemi nime / value leidmist

#         except:
#             print(f"{item_name_to_find} has no {item_value_to_find}.")
#             break  # Väljub loopist kui itemi nime / valuet ei leitud

#     else:
#         # Kui itemi nime / value ei leitud listist
#         print(f"{item_name_to_find} not found in the list")

#     print()
#     print()
#     print()

#     # Tekitab tühja listi kuhu paneb itemid mille type on object
#     object_items = []

#     # Otsib listist itemi ID'd mille type on object
#     for item in items_list:
#         if item.get("Type") == "Object":
#             object_items.append(item)

#     # Otsib itemi ID / Collision_boxi ja prindib need välja ka siis kui listis pole seda olemas
#     for object_item in object_items:
#         print("ID:", object_item.get("ID", None))
#         print("HP:", object_item.get("HP", None))
#         print("Collision_box:", object_item.get("Collision_box", None))
#         print("test:", object_item.get("test", "Mind ei ole listis"))
#         print()
