from update import EssentialsUpdate

def find_number_in_list_of_lists(list_of_lists, number):
    for row_index, sublist in enumerate(list_of_lists):
        for col_index, element in enumerate(sublist):
            if element == number:
                return row_index, col_index  # Number found, return its coordinates
    return None  # Number not found, return None

def count_occurrences_in_list_of_lists(list_of_lists, number):
    count = 0
    for sublist in list_of_lists:
        for element in sublist:
            if element == number:
                count += 1
    return count


def change_blade():
    if EssentialsUpdate.day_night_text == 'Night':  # uksed on vertikaalselt suletud.
        count_occurrences_in_list_of_lists
        

    elif EssentialsUpdate.day_night_text == 'Day':  # uksed on horisontaalselt
        count_occurrences_in_list_of_lists
    
    else:
        pass