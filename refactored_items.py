# from variables import UniversalVariables


class Item:
    def __init__(self, type: str, name: str, id: int, cookable: str=False):
        self.type = type
        self.name = name
        self.id = id
        self.cookable = cookable


class ToolItem(Item):
    def __init__(
            self,
            name: str, id: int,
            recipe: [list[str, ...], list[int | float, ...], int]=None,  # {"Recipe": {"Stick": 2, "Oak_Planks": 3}, "Amount": 1}
    ) -> None:

        super().__init__('Tool', name, id)
        self.recipe = recipe


class ObjectItem(Item):
    def __init__(
            self,
            name: str, id: int, hp: int,
            width: int | float=1, height: int | float=1, render_when: int | float=None,
            
            recipe: [list[str, ...], list[int | float, ...], int]=None,# {"Recipe": {"Stick": 2, "Oak_Planks": 3}, "Amount": 1}
            drops: tuple[list[str, ...], list[int | float, ...], int]=None,  # drops=(['Stone', 'Coal'], [0.85, 0.15], 1)
            breakable=False, placeable=False, cookable=False
    ) -> None:

        super().__init__('Object', name, id, cookable)
        self.hp = hp
        self.recipe = recipe
        self.width = width
        self.height = height
        self.render_when = render_when
        self.drops = drops
        self.breakable = breakable
        self.placeable = placeable

class WorldItem(Item):
    def __init__(self, 
            name: str, id: int,
            width: int, height: int,
            render_when: int | float=None, cookable: str = False
    ) -> None:
        
        super().__init__('World', name, id, cookable)
        self.width = width
        self.height = height
        self.render_when = render_when


class MineralItem(Item):
    def __init__(
            self,
            name: str, id: int,
            recipe: list[dict[str, dict[str, int, ...], str, int], ...]=None, #  {"Recipe": {"Stick": 2, "Oak_Planks": 3}, "Amount": 1},
            cookable=False
    ) -> None:

        super().__init__('Mineral', name, id, cookable)
        self.recipe = recipe


class ConsumableItem(Item):
    def __init__(
            self,
            name: str, id: int,
            satisfaction_gain: int | float=None,
            hunger_resistance: int | float=None, thirst_resistance: int | float=None,
            healing_amount: int=None,
            timer: int=None,
            cookable=False
    ) -> None:

        super().__init__('Consumable', name, id, cookable)
        self.satisfaction_gain = satisfaction_gain
        self.hunger_resistance = hunger_resistance
        self.healing_amount = healing_amount
        self.timer = timer
        self.thirst_resistance = thirst_resistance

block_size = 100  # UniversalVariables.block_size

