import random

from variables import UniversalVariables

block_size = UniversalVariables.block_size
"""
Collision_box: [offset_x, offset_y, width, height]


"Recipes": [
        {"Recipe": {"Item Name": Amount needed}, "Amount": Amount receive},
        {"Recipe": {"Item Name": Amount needed, "Item Name": Amount needed}, "Amount": Amount receive},
]



"Breakable": True ///

"Breakable": [
    {"hardness": "None"},        +///     None: any // Wood: wood & higher // Stone & higher....     ///+
    {"amount": ("Item Name you receive", Amount receive)},
],



///



"""


### TODO: Blocke lõhkudes peab määrama palju ja mida ta saab näiteks "Oak_Tree"d
### TODO: lõhkudes ei ta lic puukest invi, selle asemel saab ta 2 "Oak_Plank"u

items_list = [
    {
        "Type": "Object",
        "Name": "Rock",
        "ID": 2,
        "HP": 5,
        "Breakable": True,
        # "Breakable": [
        #     {"hardness": "Wood"},
        #     {"amount": ("Stone", random.randint(1, 5))},
        # ],
        "Object_width": int(block_size * 0.69),  # suhe 5:4
        "Object_height": int(block_size * 0.55),
        "Render_when": -(block_size * 0.1)
    },

    {
        "Type": "Object",
        "Name": "Farmland",
        "ID": 3,
        "Object_width": int(block_size * 0.5),
        "Object_height": int(block_size * 0.5),
    },

    {
        "Type": "Object",
        "Name": "Oak_Tree",
        "ID": 4,
        "HP": 5,
        "Breakable": True,
        # "Breakable": [
        #     {"hardness": "None"},
        #     {"amount": ("Oak_Wood", random.randint(1, 3))},
        # ],
        "Object_width": int(block_size * 2),
        "Object_height": int(block_size * 2),
        "Render_when": block_size * 0.8
    },

    {
        "Type": "Object",
        "Name": "Oak_Tree_Stump",
        "ID": 5,
        "Breakable": False,
        "Object_width": int(block_size * 2),
        "Object_height": int(block_size * 2),
        "Render_when": -(block_size * 0.8)
    },

    {
        "Type": "Object",
        "Name": "Flower",
        "ID": 6,
        "Breakable": True,
        "Placeable": True,
        "Object_width": int(block_size * 0.5),
        "Object_height": int(block_size * 0.5),
        "Render_when": -(block_size * 0.23)
    },

    {
        "Type": "Object",
        "Name": "Wheat",
        "ID": 7,
        "Breakable": True,
        "Object_width": int(block_size * 1),
        "Object_height": int(block_size * 1),
        "Render_when": (block_size * .2)
    },

    {
        "Type": "Object",
        "Name": "Campfire",
        "ID": 8,
        "Placeable": True,
        "Breakable": True,
        "Object_width": int(block_size * 1),
        "Object_height": int(block_size * 1),
        "Render_when": (block_size * -1),

        "Recipes": [
            {"Recipe": {"Oak_Log": 2, "Coal": 1, "Stone": 3}, "Amount": 1},
        ],

    },

    {
        "Type": "Object",
        "Name": "Big_Bush",
        "ID": 9,
        "Breakable": True,
        "Object_width": int(block_size * .7),
        "Object_height": int(block_size * .7),
        "Render_when": (block_size * .2)
    },

    {
        "Type": "Object",
        "Name": "Maze_Key",
        "ID": 10,
        "Breakable": True,
        "Object_width": int(block_size * 0.45),
        "Object_height": int(block_size * 0.45),
        "Render_when": (block_size * -1)
    },

    # Items

    {
        "Type": "Mineral",
        "Name": "Oak_Log",
        "ID": 19,
    },

    {
        "Type": "Mineral",
        "Name": "Oak_Wood",
        "Recipes": [
            {"Recipe": {"Oak_Log": 1}, "Amount": 2},
        ],
        "Amount": 4,
        "ID": 20,
        # "Placeable": True,
        # "Breakable": True,
    },

    {
        "Type": "Mineral",
        "Name": "Oak_Planks",
        "ID": 21,
        "Recipes": [
            {"Recipe": {"Oak_Wood": 1}, "Amount": 2},  ### TODO: SEE KASUTAB SELLE ITEMI IGAT RETSEPTI EHK SIIS PRAEGU SIIN TA CRAFTIB OAK WOODIST JA OAK TREEST EHK SIIS ÜHE CLICKIGA SAAB 6 ÄRA VAJA FIXIDA
            # {"Recipe": {"Oak_Tree": 1}, "Amount": 4},
        ],
        # "Placeable": True,
        # "Breakable": True,
    },

    {
        "Type": "Mineral",
        "Name": "Stick",
        "ID": 22,
        "Recipes": [
            # {"Recipe": {"Oak_Tree": 1}, "Amount": 8},
            # {"Recipe": {"Oak_Wood": 1}, "Amount": 4},
            {"Recipe": {"Oak_Planks": 1}, "Amount": 2},
        ],
    },

    {
        "Type": "Mineral",
        "Name": "Stone",
        "ID": 23,
        # "Placeable": True,
        # "Breakable": True,
    },

    {
        "Type": "Tool",
        "Name": "Wood_Pickaxe",
        "ID": 24,
        "Recipes": [
            {"Recipe": {"Stick": 2, "Oak_Planks": 3}, "Amount": 1},
        ],
        "Durability": 128,
    },

    {
        "Type": "Tool",
        "Name": "Wood_Axe",
        "ID": 25,
        "Recipes": [
            {"Recipe": {"Stick": 2, "Oak_Planks": 3}, "Amount": 1},
        ],
        "Durability": 128,
    },

    {
        "Type": "Tool",
        "Name": "Wood_Shovel",
        "ID": 26,
        "Recipes": [
            {"Recipe": {"Stick": 2, "Oak_Planks": 2}, "Amount": 1,},
        ],
        "Durability": 128,
    },

    {
        "Type": "Tool",
        "Name": "Stone_Shard",
        "ID": 27,
        "Recipes": [
            {"Recipe": {"Stone": 2}, "Amount": 1,},  # Tuleb Stone'iks ära muuta
        ],
        "Durability": 128,
    },

    {
        "Type": "Tool",
        "Name": "Small_Rock_Sword",
        "ID": 28,
        "Recipes": [
            {"Recipe": {"Stick": 2, "Stone_Shard": 1}, "Amount": 1},
        ],
        "Durability": 256,
    },

    {
        "Type": "Mineral",
        "Name": "Coal",
        "ID": 29,
    },

    {
        "Type": "Tool",
        "Name": "Torch",
        "ID": 30,
        "Recipes": [
            {"Recipe": {"Stick": 2, "Coal": 1}, "Amount": 4},
        ],
        "Durability": 256,
        # "Placeable": True,
        # "Breakable": True,
    },

    {
        "Type": "Tool",
        "Name": "Flashlight",
        "ID": 31,
    },

    {
        "Type": "Tool",
        "Name": "Bandage",
        "ID": 32,
    },

    {
        "Type": "Tool",
        "Name": "Canteen",
        "ID": 33,
    },

    {
        "Type": "Tool",
        "Name": "Serum",
        "ID": 34,
    },

# food

    {
        "Type": "Food",
        "Name": "Bread",
        "ID": 35,
        "Satisfaction_Gain": 1,  # Kui palju hunger bar juurde saab
        "Hunger_Resistance": 150,  # Mitu ticki ei lähe hungerit
    },

    {
        "Type": "Food",
        "Name": "Bad_Bread",
        "ID": 36,
        "Satisfaction_Gain": -1.75,  # Kui palju hunger bar juurde saab
        "Hunger_Resistance": -200,  # Mitu ticki ei lähe hungerit
    },

    {
        "Type": "Food",
        "Name": "Meat",
        "ID": 37,
        "Satisfaction_Gain": 2,  # Kui palju hunger bar juurde saab
        "Hunger_Resistance": 350,  # Mitu ticki ei lähe hungerit
    },

    {
        "Type": "Food",
        "Name": "Bottle_Water",
        "ID": 38,
        "Satisfaction_Gain": 3,
        "Thirst_Resistance": 350,
    },

    # Unbreakable Blocks - Items

### TODO: Blocke lõhkudes peab määrama palju ja mida ta saab näiteks "Oak_Tree"d
### TODO: lõhkudes ei ta lic puukest invi, selle asemel saab ta 2 "Oak_Plank"u

        {
        "Type": "Object",
        "Name": "Farmland",
        "ID": 107,
        "Breakable": False,
        "Block_vision": False,
        "Object_width": int(block_size * 1),
        "Object_height": int(block_size * 1),
        "Render_when": -block_size
        },
    {
        "Type": "Object",
        "Name": "Maze_Ground",
        "ID": 98,
        "Breakable": False,
        "Block_vision": False,
        "Object_width": int(block_size * 1),
        "Object_height": int(block_size * 1),
        "Render_when": -block_size
        },
    {
        "Type": "Object",
        "Name": "Maze_Wall",
        "ID": 99,
        "Breakable": False,
        "Block_vision": True,
        "Collision_box": [0, 0, 1, 1],
        "Object_width": int(block_size * 1),
        "Object_height": int(block_size * 1),
        "Render_when": -block_size
        },
    ### maze blade
    {
        "Type": "Object",
        "Name": "Maze_Blade",
        "ID": 9099,
        "Breakable": False,
        "Block_vision": True,
        "Collision_box": [0, 0, 1, 1],
        "Object_width": int(block_size * 1),
        "Object_height": int(block_size * 1),
        "Render_when": -block_size
        },
    {
        "Type": "Object",
        "Name": "Maze_Blade",
        "ID": 989,
        "Breakable": False,
        "Block_vision": True,
        "Collision_box": [0, 0, 1, 1],
        "Object_width": int(block_size * 1),
        "Object_height": int(block_size * 1),
        "Render_when": -block_size
        },
    {
        "Type": "Object",
        "Name": "Maze_Blade",
        "ID": 900,
        "Breakable": False,
        "Block_vision": True,
        "Collision_box": [0, 0, 1, 1],
        "Object_width": int(block_size * 1),
        "Object_height": int(block_size * 1),
        "Render_when": -block_size
        },
    {
        "Type": "Object",
        "Name": "Maze_Ground",
        "ID": 9099_98,
        "Breakable": False,
        "Block_vision": True,
        "Object_width": int(block_size * 1),
        "Object_height": int(block_size * 1),
        "Render_when": -block_size
        },
    {
        "Type": "Object",
        "Name": "Maze_Ground",
        "ID": 989_98,
        "Breakable": False,
        "Block_vision": True,
        "Object_width": int(block_size * 1),
        "Object_height": int(block_size * 1),
        "Render_when": -block_size
        },
    ###
    {
        "Type": "Object",
        "Name": "Maze_Start_Left",
        "ID": 90,
        "Breakable": False,
        "Block_vision": True,
        "Object_width": int(block_size * 1),
        "Object_height": int(block_size * 1),
        "Render_when": 0
        },
    {
        "Type": "Object",
        "Name": "Maze_Start_Top",
        "ID": 91,
        "Breakable": False,
        "Block_vision": True,
        "Object_width": int(block_size * 1),
        "Object_height": int(block_size * 1),
        "Render_when": 0
        },
    {
        "Type": "Object",
        "Name": "Maze_Start_Right",
        "ID": 92,
        "Breakable": False,
        "Block_vision": True,
        "Object_width": int(block_size * 1),
        "Object_height": int(block_size * 1),
        "Render_when": 0
        },
    {
        "Type": "Object",
        "Name": "Maze_Start_Bottom",
        "ID": 93,
        "Breakable": False,
        "Block_vision": True,
        "Object_width": int(block_size * 1),
        "Object_height": int(block_size * 1),
        "Render_when": 0
        },
    {
        "Type": "Object",
        "Name": "Maze_Start_Bottom",
        "ID": 933,
        "Breakable": False,
        "Block_vision": True,
        "Object_width": int(block_size * 1),
        "Object_height": int(block_size * 1),
        "Render_when": 0
        },
    {
        "Type": "Object",
        "Name": "Maze_End_Left",
        "ID": 94,
        "Breakable": False,
        "Block_vision": True,
        "Collision_box": [0, 0, 1, 1],
        "Object_width": int(block_size * 1),
        "Object_height": int(block_size * 1),
        "Render_when": 0
        },
    {
        "Type": "Object",
        "Name": "Maze_End_Top",
        "ID": 95,
        "Breakable": False,
        "Block_vision": True,
        "Collision_box": [0, 0, 1, 1],
        "Object_width": int(block_size * 1),
        "Object_height": int(block_size * 1),
        "Render_when": 0
        },
    {
        "Type": "Object",
        "Name": "Maze_End_Right",
        "ID": 96,
        "Breakable": False,
        "Block_vision": True,
        "Collision_box": [0, 0, 1, 1],
        "Object_width": int(block_size * 1),
        "Object_height": int(block_size * 1),
        "Render_when": 0
        },
    {
        "Type": "Object",
        "Name": "Maze_End_Bottom",
        "ID": 97,
        "Breakable": False,
        "Block_vision": True,
        "Collision_box": [0, 0, 1, 1],
        "Object_width": int(block_size * 1),
        "Object_height": int(block_size * 1),
        "Render_when": 0
        },
    {
        "Type": "Object",
        "Name": "Maze_End_Bottom",
        "ID": 977,
        "Breakable": False,
        "Block_vision": True,
        "Collision_box": [0, 0, 1, 1],
        "Object_width": int(block_size * 1),
        "Object_height": int(block_size * 1),
        "Render_when": 0
        },
    {
        "Type": "Object",
        "Name": "Puzzle_Piece",
        "ID": 89,
        "Object_width": int(block_size * 1),
        "Object_height": int(block_size * 1),
        "Render_when": 0
        },
    {
        "Type": "Object",
        "Name": "Maze_Ground_Keyhole",
        "ID": 11,
        "Breakable": False,
        "Object_width": int(block_size * 1),
        "Object_height": int(block_size * 1),
        "Render_when": (block_size * -1)
        },
    {
        "Type": "Object",
        "Name": "Keyholder_without_key",
        "ID": 981,
        "Breakable": False,
        "Collision_box": [0, 0, 1, 1],
        "Object_width": int(block_size * 1),
        "Object_height": int(block_size * 1),
        "Render_when": (block_size * -1)
        },
    {
        "Type": "Object",
        "Name": "Keyholder_with_key",
        "ID": 982,
        "Breakable": False,
        "Collision_box": [0, 0, 1, 1],
        "Object_width": int(block_size * 1),
        "Object_height": int(block_size * 1),
        "Render_when": (block_size * -1)
        },
    {
        "Type": "Object",
        "Name": "Status_gray",
        "ID": 500,
        "Breakable": False,
        "Object_width": int(block_size * 1),
        "Object_height": int(block_size * 1),
        "Render_when": (block_size * -1)
        },
    {
        "Type": "Object",
        "Name": "Status_yellow",
        "ID": 550,
        "Breakable": False,
        "Object_width": int(block_size * 1),
        "Object_height": int(block_size * 1),
        "Render_when": (block_size * -1)
        },
    {
        "Type": "Object",
        "Name": "Status_green",
        "ID": 555,
        "Breakable": False,
        "Object_width": int(block_size * 1),
        "Object_height": int(block_size * 1),
        "Render_when": (block_size * -1)
        },
    {
        "Type": "Object",
        "Name": "Maze_Start_Bottom",
        "ID": 909,
        "Breakable": False,
        "Object_width": int(block_size * 1),
        "Object_height": int(block_size * 1),
        "Render_when": (block_size * -1)
    },
    {
        "Type": "Object",
        "Name": "Final_Maze_Ground",
        "ID": 988,
        "Breakable": False,
        "Object_width": int(block_size * 1),
        "Object_height": int(block_size * 1),
        "Render_when": (block_size * -1)
        },
    {
        "Type": "Object",
        "Name": "Final_Maze_Ground_2",
        "ID": 9882,
        "Breakable": False,
        "Object_width": int(block_size * 1),
        "Object_height": int(block_size * 1),
        "Render_when": (block_size * -1)
        },
    {
        "Type": "Object",
        "Name": "Void",
        "ID": 999,
        "Collision_box": [0, 0, 1, 1],
        "Breakable": False,
        "Object_width": int(block_size * 1),
        "Object_height": int(block_size * 1),
        "Render_when": (block_size * -1)
        },
    {
        "Type": "Object",
        "Name": "Endgate",
        "ID": 1000,
        "Breakable": False,
        "Object_width": int(block_size * 2),
        "Object_height": int(block_size * 2),
        "Render_when": (block_size * -1)
        },
    {
        "Type": "Object",
        "Name": "Loot_Barrel",
        "ID": 1001,
        "Breakable": False,
        "Block_vision": False,
        "Object_width": int(block_size * 0.45),
        "Object_height": int(block_size * 0.45),
        "Render_when": -block_size
        },
    {
        "Type": "Object",
        "Name": "Opened_Loot_Barrel",
        "ID": 1002,
        "Breakable": False,
        "Block_vision": False,
        "Object_width": int(block_size * 0.45),
        "Object_height": int(block_size * 0.45),
        "Render_when": -block_size
        },

]

