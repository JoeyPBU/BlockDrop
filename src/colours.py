class Colours:
    empty_cell = (255, 255, 255)
    I_piece_colour = (51, 204, 255)
    O_piece_colour = (251, 233, 13)
    S_piece_colour = (0, 204, 0)
    Z_piece_colour = (248, 7, 7)
    L_piece_colour = (241, 127, 41)
    J_piece_colour = (51, 51, 153)
    T_piece_colour = (153, 0, 204)
    text_white = (255, 255, 255)
    text_black = (1, 1, 1)
    board_colour = (48, 98, 48)
    board_colour_light = (139, 172, 15)

    @classmethod
    def get_cell_colours(cls):
        return [cls.empty_cell, cls.L_piece_colour, cls.J_piece_colour, cls.I_piece_colour, cls.O_piece_colour, cls.S_piece_colour, cls.Z_piece_colour, cls.T_piece_colour]


#139, 172, 15