items_list = [
    # - # - # - # - # - # - # Tools # - # - # - # - # - # - #

    ToolItem(
        name="Wood_Pickaxe",
        id=50,
        recipe=[
            {"Recipe": {"Stick": 2, "Oak_Planks": 3}, "Amount": 1}
        ]
    ),

    ToolItem(
        name="Wood_Axe",
        id=51,
        recipe=[
            {"Recipe": {"Stick": 2, "Oak_Planks": 3}, "Amount": 1}
        ]
    ),

    ToolItem(
        name="Wood_Shovel",
        id=52,
        recipe=[
            {"Recipe": {"Stick": 2, "Oak_Planks": 2}, "Amount": 1}
        ]
    ),

    ToolItem(
        name="Wood_Sword",
        id=53,
        recipe=[
            {"Recipe": {"Stick": 2, "Oak_Planks": 2}, "Amount": 1}
        ]
    ),

    ToolItem(
        name="Stone_Pickaxe",
        id=54,
        recipe=[
            {"Recipe": {"Stick": 2, "Stone_Shard": 3}, "Amount": 1}
        ]
    ),

    ToolItem(
        name="Stone_Axe",
        id=55,
        recipe=[
            {"Recipe": {"Stick": 2, "Stone_Shard": 3}, "Amount": 1}
        ]
    ),

    ToolItem(
        name="Rock_Sword",
        id=57,
        recipe=[
            {"Recipe": {"Stick": 2, "Stone_Shard": 2}, "Amount": 1}
        ]
    ),

    ToolItem(
        name="Flashlight",
        id=31,
    ),

    ToolItem(
        name="Stone_Shard",
        id=27,
        recipe=[
            {"Recipe": {"Stone": 2}, "Amount": 1,}
        ]
    ),

    ToolItem(
        name="Glowstick",
        id=28,
    ),

    # - # - # - # - # - # - # World # - # - # - # - # - # - #

    # maze

    WorldItem(
        name='Maze_Ground',
        id=98,
        width=int(block_size),
        height=int(block_size)
    ),

    WorldItem(
        name='Maze_Wall',
        id=99,
        width=int(block_size),
        height=int(block_size)
    ),

    WorldItem(
        name='Maze_Wall',
        id=99,
        width=int(block_size),
        height=int(block_size)
    ),

    WorldItem(
        name='Maze_Ground_Keyhole',
        id=11,
        width=int(block_size),
        height=int(block_size)
    ),

    WorldItem(
        name='Keyholder_with_key',
        id=982,
        width=int(block_size),
        height=int(block_size)
    ),

    WorldItem(
        name='Keyholder_without_key',
        id=981,
        width=int(block_size),
        height=int(block_size)
    ),
    
    WorldItem(
        name='Status_gray',
        id=500,
        width=int(block_size),
        height=int(block_size)
    ),

    WorldItem(
        name='Status_yellow',
        id=550,
        width=int(block_size),
        height=int(block_size)
    ),

    WorldItem(
        name='Status_green',
        id=555,
        width=int(block_size),
        height=int(block_size)
    ),

    WorldItem(
        name='Final_Maze_Ground',
        id=988,
        width=int(block_size),
        height=int(block_size)
    ),

    WorldItem(
        name='Final_Maze_Ground_2',
        id=9882,
        width=int(block_size),
        height=int(block_size)
    ),

    WorldItem(
        name='Void',
        id=999,
        width=int(block_size),
        height=int(block_size)
    ),

    WorldItem(
        name='Endgate',
        id=1000,
        width=int(block_size),
        height=int(block_size)
    ),


    # blade maze

    WorldItem(
        name='Maze_Blade',
        id=9099,
        width=int(block_size),
        height=int(block_size)
    ),

    WorldItem(
        name='Maze_Blade',
        id=989,
        width=int(block_size),
        height=int(block_size)
    ),

    WorldItem(
        name='Maze_Blade',
        id=900,
        width=int(block_size),
        height=int(block_size)
    ),

    WorldItem(
        name='Maze_Ground',
        id=9099_98,
        width=int(block_size),
        height=int(block_size)
    ),

    WorldItem(
        name='Maze_Ground',
        id=989_98,
        width=int(block_size),
        height=int(block_size)
    ),
    
    # doors

    WorldItem(
        name='Maze_Start_Top',
        id=91,
        width=int(block_size),
        height=int(block_size)
    ),

    WorldItem(
        name='Maze_Start_Right',
        id=92,
        width=int(block_size),
        height=int(block_size)
    ),

    WorldItem(
        name='Maze_Start_Left',
        id=90,
        width=int(block_size),
        height=int(block_size)
    ),

    WorldItem(
        name='Maze_Start_Bottom',
        id=93,
        width=int(block_size),
        height=int(block_size)
    ),

    WorldItem(
        name='Maze_Start_Bottom',
        id=933,
        width=int(block_size),
        height=int(block_size)
    ),

    WorldItem(
        name='Maze_End_Bottom',
        id=97,
        width=int(block_size),
        height=int(block_size)
    ),

    WorldItem(
        name='Maze_End_Bottom',
        id=977,
        width=int(block_size),
        height=int(block_size)
    ),

    WorldItem(
        name='Maze_End_Top',
        id=95,
        width=int(block_size),
        height=int(block_size)
    ),

    WorldItem(
        name='Maze_End_Right',
        id=96,
        width=int(block_size),
        height=int(block_size)
    ),

    WorldItem(
        name='Maze_End_Left',
        id=94,
        width=int(block_size),
        height=int(block_size)
    ),

    # - # - # - # - # - # - # Objects # - # - # - # - # - # - #

    ObjectItem(
        name="Rock",
        id=2,
        hp=5,

        width=int(block_size * 0.69),
        height=int(block_size * 0.55),
        render_when=-(block_size * 0.1),

        drops=(['Stone', 'Coal'], [0.85, 0.15], 1),

        breakable=True

    ),

    ObjectItem(
        name="Farmland",
        id=3,
        hp=100,

        width=int(block_size),
        height=int(block_size),

    ),

    ObjectItem(
        name="Oak_Tree",
        id=4,
        hp=5,

        render_when=block_size * 1.5,

        drops=(['Oak_Log'], [1], 1),

        breakable=True
    ),

    ObjectItem(
        name="Oak_Tree_Stump",
        id=5,
        hp=100,

        width=int(block_size * 2),
        height=int(block_size * 2),
        render_when=block_size * 0.6,

    ),

    ObjectItem(
        name="String",
        id=6,
        hp=1,

        breakable=True,
        placeable=True

    ),

    ObjectItem(
        name="Wheat_Crop",
        id=7,
        hp=1,

        render_when=block_size * 0.2,

        drops=(['Wheat'], [1], 1),

        breakable=True

    ),

    ObjectItem(
        name="Campfire",
        id=8,
        hp=1,

        render_when=(block_size * 0.2),

        recipe=[
            {"Recipe": {"Oak_Log": 2, "Coal": 1, "Stone": 3}, "Amount": 1},
        ],

        breakable=True,
        placeable=True
    ),

    ObjectItem(
        name="Big_Bush",
        id=9,
        hp=1,

        width=int(block_size * 0.7),
        height=int(block_size * 0.7),
        render_when=(block_size * 0.2),

        breakable=True
    ),

    ObjectItem(
        name="Maze_Key",
        id=10,
        hp=1,

        width=int(block_size * 0.45),
        height=int(block_size * 0.45),

        breakable=True,
    ),

    ObjectItem(
        name="Maze_Key_1",
        id=12,
        hp=1,

        width=int(block_size * 0.45),
        height=int(block_size * 0.45),

        breakable=True,
    ),

    ObjectItem(
        name="Maze_Key_2",
        id=13,
        hp=1,

        width=int(block_size * 0.45),
        height=int(block_size * 0.45),

        breakable=True,
    ),

    ### TODO: kuhu panna? object - tool?
    ObjectItem(
        name="Torch",
        id=30,
        hp=1,

        recipe=[
            {"Recipe": {"Stick": 2, "Coal": 1}, "Amount": 4},
        ],

        breakable=True,
        placeable=True
    ),

    ObjectItem(
        name="Campfire",
        id=8,
        hp=1,

        width=int(block_size),
        height=int(block_size),
        render_when=(block_size * 0.2),

        recipe=[
            {"Recipe": {"Oak_Log": 2, "Coal": 1, "Stone": 3}, "Amount": 1},
        ],

        breakable=True,
        placeable=True
    ),

    ObjectItem(
        name="Campfire",
        id=8,
        hp=1,

        width=int(block_size),
        height=int(block_size),
        render_when=(block_size * 0.2),

        recipe=[
            {"Recipe": {"Oak_Log": 2, "Coal": 1, "Stone": 3}, "Amount": 1},
        ],

        breakable=True,
        placeable=True
    ),

    ObjectItem(
        name="Campfire",
        id=8,
        hp=1,

        width=int(block_size),
        height=int(block_size),
        render_when=(block_size * 0.2),

        recipe=[
            {"Recipe": {"Oak_Log": 2, "Coal": 1, "Stone": 3}, "Amount": 1},
        ],

        breakable=True,
        placeable=True
    ),
    ObjectItem(
        name="Opened_Loot_Barrel",
        id=1002,
        width=int(block_size * 0.45),
        height=int(block_size * 0.45),
        render_when=(block_size * 0.2),
    ),

    ObjectItem(
        name="Loot_Barrel",
        id=1001,
        width=int(block_size * 0.45),
        height=int(block_size * 0.45),
    ),

    # - # - # - # - # - # - # Minerals # - # - # - # - # - # - #

    MineralItem(
        name="Maze_Key_1",
        id=12,
    ),

    MineralItem(
        name="Maze_Key_2",
        id=13,
    ),

    MineralItem(
        name="Oak_Log",
        id=19,
    ),

    MineralItem(
        name='Oak_Planks',
        id=21,
        recipe=[
            {"Recipe": {"Oak_Log": 1}, "Amount": 2}
        ]
    ),

    MineralItem(
        name="Stick",
        id=22,
        recipe=[
            {"Recipe": {"Oak_Planks": 1}, "Amount": 2},
        ]
    ),

    MineralItem(
        name="Stone",
        id=23,
    ),

    MineralItem(
        name="Coal",
        id=29,
    ),

    MineralItem(
        name="Raw_Meat",
        id=36,
        cookable="Cooked_Meat"
    ),


    MineralItem(
        name="Wheat",
        id=39,
    ),

    MineralItem(
        name="Bread_Dough",
        id=40,
        recipe=[
            {"Recipe": {"Wheat": 3}, "Amount": 1}
        ]
    ),

    MineralItem(
        name=,
        id=,
        recipe=[
            {"Recipe": {"": }, "Amount": },
        ]
    ),

    MineralItem(
        name=,
        id=,
        recipe=[
            {"Recipe": {"": }, "Amount": },
        ]
    ),

    MineralItem(
        name=,
        id=,
        recipe=[
            {"Recipe": {"": }, "Amount": },
        ]
    ),

    # - # - # - # - # - # - # Consumables # - # - # - # - # - # - #

    ConsumableItem(
        name="Bread",
        id=35,
        satisfaction_gain=1,
        hunger_resistance=150
    ),

    ConsumableItem(
        name="Bad_Bread",
        id=10000,
        satisfaction_gain=-1.75,
        hunger_resistance=-200
    ),

    ConsumableItem(
        name="Cooked_Meat",
        id=37,
        satisfaction_gain=2,
        hunger_resistance=500
    ),

    ConsumableItem(
        name="Bottle_Water",
        id=38,
        satisfaction_gain=3,
        hunger_resistance=350
    ),

    ConsumableItem(
        name="Berry",
        id=1014,
        satisfaction_gain=2,
        hunger_resistance=150
    ),

    ConsumableItem(
    name="Bandage",
    id=32,
    healing_amount=5,
    ),

    ConsumableItem(
    name="Serum",
    id=34,
    timer=10,
    ),

    ConsumableItem(
        name="Bottle_Water",
        id=38,
        satisfaction_gain=3,
        thirst_resistance=150
    ),

    ConsumableItem(
    name="Serum",
    id=34,
    timer=10,
    ),

    # ConsumableItem(
    #     name="",
    #     id=,
    #     satisfaction_gain=,
    #     hunger_resistance=
    # ),

]


