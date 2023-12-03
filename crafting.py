from items import items_list


def craft_item(item_name, inventory, shift_pressed=False):
    # Otsime eseme retsepti item_list'ist
    for item in items_list:
        if item["Name"] == item_name and "Recipe" in item:
            recipe = item["Recipe"]
            can_craft = True
            # Kontrollime, kas craftimiseks on piisavalt ressursse
            for required_item, required_amount in recipe.items():
                if required_item not in inventory or inventory[required_item] < required_amount:
                    can_craft = False
                    break
            if can_craft:
                # Shift = max, else: 1
                craftable_times = 1 if not shift_pressed else min(
                    inventory[required_item] // required_amount for required_item, required_amount in recipe.items())
                if craftable_times <= 0:  # Et vähemalt ühe korra craftiks
                    craftable_times = 1

                # Craftimiseks vajalikud itemid kaovad invist ja lisandub uus item invi
                for required_item, required_amount in recipe.items():
                    inventory[required_item] -= required_amount * craftable_times
                if item_name in inventory:
                    inventory[item_name] += item.get("Amount", 1) * craftable_times
                else:
                    inventory[item_name] = item.get("Amount", 1) * craftable_times

                if craftable_times == 1:
                    print(f"Crafted {item_name}!")
                else:
                    print(f"Crafted {craftable_times} {item_name}(s)!")
                return craftable_times
            else:
                print(f"Not enough {item_name}.")
                return 0
    print(f"{item_name} recipe not found.")
    return 0


if __name__ == "__main__":  ### TODO: Et see vaataks invi ja võtaks sealt itemeid ära ja lisaks
    # Test inv
    player_inventory = {
        "Oak_Wood": 5222,
        "Stick": 525,
        "Oak_Planks": 5332,
    }

    # Shifti all hoides
    crafted_amount = craft_item("Wood_Pickaxe", player_inventory)

    crafted_amount_shift = craft_item("Wood_Pickaxe", player_inventory, shift_pressed=True)
