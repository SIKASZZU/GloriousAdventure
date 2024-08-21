import pygame
import time  # Import time module for cooldown functionality
from images import ImageLoader
from variables import UniversalVariables
from camera import Camera

from inventory import Inventory


class Cooking:
    menu_visible = False
    menu_position = (75, 75)
    station_coordinates = None  # Hoiustab station'i kordinaadid, et jälgida kaugel player on station'ist

    raw_item: str = None
    cooked_item: str = None

    raw_item_slot_pos = (menu_position[0] + 52, menu_position[1] + 67)
    cooked_item_slot_pos = (menu_position[0] + 257, menu_position[1] + 67)

    raw_item_quantity: int = 0  # Raw item'i kogus cooking station'is
    cooked_item_quantity: int = 0  # Cooked item'i kogus cooking station'is

    stations = {}

    cooking_delay = 0
    station_key: str

    @staticmethod
    def player_in_range(station_x: int, station_y: int) -> bool:
        """
        Kontrollib, kas mängija on cooking station'i läheduses.

        Args:
            station_x (int): cooking station'i x-koordinaat (grid-kordinaat).
            station_y (int): cooking station'i y-koordinaat (grid-kordinaat).

        Returns:
            bool: True, kui mängija on cooking_range'is, muidu False.
        """

        player_x: int = UniversalVariables.player_x // UniversalVariables.block_size
        player_y: int = UniversalVariables.player_y // UniversalVariables.block_size
        return (
                abs(station_x - player_x) <= UniversalVariables.cooking_range and
                abs(station_y - player_y) <= UniversalVariables.cooking_range
        )

    def cooking_in_progress(self) -> None:
        ### TODO: if Cooking.raw_item == is_cookable:

        if Cooking.cooking_delay >= 20 and Cooking.cooked_item_quantity < UniversalVariables.station_capacity:
            if Cooking.cooked_item:
                if Cooking.cooked_item == Cooking.raw_item:
                    Cooking.raw_item_quantity -= 1
                    Cooking.cooked_item_quantity += 1
                    Cooking.cooking_delay = 0

            elif Cooking.cooked_item == None:
                Cooking.cooked_item = Cooking.raw_item
                Cooking.raw_item_quantity -= 1
                Cooking.cooked_item_quantity += 1
                Cooking.cooking_delay = 0

            Cooking.stations[Cooking.station_key]["station_raw_item"] = Cooking.raw_item, Cooking.raw_item_quantity
            Cooking.stations[Cooking.station_key]["station_cooked_item"] = Cooking.cooked_item, Cooking.cooked_item_quantity

            if Cooking.raw_item_quantity <= 0:
                Cooking.raw_item = None
                Cooking.stations[Cooking.station_key]["station_raw_item"] = (None, 0)

    def handle_item_interaction(self, mouse_x: int, mouse_y: int, mouse_buttons: tuple[int, int, int]) -> None:
        """
        Käsitleb itemite paigutamist küpsetamisjaama sisse ja väljavõtmist.

        Argumendid:
            mouse_x (int): Hiire x-koordinaat.
            mouse_y (int): Hiire y-koordinaat.
            mouse_buttons (tuple[int, int, int]): Hiire nuppude olekud.
        """

        inventory = Inventory.inventory

        # Vaatab raw item slot'ti
        if Cooking.raw_item_slot_pos[0] <= mouse_x <= Cooking.raw_item_slot_pos[0] + 41 and Cooking.raw_item_slot_pos[1] <= mouse_y <= Cooking.raw_item_slot_pos[1] + 41:

            if mouse_buttons[0] and Cooking.raw_item_quantity < UniversalVariables.station_capacity:  # Left click
                Cooking.raw_item = UniversalVariables.current_equipped_item
                if UniversalVariables.current_equipped_item is not None:

                    # Jälgib shift'i vajutamist
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:

                        # Kui shift'i all hoida sisestab max koguse mis hetkel võimalik, kas kõik mis on või max station capacity
                        quantity = min(inventory.get(Cooking.raw_item, 0), UniversalVariables.station_capacity - Cooking.raw_item_quantity)
                    else:
                        # Ilma shift'ita on koguseks 1
                        quantity = 1

                    if Cooking.raw_item in inventory and inventory[Cooking.raw_item] >= quantity:
                        if Cooking.raw_item is None:
                            Cooking.raw_item_quantity = quantity

                            # Muudab station list'is station'i raw item state'i
                            Cooking.stations[Cooking.station_key][
                                "station_raw_item"] = Cooking.raw_item, Cooking.raw_item_quantity

                        else:
                            Cooking.raw_item_quantity = min(Cooking.raw_item_quantity + quantity, UniversalVariables.station_capacity)
                            Cooking.stations[Cooking.station_key]["station_raw_item"] = Cooking.raw_item, Cooking.raw_item_quantity

                        inventory[Cooking.raw_item] -= quantity
                        if inventory[Cooking.raw_item] <= 0:
                            del inventory[Cooking.raw_item]


            elif mouse_buttons[2]:  # Right click
                if Cooking.raw_item is not None:

                    # Kui shift'i all hoida eemaldab max koguse mis võimalik, kas kõik mis on või max station capacity
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        quantity = Cooking.raw_item_quantity  # Eemaldab kõik kui shift'i all hoida
                        Cooking.raw_item_quantity = 0

                        # Muudab station list'is station'i raw item state'i
                        Cooking.stations[Cooking.station_key]["station_raw_item"] = (None, 0)

                    else:

                        # Ilma shift'ita ainult 1
                        quantity = 1
                        Cooking.raw_item_quantity -= 1
                        Cooking.stations[Cooking.station_key]["station_raw_item"] = Cooking.raw_item, Cooking.raw_item_quantity

                    if Cooking.raw_item in inventory:
                        inventory[Cooking.raw_item] += quantity
                    else:
                        inventory[Cooking.raw_item] = quantity

                    if Cooking.raw_item_quantity <= 0:
                        Cooking.raw_item = None
                        Cooking.raw_item_quantity = 0

                        Cooking.stations[Cooking.station_key]["station_raw_item"] = (None, 0)

        # Vaatab cooked item slot'ti
        if Cooking.cooked_item_slot_pos[0] <= mouse_x <= Cooking.cooked_item_slot_pos[0] + 41 and \
                Cooking.cooked_item_slot_pos[1] <= mouse_y <= Cooking.cooked_item_slot_pos[1] + 41:
            if mouse_buttons[2]:  # Right click

                if Cooking.cooked_item is not None:  # Vaatab kas on item'it mida võtta
                    item = Cooking.cooked_item

                    # Kui shift'i all hoida eemaldab max koguse mis võimalik, kas kõik mis on või max station capacity
                    quantity = 1 if not pygame.key.get_mods() & pygame.KMOD_SHIFT else Cooking.cooked_item_quantity


                    # Paneb item'i invi
                    if item in inventory:
                        inventory[item] += quantity
                    else:
                        inventory[item] = quantity

                    # Eemaldab item'i cooked item slot'ist
                    if Cooking.cooked_item_quantity > quantity:
                        Cooking.cooked_item_quantity -= quantity
                    else:
                        Cooking.cooked_item = None
                        Cooking.cooked_item_quantity = 0
                        Cooking.stations[Cooking.station_key]["station_raw_item"] = (None, 0)

                    Cooking.stations[Cooking.station_key]["station_cooked_item"] = Cooking.cooked_item, Cooking.cooked_item_quantity

    def display_menu(self) -> None:
        """
        Toggle'ib cooking menu sõltuvalt right click'ist ja player'i kaugusest cooking station'ist.

        Returns:
            None
        """

        mouse_buttons = pygame.mouse.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if mouse_buttons[2]:  # Right click
            if Camera.right_click_x and Camera.right_click_y:
                click_x: int = Camera.right_click_x // UniversalVariables.block_size
                click_y: int = Camera.right_click_y // UniversalVariables.block_size

                # Kui on click'itud cooking station'i peale
                if self.terrain_data[click_y][click_x] in UniversalVariables.cooking_stations:
                    Cooking.station_key = f"station_{click_y}_{click_x}"

                    Cooking.stations[Cooking.station_key] = {
                        "station_coordinates": (click_y, click_x),
                        "station_raw_item": (None, 0),
                        "station_cooked_item": (None, 0)
                    }

                    # Kui vajutad uuesti cooking station'i peale kui cooking menu on lahti siis sulgeb cooking menu
                    if Cooking.menu_visible:
                        Cooking.menu_visible = False
                    else:
                        # Kui vajutad cooking station'i peale siis avab cooking menu ja salvestab selle kordinaadid
                        Cooking.station_coordinates = (click_x, click_y)
                        Cooking.menu_visible = True

                    # Kui cooking menu ei ole nähtav või player ei ole cooking_range'is siis suletakse inventory
                    if not Cooking.menu_visible or not Cooking.player_in_range(click_x, click_y):
                        Inventory.inv_count = 0
                        Inventory.render_inv = False
                        UniversalVariables.is_cooking = False

            Camera.right_click_x, Camera.right_click_y = None, None

        # Renderib'b cooking menu kui Cooking.menu_visible on True ja player on läheduses
        if Cooking.menu_visible == True and Cooking.station_coordinates:
            station_x, station_y = Cooking.station_coordinates

            # Kontrollib, et cooking station oleks endiselt olemas, kui ei ole siis ei render'i cooking menu'd
            if not self.terrain_data[station_y][station_x] in UniversalVariables.cooking_stations:
                UniversalVariables.is_cooking = False
                Inventory.render_inv = False
                Inventory.inv_count = 0

                Cooking.menu_visible = False

            elif Cooking.player_in_range(station_x, station_y):
                Inventory.inv_count = 1
                Inventory.render_inv = True
                UniversalVariables.is_cooking = True

                # Load'ib ja resize'ib pildid
                cooking_menu = ImageLoader.load_image("Cooking_Menu", image_path='images/Hud/Cooking_Menu.png')
                width, height = cooking_menu.get_width() * 5, cooking_menu.get_height() * 5
                resized_cooking_menu = pygame.transform.scale(cooking_menu, (width, height))

                if Cooking.raw_item:
                    raw_item = ImageLoader.load_image(Cooking.raw_item)
                    resized_raw_item = pygame.transform.scale(raw_item, (41, 41))

                if Cooking.cooked_item:
                    cooked_item = ImageLoader.load_image(Cooking.cooked_item)
                    resized_cooked_item = pygame.transform.scale(cooked_item, (41, 41))

                if not Cooking.raw_item and not Cooking.cooked_item:
                    self.screen.blits([
                        (resized_cooking_menu, Cooking.menu_position)
                    ])

                elif Cooking.raw_item and not Cooking.cooked_item:
                    self.screen.blits([
                        (resized_cooking_menu, Cooking.menu_position),
                        (resized_raw_item, Cooking.raw_item_slot_pos)

                    ])

                elif not Cooking.raw_item and Cooking.cooked_item:
                    self.screen.blits([
                        (resized_cooking_menu, Cooking.menu_position),
                        (resized_cooked_item, Cooking.cooked_item_slot_pos)
                    ])

                elif Cooking.raw_item and Cooking.cooked_item:
                    self.screen.blits([
                        (resized_cooking_menu, Cooking.menu_position),
                        (resized_raw_item, Cooking.raw_item_slot_pos),
                        (resized_cooked_item, Cooking.cooked_item_slot_pos)
                    ])

                # Render'ib item'i koguse kui seda on rohkem kui 1
                if Cooking.raw_item is not None:
                    font = pygame.font.Font(None, 25)
                    quantity_text = f"{Cooking.raw_item_quantity}" if Cooking.raw_item_quantity > 1 else ""
                    quantity_surface = font.render(quantity_text, True, (255, 255, 255))
                    self.screen.blit(quantity_surface, Cooking.raw_item_slot_pos)

                if Cooking.cooked_item is not None:
                    font = pygame.font.Font(None, 25)
                    quantity_text = f"{Cooking.cooked_item_quantity}" if Cooking.cooked_item_quantity > 1 else ""
                    quantity_surface = font.render(quantity_text, True, (255, 255, 255))
                    self.screen.blit(quantity_surface, Cooking.cooked_item_slot_pos)

                # Käsitleb item'ite panemist ja võtmist cooking station'ist
                Cooking.handle_item_interaction(self, mouse_x, mouse_y, mouse_buttons)

            else:
                Cooking.menu_visible = False
                Inventory.inv_count = 0
                Inventory.render_inv = False
                UniversalVariables.is_cooking = False

    def update(self):
        Cooking.display_menu(self)

        Cooking.cooking_in_progress(self)

        if Cooking.raw_item_quantity > 0:
            Cooking.cooking_delay += 1
        else:
            Cooking.cooking_delay = 0

        ### TODO: Kui item'eid station'is pole ss võtab selle station list'ist ära
        # stations_to_remove = []
        #
        # for station in Cooking.stations:
        #     if (Cooking.stations[station]["station_raw_item"][0] is None and
        #             Cooking.stations[station]["station_cooked_item"][0] is None):
        #         stations_to_remove.append(station)
        #
        # for station in stations_to_remove:
        #     del Cooking.stations[station]

        print(Cooking.stations)