# Teeb dict'id, et saaks kiiremini asju ülesse otsida. (efficient)
items_dict_by_id = {item.id: item for item in items_list}
items_dict_by_name = {item.name: item for item in items_list}


# Otsib itemi selle ID järgi.
def find_item_by_id(id) -> dict:
    return items_dict_by_id.get(id, None)


# # Otsib itemi selle Name järgi.
def find_item_by_name(search_name) -> dict:
    return items_dict_by_name.get(search_name, None)


# Otsib valitud attribute item'ite seast.
def search_item_from_items(type: type, item_name_or_id: str | int, target_attribute: str) -> any:
    # Näidis:
    #   search_item_from_items(type=ObjectItem, item_name_or_id=2, target_attribute='drops')
    #   search_item_from_items(type=ConsumableItem, item_name_or_id='bread', target_attribute='satisfaction_gain')

    item = None

    if isinstance(item_name_or_id, int):
        item = find_item_by_id(item_name_or_id)

    elif isinstance(item_name_or_id, str):
        item = find_item_by_name(item_name_or_id.capitalize())

    # Vaatab kas item'il on target_attribute, kui ei ole siis return'ib None.
    if item and isinstance(item, type):
        return getattr(item, target_attribute.lower(), None)
    return None

# result = search_item_from_items(type=ConsumableItem, item_name_or_id='berry', target_attribute='satisfaction_gain')
# print(result)