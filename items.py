""" K6ik pildid on images/Items folderis, sest need k6ik pildid k2ivad items_list'i kohta. """
""" Folder jaguneb v2iksemateks harudeks classide systeemi j2rgi -> Objects folder on ObjectItemi jaoks. """

from variables import UniversalVariables
block_size = UniversalVariables.block_size


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
            width: int | float=block_size, height: int | float=block_size, render_when: int | float=None,
            
            recipe: [list[str, ...], list[int | float, ...], int]=None,# {"Recipe": {"Stick": 2, "Oak_Planks": 3}, "Amount": 1}
            drops: tuple[list[str, ...], list[int | float, ...], int]=None,  # drops=(['Stone', 'Coal'], [0.85, 0.15], 1)
            breakable=False, placeable=False
    ) -> None:

        super().__init__('Object', name, id)
        self.hp = hp
        self.recipe = recipe
        self.width = width
        self.height = height
        self.render_when = render_when
        self.drops = drops
        self.breakable = breakable
        self.placeable = placeable

        if self.drops is None:
            self.drops = ([self.name], [1], 1)

class WorldItem(Item):
    def __init__(self, 
            name: str, id: int,
            width: int=block_size, height: int=block_size,
            collision_box: list=None,
            render_when: int | float=None
    ) -> None:
        
        super().__init__('World', name, id)
        self.width = width
        self.height = height
        self.render_when = render_when
        self.collision_box = collision_box


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
    ) -> None:

        super().__init__('Consumable', name, id)
        self.satisfaction_gain = satisfaction_gain
        self.hunger_resistance = hunger_resistance
        self.healing_amount = healing_amount
        self.timer = timer
        self.thirst_resistance = thirst_resistance

items_list = [
    # - # - # - # - # - # - # World # - # - # - # - # - # - #

    # maze

    WorldItem(
        name='Maze_Ground',
        id=98,
    ),

    WorldItem(
        name='Maze_Wall',
        id=99,
        collision_box=[0, 0, 1, 1]
    ),

    WorldItem(
        name='Maze_Ground_Keyhole',
        id=11,
        collision_box=[0, 0, 1, 1]
    ),

    WorldItem(
        name='Keyholder_With_Key',
        id=982,
        collision_box=[0, 0, 1, 1]
    ),

    WorldItem(
        name='Keyholder_Without_Key',
        id=981,
        collision_box=[0, 0, 1, 1]

    ),
    
    WorldItem(
        name='Status_Gray',
        id=500,
    ),

    WorldItem(
        name='Status_Yellow',
        id=550,
    ),

    WorldItem(
        name='Status_Green',
        id=555,
    ),

    WorldItem(
        name='Final_Maze_Ground',
        id=988,
    ),

    WorldItem(
        name='Final_Maze_Ground_2',
        id=9882,
    ),

    WorldItem(
        name='Void',
        id=999,
    ),

    WorldItem(
        name='Endgate',
        id=1000,
    ),

    # blade maze

    WorldItem(
        name='Maze_Blade',
        id=9099,
    ),

    WorldItem(
        name='Maze_Blade',
        id=989,
    ),

    WorldItem(
        name='Maze_Blade',
        id=900,
    ),

    WorldItem(
        name='Maze_Ground',
        id=9099_98,
    ),

    WorldItem(
        name='Maze_Ground',
        id=989_98,
    ),
    
    # doors

    WorldItem(
        name='Maze_Start_Top',
        id=91,
    ),

    WorldItem(
        name='Maze_Start_Right',
        id=92,
    ),

    WorldItem(
        name='Maze_Start_Left',
        id=90,
    ),

    WorldItem(
        name='Maze_Start_Bottom',
        id=93,
    ),

    WorldItem(
        name='Maze_Start_Bottom',
        id=933,
    ),

    WorldItem(
        name='Maze_End_Bottom',
        id=97,
    ),

    WorldItem(
        name='Maze_End_Bottom',
        id=977,
    ),

    WorldItem(
        name='Maze_End_Top',
        id=95,
    ),

    WorldItem(
        name='Maze_End_Right',
        id=96,
    ),

    WorldItem(
        name='Maze_End_Left',
        id=94,
    ),

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

        width=int(block_size * 2),
        height=int(block_size * 2),
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
        name="Wheat_Sapling",
        id=69,
        hp=1,

        render_when=block_size * 0.2,

        breakable=False

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
        name="Opened_Loot_Barrel",
        id=1002,
        hp=1,
        
        width=int(block_size * 0.45),
        height=int(block_size * 0.45),
        render_when=(block_size * 0.2),
    ),

    ObjectItem(
        name="Loot_Barrel",
        id=1001,
        hp=1,

        width=int(block_size * 0.45),
        height=int(block_size * 0.45),
    ),

    # - # - # - # - # - # - # Minerals # - # - # - # - # - # - #

    # need id 12,13 on juba objectitemi all olemas? id peab olema teine muidu tekib error

    # MineralItem(
    #     name="Maze_Key_1",
    #     id=12,
    # ),

    # MineralItem(
    #     name="Maze_Key_2",
    #     id=13,
    # ),

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
        ],
        cookable="Bread"
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

# List'id item type kohta
world_items = [item for item in items_list if isinstance(item, WorldItem)]
object_items = [item for item in items_list if isinstance(item, ObjectItem)]
tool_items = [item for item in items_list if isinstance(item, ToolItem)]
mineral_items = [item for item in items_list if isinstance(item, MineralItem)]
consumable_item = [item for item in items_list if isinstance(item, ConsumableItem)]


# for obj_item in object_items:
#     print(vars(obj_item))

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
