from images import item_images

object_nr_list: list = [2, 4, 5, 6]  # object_id list


# Item name, max hp, min hp, ITEM ID, breakable/pickable
minerals = {"Tree":     (5, 0, 4, True),
            "Stone":    (0, 0, 2, True),
            "Flower":   (0, 0, 5, True),
            "Mushroom": (0, 0, 6, True),
            "Pickaxe":  (0, 0, 10, False),

            }

# Max hp, Min hp, Value, Image
# b - blocks
# m - minerals
# i - items
# c - consumables

# items = {"Tree":    (5, 0, "b_0001", item_images.get("Tree")),
#              "Stone":   (0, 0, "m_0001", item_images.get("Stone")),
#              "Pickaxe": (0, 0, "i_0001", item_images.get("Pickaxe")),
#              "Axe":     (0, 0, "i_0002", item_images.get("Axe")),
#              "Apple":   (0, 0, "c_0001", item_images.get("Apple")),
#              }