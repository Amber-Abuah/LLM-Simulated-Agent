from gui.gui_ascii_art import *

# Draws the cat's current ascii expression to a grid, centred.
def build_grid(cat_expression):

    # Calculate the maximum height and width for display area
    max_columns = max([len(a.split("\n")) for a in all_expressions]) + 2
    max_rows = max([len(line) for a in all_expressions for line in a.split("\n")]) + 2

    if cat_expression == "eat":
        cat_ascii = cat_eat
    elif cat_expression == "play":
        cat_ascii = cat_play
    elif cat_expression == "sleep":
        cat_ascii = cat_sleep
    else:
        cat_ascii = cat_sit

    cat_ascii_array = [list(c) for c in cat_ascii.split("\n")]

    column_padding = (max_columns - len(cat_ascii_array))//2
    row_padding = (max_rows - max(len(c) for c in cat_ascii_array))//2

    # Draw ascii to output grid
    output = [[" " for _ in range(max_rows)] for _ in range(max_columns)]

    for column_index in range(min(len(cat_ascii_array), max_columns- column_padding)):
        for row_index in range(min(len(cat_ascii_array[column_index]), max_rows - row_padding)):
            if cat_ascii_array[column_index][row_index] != " ":
                output[column_padding + column_index][row_index + row_padding] = cat_ascii_array[column_index][row_index]

    return "\n".join(["".join(c) for c in output])