# Testida asju mis on seotud ainult item'ga
if __name__ == "__main__":
    item_name_to_find = "Rock"
    item_value_to_find = "Collision_box"

    # Otsib listist itemi nime ja otsitavad valued
    for item in items_list:
        try:
            if item["Name"].capitalize() == item_name_to_find.capitalize():
                item_value = item[item_value_to_find]
                print(f"The {item_value_to_find} of {item_name_to_find} is {item_value}")
                break  # Väljub loopist peale itemi nime / value leidmist

        except:
            print(f"{item_name_to_find} has no {item_value_to_find}.")
            break  # Väljub loopist kui itemi nime / valuet ei leitud

    else:
        # Kui itemi nime / value ei leitud listist
        print(f"{item_name_to_find} not found in the list")

    print()
    print()
    print()

    # Tekitab tühja listi kuhu paneb itemid mille type on object
    object_items = []

    # Otsib listist itemi ID'd mille type on object
    for item in items_list:
        if item.get("Type") == "Object":
            object_items.append(item)

    # Otsib itemi ID / Collision_boxi ja prindib need välja ka siis kui listis pole seda olemas
    for object_item in object_items:
        print("ID:", object_item.get("ID", None))
        print("HP:", object_item.get("HP", None))
        print("Collision_box:", object_item.get("Collision_box", None))
        print("test:", object_item.get("test", "Mind ei ole listis"))
        print()
