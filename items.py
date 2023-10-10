from images import item_images

block_size = 100

# hitbox: [offset_x, offset_y, width, height]
items_list = [
    {
        "Type": "Object",
        "Name": "Tree",
        "ID": 4,
        "HP": 5,
        "Breakable": True,
        "Collision_box": [0.85, 0.85, 0.35, 0.7],
        "Object_width": int(block_size * 2),
        "Object_height": int(block_size * 2)
    },
    {
        "Type": "Object",
        "Name": "Rock",
        "ID": 2,
        "HP": 5,
        "Breakable": True,
        "Collision_box": [0.3, 0.25, 0.5, 0.4],
        "Object_width": int(block_size * 1),
        "Object_height": int(block_size * 0.8)
    },
    {
        "Type": "Object",
        "Name": "Flower",
        "ID": 5,
        "Breakable": True,
        "Object_width": int(block_size * 0.5),
        "Object_height": int(block_size * 0.5)    },
    {
        "Type": "Object",
        "Name": "Mushroom",
        "ID": 6,
        "Breakable": True,
        "Object_width": int(block_size * 0.3),
        "Object_height": int(block_size * 0.3)    },
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
