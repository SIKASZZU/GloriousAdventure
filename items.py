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
### TODO: Copy-pastesin seda allapoole kaa

items_list = [
    {
        "Type": "Object",
        "Name": "Rock",
        "ID": 2,
        "HP": 5,

        ### TODO: Muudaks selle selliseks????
        "Breakable": True,
        # "Breakable": [
        #     {"hardness": "Wood"},
        #     {"amount": ("Stone", random.randint(1, 5))},
        # ],
        ### TODO: Ehk siis selle True asemel on see item ja kogus mida sa saad objecti lõhkudes
        ### TODO: Kui "Breakable" ei ole dictis siis seda itemit ei saa lõhkuda

        "Collision_box": [0.3, 0.25, 0.5, 0.4],
        "Object_width": int(block_size * 1),
        "Object_height": int(block_size * 0.8),
        "Render_when": -(block_size * 0.1)
        },
    {
        "Type": "Object",
        "Name": "Oak_Tree",
        "ID": 4,
        "HP": 5,

        ### TODO: Muudaks selle selliseks????

        "Breakable": True,
        # "Breakable": [
        #     {"hardness": "None"},
        #     {"amount": ("Oak_Wood", random.randint(1, 3))},
        # ],
        ### TODO: Ehk siis selle True asemel on see item ja kogus mida sa saad objecti lõhkudes
        ### TODO: Kui "Breakable" ei ole dictis siis seda itemit ei saa lõhkuda

        "Collision_box": [0.85, 0.85, 0.35, 0.7],
        "Object_width": int(block_size * 2),
        "Object_height": int(block_size * 2),
        "Render_when": block_size * 0.8
        },
    {
        "Type": "Object",
        "Name": "Flower",
        "ID": 6,
        "Breakable": True,
        "Placeable": True,
        "Collision_box": [0, 0, 0, 0],
        "Object_width": int(block_size * 0.5),
        "Object_height": int(block_size * 0.5),
        "Render_when": -(block_size * 0.23)
        },
    {
        "Type": "Object",
        "Name": "Mushroom",
        "ID": 6,
        "Breakable": True,
        "Placeable": True,
        "Collision_box": [0, 0, 0, 0],
        "Object_width": int(block_size * 0.3),
        "Object_height": int(block_size * 0.3),
        "Render_when": -(block_size * 0.45)
        },
    {
        "Type": "Object",
        "Name": "Wheat",
        "ID": 7,
        "Breakable": True,
        "Collision_box": [0, 0, 0, 0],
        "Object_width": int(block_size * 1),
        "Object_height": int(block_size * 1),
        "Render_when": (block_size * .2)
        },

    # Items

### TODO: Blocke lõhkudes peab määrama palju ja mida ta saab näiteks "Oak_Tree"d
### TODO: lõhkudes ei ta lic puukest invi, selle asemel saab ta 2 "Oak_Plank"u

    {
        "Type": "Item",
        "Name": "Oak_Wood",
        "Recipes": [
            {"Recipe": {"Oak_Tree": 1}, "Amount": 2},
        ],
        "Amount": 4,
        "ID": 20,
        "Placeable": True,
        "Breakable": True,
    },
    {
        "Type": "Item",
        "Name": "Oak_Planks",
        "ID": 21,
        "Recipes": [
            {"Recipe": {"Oak_Wood": 1}, "Amount": 2},  ### TODO: SEE KASUTAB SELLE ITEMI IGAT RETSEPTI EHK SIIS PRAEGU SIIN TA CRAFTIB OAK WOODIST JA OAK TREEST EHK SIIS ÜHE CLICKIGA SAAB 6 ÄRA VAJA FIXIDA
            {"Recipe": {"Oak_Tree": 1}, "Amount": 4},
        ],
        "Placeable": True,
        "Breakable": True,
        },
    {
        "Type": "Item",
        "Name": "Stick",
        "ID": 22,
        "Recipes": [
            {"Recipe": {"Oak_Tree": 1}, "Amount": 8},
            {"Recipe": {"Oak_Wood": 1}, "Amount": 4},
            {"Recipe": {"Oak_Planks": 1}, "Amount": 2},
        ],
        },
    {
        "Type": "Item",
        "Name": "Stone",
        "ID": 23,
        "Placeable": True,
        "Breakable": True,
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
            {"Recipe": {"Rock": 2}, "Amount": 1,},  # Tuleb Stone'iks ära muuta
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
        "Type": "Item",
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
        "Placeable": True,
        "Breakable": True,
    },

    # Unbreakable Blocks - Items

### TODO: Blocke lõhkudes peab määrama palju ja mida ta saab näiteks "Oak_Tree"d
### TODO: lõhkudes ei ta lic puukest invi, selle asemel saab ta 2 "Oak_Plank"u

    {
        "Type": "Object",
        "Name": "Wall",
        "ID": 99,
        "Breakable": False,
        "Block_vision": True,
        "Collision_box": [0, 0, 1, 1],
        "Object_width": int(block_size * 1),
        "Object_height": int(block_size * 1),
        "Render_when": (block_size * 1)
        },
]

# Testida asju mis on seotud ainult item'ga
if __name__ == "__main__":
    item_name_to_find = "Stone"
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
