import pygame
import time  # Import time module for cooldown functionality
from images import ImageLoader
from variables import UniversalVariables
from camera import Camera
from items import items_list
from inventory import Inventory


class Cooking:
    menu_visible = False

    menu_position = (75, 75)
    raw_item_slot_pos = (menu_position[0] + 52, menu_position[1] + 67)
    cooked_item_slot_pos = (menu_position[0] + 257, menu_position[1] + 67)
    station_coordinates = None  # Hoiustab station'i kordinaadid, et jälgida kaugel player on station'ist

    ### TODO: Ratio peaks kõigele mõjuma pildi suurus, itemi asukoht,
    #    numbri suurus jne... praegu lic ainult cooking menu pilt.

    cooking_menu_ratio = 5

    stations = {}
    station_key: str = None
    cooking_delay = 0

    last_click_time = 0
    click_delay = 0.1
    mouse_button_down = False

    cooking_list:list = []

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

    @staticmethod
    def find_cookable_item(raw_item_name: str):
        return Cooking.cooking_list.get(raw_item_name)

    @staticmethod
    def cooking_in_progress() -> None:
        if not Cooking.cooking_list:
            # Populate the cooking list as a dictionary
            if not Cooking.cooking_list:
                Cooking.cooking_list = {item.get("Name"): item.get("Cookable") for item in items_list if item.get("Cookable")}

        for station_key, station_data in Cooking.stations.items():
            raw_item, raw_item_quantity = station_data['station_raw_item']
            cooked_item, cooked_item_quantity = station_data['station_cooked_item']
            station_cooking_delay = station_data.get("station_cooking_delay", 0)

            # Kui raw item'it pole
            if not raw_item:
                continue

            # Kui raw item'it pole list'is
            if raw_item not in Cooking.cooking_list:
                continue

            # Vaatab kas ruumi on station'is
            if cooked_item_quantity >= UniversalVariables.station_capacity:
                continue

            # Cook'ib stabiilselt | ühtlaste vahedega, liiga kiirelt ei cook'iks
            if station_cooking_delay >= UniversalVariables.cooking_delay:
                cooked_item_name = Cooking.find_cookable_item(raw_item)

                # Update quantities and reset delay
                raw_item_quantity -= 1
                cooked_item_quantity += 1
                station_cooking_delay = 0

                # Update station data with the cooked item
                station_data["station_raw_item"] = (raw_item, raw_item_quantity)
                station_data["station_cooked_item"] = (cooked_item_name, cooked_item_quantity)

                # Remove raw item if its quantity is zero
                if raw_item_quantity <= 0:
                    station_data["station_raw_item"] = (None, 0)

            # Increment cooking delay if there's a raw item
            station_data["station_cooking_delay"] = station_cooking_delay + 1 if raw_item_quantity > 0 else 0

    def handle_item_interaction(self, mouse_x: int, mouse_y: int, mouse_buttons: tuple[int, int, int]) -> None:
        """
        Käsitleb itemite paigutamist küpsetamisjaama sisse ja väljavõtmist.

        Argumendid:
            mouse_x (int): Hiire x-koordinaat.
            mouse_y (int): Hiire y-koordinaat.
            mouse_buttons (tuple[int, int, int]): Hiire nuppude olekud.
        """

        current_time = time.time()

        inventory = Inventory.inventory
        selected_station_key = None

        # Võtab õige station key, et muudaks ainult ühe stationit
        for station_key, station_data in Cooking.stations.items():
            if station_key == Cooking.station_key:
                raw_item, raw_item_quantity = station_data['station_raw_item']
                cooked_item, cooked_item_quantity = station_data['station_cooked_item']
                station_cooking_delay = station_data.get("station_cooking_delay", 0)
                selected_station_key = station_key

        # Vaatab raw item slot'ti
        if Cooking.raw_item_slot_pos[0] <= mouse_x <= Cooking.raw_item_slot_pos[0] + 41 and Cooking.raw_item_slot_pos[1] <= mouse_y <= Cooking.raw_item_slot_pos[1] + 41:

            if mouse_buttons[0] and raw_item_quantity < UniversalVariables.station_capacity:  # Left click
                Cooking.mouse_button_down = True
                if current_time - Cooking.last_click_time > Cooking.click_delay:
                    Cooking.last_click_time = current_time

                    # Check if there's a current equipped item
                    current_equipped_item = UniversalVariables.current_equipped_item
                    if current_equipped_item is not None:

                        # Prevent adding a different item
                        if raw_item is not None and raw_item != current_equipped_item:
                            return  # Do nothing if trying to add a different item

                        raw_item = current_equipped_item

                        # Jälgib shift'i vajutamist
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:

                            # Kui shift'i all hoida sisestab max koguse mis hetkel võimalik, kas kõik mis on või max station capacity
                            quantity = min(inventory.get(raw_item, 0), UniversalVariables.station_capacity - raw_item_quantity)
                        else:
                            # Ilma shift'ita on koguseks 1
                            quantity = 1

                        if raw_item in inventory and inventory[raw_item] >= quantity:
                            if raw_item is None:
                                raw_item_quantity = quantity

                                # Muudab station list'is station'i raw item state'i
                                Cooking.stations[selected_station_key]["station_raw_item"] = raw_item, raw_item_quantity

                            else:
                                raw_item_quantity = min(raw_item_quantity + quantity, UniversalVariables.station_capacity)
                                Cooking.stations[selected_station_key]["station_raw_item"] = raw_item, raw_item_quantity

                            inventory[raw_item] -= quantity
                            if inventory[raw_item] <= 0:
                                del inventory[raw_item]


            elif mouse_buttons[2]:  # Right click
                Cooking.mouse_button_down = True
                if current_time - Cooking.last_click_time > Cooking.click_delay:
                    Cooking.last_click_time = current_time

                    if raw_item is not None:

                        # Kui shift'i all hoida eemaldab max koguse mis võimalik, kas kõik mis on või max station capacity
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                            quantity = raw_item_quantity  # Eemaldab kõik kui shift'i all hoida
                            raw_item_quantity = 0

                            # Muudab station list'is station'i raw item state'i
                            Cooking.stations[selected_station_key]["station_raw_item"] = (None, 0)

                        else:
                            # Ilma shift'ita ainult 1
                            quantity = 1
                            raw_item_quantity -= 1
                            Cooking.stations[selected_station_key]["station_raw_item"] = raw_item, raw_item_quantity

                        if raw_item in inventory:
                            inventory[raw_item] += quantity
                        else:
                            inventory[raw_item] = quantity

                        if raw_item_quantity <= 0:
                            raw_item = None
                            raw_item_quantity = 0

                            Cooking.stations[selected_station_key]["station_raw_item"] = (None, 0)
                            station_data["station_cooking_delay"] = 0



        # Vaatab cooked item slot'ti
        elif Cooking.cooked_item_slot_pos[0] <= mouse_x <= Cooking.cooked_item_slot_pos[0] + 41 and \
                Cooking.cooked_item_slot_pos[1] <= mouse_y <= Cooking.cooked_item_slot_pos[1] + 41:
            if mouse_buttons[2]:  # Right click
                Cooking.mouse_button_down = True
                if current_time - Cooking.last_click_time > Cooking.click_delay:
                    Cooking.last_click_time = current_time

                    if cooked_item is not None:  # Vaatab kas on item'it mida võtta
                        item = cooked_item

                        # Kui shift'i all hoida eemaldab max koguse mis võimalik, kas kõik mis on või max station capacity
                        quantity = 1 if not pygame.key.get_mods() & pygame.KMOD_SHIFT else cooked_item_quantity


                        # Paneb item'i invi
                        if item in inventory:
                            inventory[item] += quantity
                        else:
                            inventory[item] = quantity

                        # Eemaldab item'i cooked item slot'ist
                        if cooked_item_quantity > quantity:
                            cooked_item_quantity -= quantity
                        else:
                            cooked_item = None
                            cooked_item_quantity = 0
                            Cooking.stations[selected_station_key]["station_cooked_item"] = (None, 0)

                        Cooking.stations[selected_station_key]["station_cooked_item"] = cooked_item, cooked_item_quantity

        if not any(mouse_buttons):
            Cooking.mouse_button_down = False


    def display_menu(self) -> None:
        """
        Toggle'ib cooking menu sõltuvalt right click'ist ja player'i kaugusest cooking station'ist.

        Returns:
            None
        """


        mouse_buttons = pygame.mouse.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if mouse_buttons[2]:  # Right click
            click_x, click_y = Camera.right_click_x, Camera.right_click_y
            if click_x is not None and click_y is not None:
                click_x //= UniversalVariables.block_size
                click_y //= UniversalVariables.block_size

                # Kui on click'itud cooking station'i peale
                if self.terrain_data[click_y][click_x] in UniversalVariables.cooking_stations:
                    Cooking.station_key = f"station_{click_y}_{click_x}"

                    station = Cooking.stations.setdefault(Cooking.station_key, {
                        "station_coordinates": (click_y, click_x),
                        "station_raw_item": (None, 0),
                        "station_cooked_item": (None, 0),
                        "station_cooking_delay": 0
                    })

                    # Kui vajutad uuesti cooking station'i peale kui cooking menu on lahti siis sulgeb cooking menu
                    if UniversalVariables.cooking_menu:
                        UniversalVariables.cooking_menu = False
                    else:
                        # Kui vajutad cooking station'i peale siis avab cooking menu ja salvestab selle kordinaadid
                        Cooking.station_coordinates = (click_x, click_y)
                        UniversalVariables.cooking_menu = True

                    # Kui cooking menu ei ole nähtav või player ei ole cooking_range'is siis suletakse inventory
                    if not UniversalVariables.cooking_menu or not Cooking.player_in_range(click_x, click_y):
                        Inventory.inv_count = 0
                        Inventory.render_inv = False
                        UniversalVariables.is_cooking = False

            Camera.right_click_x, Camera.right_click_y = None, None

        # Renderib'b cooking menu kui UniversalVariables.cooking_menu on True ja player on läheduses
        if UniversalVariables.cooking_menu == True and Cooking.station_coordinates:
            station_x, station_y = Cooking.station_coordinates

            # Kontrollib, et cooking station oleks endiselt olemas, kui ei ole siis ei render'i cooking menu'd
            if not self.terrain_data[station_y][station_x] in UniversalVariables.cooking_stations:
                Inventory.inv_count = 0
                Inventory.render_inv = False
                UniversalVariables.is_cooking = False

                raw_item, cooked_item = None, None
                raw_item_quantity, cooked_item_quantity = 0, 0

                UniversalVariables.cooking_menu = False

            elif Cooking.player_in_range(station_x, station_y):
                Inventory.inv_count = 1
                Inventory.render_inv = True
                UniversalVariables.is_cooking = True

                # Load'ib ja resize'ib pildid
                cooking_menu = ImageLoader.load_image("Cooking_Menu", image_path='images/Hud/Cooking_Menu.png')
                width, height = cooking_menu.get_width() * Cooking.cooking_menu_ratio, cooking_menu.get_height() * Cooking.cooking_menu_ratio
                resized_cooking_menu = pygame.transform.scale(cooking_menu, (width, height))


                for station_key, station_data in Cooking.stations.items():
                    if station_key == Cooking.station_key:
                        raw_item, raw_item_quantity = station_data['station_raw_item']
                        cooked_item, cooked_item_quantity = station_data['station_cooked_item']
                        station_cooking_delay = station_data.get("station_cooking_delay", 0)

                # Progress bar'i jaoks
                cookable_item = False
                for item in items_list:
                    if item.get("Name") == raw_item and "Cookable" in item:
                        cookable_item = True
                        break

                if raw_item:
                    raw_item = ImageLoader.load_image(raw_item)
                    resized_raw_item = pygame.transform.scale(raw_item, (41, 41))

                if cooked_item:
                    cooked_item = ImageLoader.load_image(cooked_item)
                    resized_cooked_item = pygame.transform.scale(cooked_item, (41, 41))


                if not raw_item and not cooked_item:
                    self.screen.blits([
                        (resized_cooking_menu, Cooking.menu_position)
                    ])

                if raw_item and not cooked_item:
                    self.screen.blits([
                        (resized_cooking_menu, Cooking.menu_position),
                        (resized_raw_item, Cooking.raw_item_slot_pos)

                    ])

                if not raw_item and cooked_item:
                    self.screen.blits([
                        (resized_cooking_menu, Cooking.menu_position),
                        (resized_cooked_item, Cooking.cooked_item_slot_pos)
                    ])

                if raw_item and cooked_item:
                    self.screen.blits([
                        (resized_cooking_menu, Cooking.menu_position),
                        (resized_raw_item, Cooking.raw_item_slot_pos),
                        (resized_cooked_item, Cooking.cooked_item_slot_pos)
                    ])

                # Render'ib item'i koguse kui seda on rohkem kui 1
                if raw_item is not None:
                    font = pygame.font.Font(None, 25)
                    quantity_text = f"{raw_item_quantity}" if raw_item_quantity > 1 else ""
                    quantity_surface = font.render(quantity_text, True, (255, 255, 255))
                    self.screen.blit(quantity_surface, Cooking.raw_item_slot_pos)

                if cooked_item is not None:
                    font = pygame.font.Font(None, 25)
                    quantity_text = f"{cooked_item_quantity}" if cooked_item_quantity > 1 else ""
                    quantity_surface = font.render(quantity_text, True, (255, 255, 255))
                    self.screen.blit(quantity_surface, Cooking.cooked_item_slot_pos)

                # Draw the progress bar
                progress_bar_width = 20 * Cooking.cooking_menu_ratio
                progress_bar_height = 5 * Cooking.cooking_menu_ratio
                progress_bar_x = Cooking.menu_position[0] + 25 * Cooking.cooking_menu_ratio
                progress_bar_y = Cooking.menu_position[1] + 15 * Cooking.cooking_menu_ratio
                progress = min(station_cooking_delay / UniversalVariables.cooking_delay, 1.0)


                if raw_item and cookable_item:
                    progress_surface = pygame.Surface((progress_bar_width, progress_bar_height), pygame.SRCALPHA)

                    pygame.draw.rect(progress_surface, (60, 250, 72, 125),
                                     (0, 0, progress * progress_bar_width, progress_bar_height))
                    self.screen.blit(progress_surface, (progress_bar_x, progress_bar_y))

                # Läheb siia ainult siis kui mingit nuppu on vajutatud
                if True in mouse_buttons:
                    # Käsitleb item'ite panemist ja võtmist cooking station'ist
                    Cooking.handle_item_interaction(self, mouse_x, mouse_y, mouse_buttons)

            else:
                UniversalVariables.cooking_menu = False
                Inventory.inv_count = 0
                Inventory.render_inv = False
                UniversalVariables.is_cooking = False

    def update(self):
        Cooking.display_menu(self)

        Cooking.cooking_in_progress()

        if Cooking.stations.get(Cooking.station_key, {}).get('station_raw_item', (None, 0))[1] > 0:
            Cooking.cooking_delay += 1
        else:
            Cooking.cooking_delay = 0


        if not UniversalVariables.cooking_menu:
            Cooking.stations = {
                key: station for key, station in Cooking.stations.items()
                if station['station_raw_item'][1] > 0 or station['station_cooked_item'][1] > 0
            }


