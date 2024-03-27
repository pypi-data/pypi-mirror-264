import builtins

from functools import wraps


_named_colors_256 = {
    'black': {'number': 0, 'hex': '#000000', 'rgb': (0, 0, 0), 'hsl': (0, 0, 0)},
    'maroon': {'number': 1, 'hex': '#800000', 'rgb': (128, 0, 0), 'hsl': (0, 100, 25)},
    'green1': {'number': 2, 'hex': '#008000', 'rgb': (0, 128, 0), 'hsl': (120, 100, 25)},
    'olive': {'number': 3, 'hex': '#808000', 'rgb': (128, 128, 0), 'hsl': (60, 100, 25)},
    'navy': {'number': 4, 'hex': '#000080', 'rgb': (0, 0, 128), 'hsl': (240, 100, 25)},
    'purple': {'number': 5, 'hex': '#800080', 'rgb': (128, 0, 128), 'hsl': (300, 100, 25)},
    'teal': {'number': 6, 'hex': '#008080', 'rgb': (0, 128, 128), 'hsl': (180, 100, 25)},
    'silver': {'number': 7, 'hex': '#c0c0c0', 'rgb': (192, 192, 192), 'hsl': (0, 0, 75)},
    'grey': {'number': 8, 'hex': '#808080', 'rgb': (128, 128, 128), 'hsl': (0, 0, 50)},
    'red': {'number': 9, 'hex': '#ff0000', 'rgb': (255, 0, 0), 'hsl': (0, 100, 50)},
    'lime': {'number': 10, 'hex': '#00ff00', 'rgb': (0, 255, 0), 'hsl': (120, 100, 50)},
    'yellow': {'number': 11, 'hex': '#ffff00', 'rgb': (255, 255, 0), 'hsl': (60, 100, 50)},
    'blue': {'number': 12, 'hex': '#0000ff', 'rgb': (0, 0, 255), 'hsl': (240, 100, 50)},
    'fuchsia': {'number': 13, 'hex': '#ff00ff', 'rgb': (255, 0, 255), 'hsl': (300, 100, 50)},
    'pink': {'number': 13, 'hex': '#ff00ff', 'rgb': (255, 0, 255), 'hsl': (300, 100, 50)},
    'aqua': {'number': 14, 'hex': '#00ffff', 'rgb': (0, 255, 255), 'hsl': (180, 100, 50)},
    'white': {'number': 15, 'hex': '#ffffff', 'rgb': (255, 255, 255), 'hsl': (0, 0, 100)},
    'grey0': {'number': 16, 'hex': '#000000', 'rgb': (0, 0, 0), 'hsl': (0, 0, 0)},
    'navyblue': {'number': 17, 'hex': '#00005f', 'rgb': (0, 0, 95), 'hsl': (240, 100, 18)},
    'darkblue': {'number': 18, 'hex': '#000087', 'rgb': (0, 0, 135), 'hsl': (240, 100, 26)},
    'blue3_': {'number': 19, 'hex': '#0000af', 'rgb': (0, 0, 175), 'hsl': (240, 100, 34)},
    'blue3': {'number': 20, 'hex': '#0000d7', 'rgb': (0, 0, 215), 'hsl': (240, 100, 42)},
    'blue1': {'number': 21, 'hex': '#0000ff', 'rgb': (0, 0, 255), 'hsl': (240, 100, 50)},
    'darkgreen': {'number': 22, 'hex': '#005f00', 'rgb': (0, 95, 0), 'hsl': (120, 100, 18)},
    'deepskyblue4__': {'number': 23, 'hex': '#005f5f', 'rgb': (0, 95, 95), 'hsl': (180, 100, 18)},
    'deepskyblue4_': {'number': 24, 'hex': '#005f87', 'rgb': (0, 95, 135), 'hsl': (97, 100, 26)},
    'deepskyblue4': {'number': 25, 'hex': '#005faf', 'rgb': (0, 95, 175), 'hsl': (7, 100, 34)},
    'dodgerblue3': {'number': 26, 'hex': '#005fd7', 'rgb': (0, 95, 215), 'hsl': (13, 100, 42)},
    'dodgerblue2': {'number': 27, 'hex': '#005fff', 'rgb': (0, 95, 255), 'hsl': (17, 100, 50)},
    'green4': {'number': 28, 'hex': '#008700', 'rgb': (0, 135, 0), 'hsl': (120, 100, 26)},
    'springgreen4': {'number': 29, 'hex': '#00875f', 'rgb': (0, 135, 95), 'hsl': (62, 100, 26)},
    'turquoise4': {'number': 30, 'hex': '#008787', 'rgb': (0, 135, 135), 'hsl': (180, 100, 26)},
    'deepskyblue3_': {'number': 31, 'hex': '#0087af', 'rgb': (0, 135, 175), 'hsl': (93, 100, 34)},
    'deepskyblue3': {'number': 32, 'hex': '#0087d7', 'rgb': (0, 135, 215), 'hsl': (2, 100, 42)},
    'dodgerblue1': {'number': 33, 'hex': '#0087ff', 'rgb': (0, 135, 255), 'hsl': (8, 100, 50)},
    'dodgerblue': {'number': 33, 'hex': '#0087ff', 'rgb': (0, 135, 255), 'hsl': (8, 100, 50)},
    'green3_': {'number': 34, 'hex': '#00af00', 'rgb': (0, 175, 0), 'hsl': (120, 100, 34)},
    'springgreen3_': {'number': 35, 'hex': '#00af5f', 'rgb': (0, 175, 95), 'hsl': (52, 100, 34)},
    'darkcyan': {'number': 36, 'hex': '#00af87', 'rgb': (0, 175, 135), 'hsl': (66, 100, 34)},
    'lightseagreen': {'number': 37, 'hex': '#00afaf', 'rgb': (0, 175, 175), 'hsl': (180, 100, 34)},
    'deepskyblue2': {'number': 38, 'hex': '#00afd7', 'rgb': (0, 175, 215), 'hsl': (91, 100, 42)},
    'deepskyblue1': {'number': 39, 'hex': '#00afff', 'rgb': (0, 175, 255), 'hsl': (98, 100, 50)},
    'deepskyblue': {'number': 39, 'hex': '#00afff', 'rgb': (0, 175, 255), 'hsl': (98, 100, 50)},
    'green3': {'number': 40, 'hex': '#00d700', 'rgb': (0, 215, 0), 'hsl': (120, 100, 42)},
    'springgreen3': {'number': 41, 'hex': '#00d75f', 'rgb': (0, 215, 95), 'hsl': (46, 100, 42)},
    'springgreen2_': {'number': 42, 'hex': '#00d787', 'rgb': (0, 215, 135), 'hsl': (57, 100, 42)},
    'cyan3': {'number': 43, 'hex': '#00d7af', 'rgb': (0, 215, 175), 'hsl': (68, 100, 42)},
    'darkturquoise': {'number': 44, 'hex': '#00d7d7', 'rgb': (0, 215, 215), 'hsl': (180, 100, 42)},
    'turquoise2': {'number': 45, 'hex': '#00d7ff', 'rgb': (0, 215, 255), 'hsl': (89, 100, 50)},
    'turquoise': {'number': 45, 'hex': '#00d7ff', 'rgb': (0, 215, 255), 'hsl': (89, 100, 50)},
    'green': {'number': 46, 'hex': '#00ff00', 'rgb': (0, 255, 0), 'hsl': (120, 100, 50)},
    'springgreen2': {'number': 47, 'hex': '#00ff5f', 'rgb': (0, 255, 95), 'hsl': (42, 100, 50)},
    'springgreen1': {'number': 48, 'hex': '#00ff87', 'rgb': (0, 255, 135), 'hsl': (51, 100, 50)},
    'springgreen': {'number': 48, 'hex': '#00ff87', 'rgb': (0, 255, 135), 'hsl': (51, 100, 50)},
    'mediumspringgreen': {'number': 49, 'hex': '#00ffaf', 'rgb': (0, 255, 175), 'hsl': (61, 100, 50)},
    'cyan2': {'number': 50, 'hex': '#00ffd7', 'rgb': (0, 255, 215), 'hsl': (70, 100, 50)},
    'cyan1': {'number': 51, 'hex': '#00ffff', 'rgb': (0, 255, 255), 'hsl': (180, 100, 50)},
    'cyan': {'number': 51, 'hex': '#00ffff', 'rgb': (0, 255, 255), 'hsl': (180, 100, 50)},
    'darkred_': {'number': 52, 'hex': '#5f0000', 'rgb': (95, 0, 0), 'hsl': (0, 100, 18)},
    'deeppink4_': {'number': 53, 'hex': '#5f005f', 'rgb': (95, 0, 95), 'hsl': (300, 100, 18)},
    'purple4_': {'number': 54, 'hex': '#5f0087', 'rgb': (95, 0, 135), 'hsl': (82, 100, 26)},
    'purple4': {'number': 55, 'hex': '#5f00af', 'rgb': (95, 0, 175), 'hsl': (72, 100, 34)},
    'purple3': {'number': 56, 'hex': '#5f00d7', 'rgb': (95, 0, 215), 'hsl': (66, 100, 42)},
    'blueviolet': {'number': 57, 'hex': '#5f00ff', 'rgb': (95, 0, 255), 'hsl': (62, 100, 50)},
    'orange4_': {'number': 58, 'hex': '#5f5f00', 'rgb': (95, 95, 0), 'hsl': (60, 100, 18)},
    'grey37': {'number': 59, 'hex': '#5f5f5f', 'rgb': (95, 95, 95), 'hsl': (0, 0, 37)},
    'mediumpurple4': {'number': 60, 'hex': '#5f5f87', 'rgb': (95, 95, 135), 'hsl': (240, 17, 45)},
    'slateblue3_': {'number': 61, 'hex': '#5f5faf', 'rgb': (95, 95, 175), 'hsl': (240, 33, 52)},
    'slateblue3': {'number': 62, 'hex': '#5f5fd7', 'rgb': (95, 95, 215), 'hsl': (240, 60, 60)},
    'royalblue1': {'number': 63, 'hex': '#5f5fff', 'rgb': (95, 95, 255), 'hsl': (240, 100, 68)},
    'royalblue': {'number': 63, 'hex': '#5f5fff', 'rgb': (95, 95, 255), 'hsl': (240, 100, 68)},
    'chartreuse4': {'number': 64, 'hex': '#5f8700', 'rgb': (95, 135, 0), 'hsl': (7, 100, 26)},
    'darkseagreen4_': {'number': 65, 'hex': '#5f875f', 'rgb': (95, 135, 95), 'hsl': (120, 17, 45)},
    'paleturquoise4': {'number': 66, 'hex': '#5f8787', 'rgb': (95, 135, 135), 'hsl': (180, 17, 45)},
    'steelblue': {'number': 67, 'hex': '#5f87af', 'rgb': (95, 135, 175), 'hsl': (210, 33, 52)},
    'steelblue3': {'number': 68, 'hex': '#5f87d7', 'rgb': (95, 135, 215), 'hsl': (220, 60, 60)},
    'cornflowerblue': {'number': 69, 'hex': '#5f87ff', 'rgb': (95, 135, 255), 'hsl': (225, 100, 68)},
    'chartreuse3_': {'number': 70, 'hex': '#5faf00', 'rgb': (95, 175, 0), 'hsl': (7, 100, 34)},
    'darkseagreen4': {'number': 71, 'hex': '#5faf5f', 'rgb': (95, 175, 95), 'hsl': (120, 33, 52)},
    'cadetblue_': {'number': 72, 'hex': '#5faf87', 'rgb': (95, 175, 135), 'hsl': (150, 33, 52)},
    'cadetblue': {'number': 73, 'hex': '#5fafaf', 'rgb': (95, 175, 175), 'hsl': (180, 33, 52)},
    'skyblue3': {'number': 74, 'hex': '#5fafd7', 'rgb': (95, 175, 215), 'hsl': (200, 60, 60)},
    'steelblue1_': {'number': 75, 'hex': '#5fafff', 'rgb': (95, 175, 255), 'hsl': (210, 100, 68)},
    'chartreuse3': {'number': 76, 'hex': '#5fd700', 'rgb': (95, 215, 0), 'hsl': (3, 100, 42)},
    'palegreen3_': {'number': 77, 'hex': '#5fd75f', 'rgb': (95, 215, 95), 'hsl': (120, 60, 60)},
    'seagreen3': {'number': 78, 'hex': '#5fd787', 'rgb': (95, 215, 135), 'hsl': (140, 60, 60)},
    'aquamarine3': {'number': 79, 'hex': '#5fd7af', 'rgb': (95, 215, 175), 'hsl': (160, 60, 60)},
    'mediumturquoise': {'number': 80, 'hex': '#5fd7d7', 'rgb': (95, 215, 215), 'hsl': (180, 60, 60)},
    'steelblue1': {'number': 81, 'hex': '#5fd7ff', 'rgb': (95, 215, 255), 'hsl': (195, 100, 68)},
    'chartreuse2_': {'number': 82, 'hex': '#5fff00', 'rgb': (95, 255, 0), 'hsl': (7, 100, 50)},
    'seagreen2': {'number': 83, 'hex': '#5fff5f', 'rgb': (95, 255, 95), 'hsl': (120, 100, 68)},
    'seagreen1_': {'number': 84, 'hex': '#5fff87', 'rgb': (95, 255, 135), 'hsl': (135, 100, 68)},
    'seagreen1': {'number': 85, 'hex': '#5fffaf', 'rgb': (95, 255, 175), 'hsl': (150, 100, 68)},
    'seagreen': {'number': 85, 'hex': '#5fffaf', 'rgb': (95, 255, 175), 'hsl': (150, 100, 68)},
    'aquamarine1_': {'number': 86, 'hex': '#5fffd7', 'rgb': (95, 255, 215), 'hsl': (165, 100, 68)},
    'darkslategray2': {'number': 87, 'hex': '#5fffff', 'rgb': (95, 255, 255), 'hsl': (180, 100, 68)},
    'darkred': {'number': 88, 'hex': '#870000', 'rgb': (135, 0, 0), 'hsl': (0, 100, 26)},
    'deeppink4__': {'number': 89, 'hex': '#87005f', 'rgb': (135, 0, 95), 'hsl': (17, 100, 26)},
    'darkmagenta_': {'number': 90, 'hex': '#870087', 'rgb': (135, 0, 135), 'hsl': (300, 100, 26)},
    'darkmagenta': {'number': 91, 'hex': '#8700af', 'rgb': (135, 0, 175), 'hsl': (86, 100, 34)},
    'darkviolet_': {'number': 92, 'hex': '#8700d7', 'rgb': (135, 0, 215), 'hsl': (77, 100, 42)},
    'purple_': {'number': 93, 'hex': '#8700ff', 'rgb': (135, 0, 255), 'hsl': (71, 100, 50)},
    'orange4': {'number': 94, 'hex': '#875f00', 'rgb': (135, 95, 0), 'hsl': (2, 100, 26)},
    'lightpink4': {'number': 95, 'hex': '#875f5f', 'rgb': (135, 95, 95), 'hsl': (0, 17, 45)},
    'plum4': {'number': 96, 'hex': '#875f87', 'rgb': (135, 95, 135), 'hsl': (300, 17, 45)},
    'mediumpurple3_': {'number': 97, 'hex': '#875faf', 'rgb': (135, 95, 175), 'hsl': (270, 33, 52)},
    'mediumpurple3': {'number': 98, 'hex': '#875fd7', 'rgb': (135, 95, 215), 'hsl': (260, 60, 60)},
    'slateblue1': {'number': 99, 'hex': '#875fff', 'rgb': (135, 95, 255), 'hsl': (255, 100, 68)},
    'slateblue': {'number': 99, 'hex': '#875fff', 'rgb': (135, 95, 255), 'hsl': (255, 100, 68)},
    'slate': {'number': 99, 'hex': '#875fff', 'rgb': (135, 95, 255), 'hsl': (255, 100, 68)},
    'yellow4_': {'number': 100, 'hex': '#878700', 'rgb': (135, 135, 0), 'hsl': (60, 100, 26)},
    'wheat4': {'number': 101, 'hex': '#87875f', 'rgb': (135, 135, 95), 'hsl': (60, 17, 45)},
    'grey53': {'number': 102, 'hex': '#878787', 'rgb': (135, 135, 135), 'hsl': (0, 0, 52)},
    'lightslategrey': {'number': 103, 'hex': '#8787af', 'rgb': (135, 135, 175), 'hsl': (240, 20, 60)},
    'mediumpurple': {'number': 104, 'hex': '#8787d7', 'rgb': (135, 135, 215), 'hsl': (240, 50, 68)},
    'lightslateblue': {'number': 105, 'hex': '#8787ff', 'rgb': (135, 135, 255), 'hsl': (240, 100, 76)},
    'yellow4': {'number': 106, 'hex': '#87af00', 'rgb': (135, 175, 0), 'hsl': (3, 100, 34)},
    'darkolivegreen3__': {'number': 107, 'hex': '#87af5f', 'rgb': (135, 175, 95), 'hsl': (90, 33, 52)},
    'darkseagreen': {'number': 108, 'hex': '#87af87', 'rgb': (135, 175, 135), 'hsl': (120, 20, 60)},
    'lightskyblue3_': {'number': 109, 'hex': '#87afaf', 'rgb': (135, 175, 175), 'hsl': (180, 20, 60)},
    'lightskyblue3': {'number': 110, 'hex': '#87afd7', 'rgb': (135, 175, 215), 'hsl': (210, 50, 68)},
    'skyblue2': {'number': 111, 'hex': '#87afff', 'rgb': (135, 175, 255), 'hsl': (220, 100, 76)},
    'chartreuse2': {'number': 112, 'hex': '#87d700', 'rgb': (135, 215, 0), 'hsl': (2, 100, 42)},
    'darkolivegreen3_': {'number': 113, 'hex': '#87d75f', 'rgb': (135, 215, 95), 'hsl': (100, 60, 60)},
    'palegreen3': {'number': 114, 'hex': '#87d787', 'rgb': (135, 215, 135), 'hsl': (120, 50, 68)},
    'darkseagreen3_': {'number': 115, 'hex': '#87d7af', 'rgb': (135, 215, 175), 'hsl': (150, 50, 68)},
    'darkslategray3': {'number': 116, 'hex': '#87d7d7', 'rgb': (135, 215, 215), 'hsl': (180, 50, 68)},
    'skyblue1': {'number': 117, 'hex': '#87d7ff', 'rgb': (135, 215, 255), 'hsl': (200, 100, 76)},
    'skyblue': {'number': 117, 'hex': '#87d7ff', 'rgb': (135, 215, 255), 'hsl': (200, 100, 76)},
    'chartreuse1': {'number': 118, 'hex': '#87ff00', 'rgb': (135, 255, 0), 'hsl': (8, 100, 50)},
    'chartreuse': {'number': 118, 'hex': '#87ff00', 'rgb': (135, 255, 0), 'hsl': (8, 100, 50)},
    'lightgreen_': {'number': 119, 'hex': '#87ff5f', 'rgb': (135, 255, 95), 'hsl': (105, 100, 68)},
    'lightgreen': {'number': 120, 'hex': '#87ff87', 'rgb': (135, 255, 135), 'hsl': (120, 100, 76)},
    'palegreen1_': {'number': 121, 'hex': '#87ffaf', 'rgb': (135, 255, 175), 'hsl': (140, 100, 76)},
    'aquamarine1': {'number': 122, 'hex': '#87ffd7', 'rgb': (135, 255, 215), 'hsl': (160, 100, 76)},
    'aquamarine': {'number': 122, 'hex': '#87ffd7', 'rgb': (135, 255, 215), 'hsl': (160, 100, 76)},
    'darkslategray1': {'number': 123, 'hex': '#87ffff', 'rgb': (135, 255, 255), 'hsl': (180, 100, 76)},
    'darkslategray': {'number': 123, 'hex': '#87ffff', 'rgb': (135, 255, 255), 'hsl': (180, 100, 76)},
    'red3_': {'number': 124, 'hex': '#af0000', 'rgb': (175, 0, 0), 'hsl': (0, 100, 34)},
    'deeppink4': {'number': 125, 'hex': '#af005f', 'rgb': (175, 0, 95), 'hsl': (27, 100, 34)},
    'mediumvioletred': {'number': 126, 'hex': '#af0087', 'rgb': (175, 0, 135), 'hsl': (13, 100, 34)},
    'magenta3_': {'number': 127, 'hex': '#af00af', 'rgb': (175, 0, 175), 'hsl': (300, 100, 34)},
    'darkviolet': {'number': 128, 'hex': '#af00d7', 'rgb': (175, 0, 215), 'hsl': (88, 100, 42)},
    'purple__': {'number': 129, 'hex': '#af00ff', 'rgb': (175, 0, 255), 'hsl': (81, 100, 50)},
    'purple (system)': {'number': 129, 'hex': '#af00ff', 'rgb': (175, 0, 255), 'hsl': (81, 100, 50)},
    'darkorange3_': {'number': 130, 'hex': '#af5f00', 'rgb': (175, 95, 0), 'hsl': (2, 100, 34)},
    'indianred_': {'number': 131, 'hex': '#af5f5f', 'rgb': (175, 95, 95), 'hsl': (0, 33, 52)},
    'hotpink3_': {'number': 132, 'hex': '#af5f87', 'rgb': (175, 95, 135), 'hsl': (330, 33, 52)},
    'mediumorchid3': {'number': 133, 'hex': '#af5faf', 'rgb': (175, 95, 175), 'hsl': (300, 33, 52)},
    'mediumorchid': {'number': 134, 'hex': '#af5fd7', 'rgb': (175, 95, 215), 'hsl': (280, 60, 60)},
    'mediumpurple2_': {'number': 135, 'hex': '#af5fff', 'rgb': (175, 95, 255), 'hsl': (270, 100, 68)},
    'darkgoldenrod': {'number': 136, 'hex': '#af8700', 'rgb': (175, 135, 0), 'hsl': (6, 100, 34)},
    'lightsalmon3_': {'number': 137, 'hex': '#af875f', 'rgb': (175, 135, 95), 'hsl': (30, 33, 52)},
    'rosybrown': {'number': 138, 'hex': '#af8787', 'rgb': (175, 135, 135), 'hsl': (0, 20, 60)},
    'brown': {'number': 138, 'hex': '#af8787', 'rgb': (175, 135, 135), 'hsl': (0, 20, 60)},
    'grey63': {'number': 139, 'hex': '#af87af', 'rgb': (175, 135, 175), 'hsl': (300, 20, 60)},
    'mediumpurple2': {'number': 140, 'hex': '#af87d7', 'rgb': (175, 135, 215), 'hsl': (270, 50, 68)},
    'mediumpurple1': {'number': 141, 'hex': '#af87ff', 'rgb': (175, 135, 255), 'hsl': (260, 100, 76)},
    'gold3_': {'number': 142, 'hex': '#afaf00', 'rgb': (175, 175, 0), 'hsl': (60, 100, 34)},
    'darkkhaki': {'number': 143, 'hex': '#afaf5f', 'rgb': (175, 175, 95), 'hsl': (60, 33, 52)},
    'navajowhite3': {'number': 144, 'hex': '#afaf87', 'rgb': (175, 175, 135), 'hsl': (60, 20, 60)},
    'grey69': {'number': 145, 'hex': '#afafaf', 'rgb': (175, 175, 175), 'hsl': (0, 0, 68)},
    'lightsteelblue3': {'number': 146, 'hex': '#afafd7', 'rgb': (175, 175, 215), 'hsl': (240, 33, 76)},
    'lightsteelblue': {'number': 147, 'hex': '#afafff', 'rgb': (175, 175, 255), 'hsl': (240, 100, 84)},
    'yellow3_': {'number': 148, 'hex': '#afd700', 'rgb': (175, 215, 0), 'hsl': (1, 100, 42)},
    'darkolivegreen3': {'number': 149, 'hex': '#afd75f', 'rgb': (175, 215, 95), 'hsl': (80, 60, 60)},
    'darkseagreen3': {'number': 150, 'hex': '#afd787', 'rgb': (175, 215, 135), 'hsl': (90, 50, 68)},
    'darkseagreen2_': {'number': 151, 'hex': '#afd7af', 'rgb': (175, 215, 175), 'hsl': (120, 33, 76)},
    'lightcyan3': {'number': 152, 'hex': '#afd7d7', 'rgb': (175, 215, 215), 'hsl': (180, 33, 76)},
    'lightskyblue1': {'number': 153, 'hex': '#afd7ff', 'rgb': (175, 215, 255), 'hsl': (210, 100, 84)},
    'lightskyblue': {'number': 153, 'hex': '#afd7ff', 'rgb': (175, 215, 255), 'hsl': (210, 100, 84)},
    'greenyellow': {'number': 154, 'hex': '#afff00', 'rgb': (175, 255, 0), 'hsl': (8, 100, 50)},
    'darkolivegreen2': {'number': 155, 'hex': '#afff5f', 'rgb': (175, 255, 95), 'hsl': (90, 100, 68)},
    'palegreen1': {'number': 156, 'hex': '#afff87', 'rgb': (175, 255, 135), 'hsl': (100, 100, 76)},
    'palegreen': {'number': 156, 'hex': '#afff87', 'rgb': (175, 255, 135), 'hsl': (100, 100, 76)},
    'darkseagreen2': {'number': 157, 'hex': '#afffaf', 'rgb': (175, 255, 175), 'hsl': (120, 100, 84)},
    'darkseagreen1_': {'number': 158, 'hex': '#afffd7', 'rgb': (175, 255, 215), 'hsl': (150, 100, 84)},
    'paleturquoise1': {'number': 159, 'hex': '#afffff', 'rgb': (175, 255, 255), 'hsl': (180, 100, 84)},
    'paleturquoise': {'number': 159, 'hex': '#afffff', 'rgb': (175, 255, 255), 'hsl': (180, 100, 84)},
    'red3': {'number': 160, 'hex': '#d70000', 'rgb': (215, 0, 0), 'hsl': (0, 100, 42)},
    'deeppink3_': {'number': 161, 'hex': '#d7005f', 'rgb': (215, 0, 95), 'hsl': (33, 100, 42)},
    'deeppink3': {'number': 162, 'hex': '#d70087', 'rgb': (215, 0, 135), 'hsl': (22, 100, 42)},
    'magenta3__': {'number': 163, 'hex': '#d700af', 'rgb': (215, 0, 175), 'hsl': (11, 100, 42)},
    'magenta3': {'number': 164, 'hex': '#d700d7', 'rgb': (215, 0, 215), 'hsl': (300, 100, 42)},
    'magenta2_': {'number': 165, 'hex': '#d700ff', 'rgb': (215, 0, 255), 'hsl': (90, 100, 50)},
    'darkorange3': {'number': 166, 'hex': '#d75f00', 'rgb': (215, 95, 0), 'hsl': (6, 100, 42)},
    'indianred': {'number': 167, 'hex': '#d75f5f', 'rgb': (215, 95, 95), 'hsl': (0, 60, 60)},
    'hotpink3': {'number': 168, 'hex': '#d75f87', 'rgb': (215, 95, 135), 'hsl': (340, 60, 60)},
    'hotpink2': {'number': 169, 'hex': '#d75faf', 'rgb': (215, 95, 175), 'hsl': (320, 60, 60)},
    'orchid': {'number': 170, 'hex': '#d75fd7', 'rgb': (215, 95, 215), 'hsl': (300, 60, 60)},
    'mediumorchid1_': {'number': 171, 'hex': '#d75fff', 'rgb': (215, 95, 255), 'hsl': (285, 100, 68)},
    'orange3': {'number': 172, 'hex': '#d78700', 'rgb': (215, 135, 0), 'hsl': (7, 100, 42)},
    'lightsalmon3': {'number': 173, 'hex': '#d7875f', 'rgb': (215, 135, 95), 'hsl': (20, 60, 60)},
    'lightpink3': {'number': 174, 'hex': '#d78787', 'rgb': (215, 135, 135), 'hsl': (0, 50, 68)},
    'pink3': {'number': 175, 'hex': '#d787af', 'rgb': (215, 135, 175), 'hsl': (330, 50, 68)},
    'plum3': {'number': 176, 'hex': '#d787d7', 'rgb': (215, 135, 215), 'hsl': (300, 50, 68)},
    'violet': {'number': 177, 'hex': '#d787ff', 'rgb': (215, 135, 255), 'hsl': (280, 100, 76)},
    'gold': {'number': 178, 'hex': '#d7af00', 'rgb': (215, 175, 0), 'hsl': (8, 100, 42)},
    'gold3': {'number': 178, 'hex': '#d7af00', 'rgb': (215, 175, 0), 'hsl': (8, 100, 42)},
    'lightgoldenrod3': {'number': 179, 'hex': '#d7af5f', 'rgb': (215, 175, 95), 'hsl': (40, 60, 60)},
    'tan': {'number': 180, 'hex': '#d7af87', 'rgb': (215, 175, 135), 'hsl': (30, 50, 68)},
    'mistyrose3': {'number': 181, 'hex': '#d7afaf', 'rgb': (215, 175, 175), 'hsl': (0, 33, 76)},
    'thistle3': {'number': 182, 'hex': '#d7afd7', 'rgb': (215, 175, 215), 'hsl': (300, 33, 76)},
    'plum2': {'number': 183, 'hex': '#d7afff', 'rgb': (215, 175, 255), 'hsl': (270, 100, 84)},
    'yellow3': {'number': 184, 'hex': '#d7d700', 'rgb': (215, 215, 0), 'hsl': (60, 100, 42)},
    'khaki3': {'number': 185, 'hex': '#d7d75f', 'rgb': (215, 215, 95), 'hsl': (60, 60, 60)},
    'lightgoldenrod2__': {'number': 186, 'hex': '#d7d787', 'rgb': (215, 215, 135), 'hsl': (60, 50, 68)},
    'lightyellow3': {'number': 187, 'hex': '#d7d7af', 'rgb': (215, 215, 175), 'hsl': (60, 33, 76)},
    'lightyellow': {'number': 187, 'hex': '#d7d7af', 'rgb': (215, 215, 175), 'hsl': (60, 33, 76)},
    'grey84': {'number': 188, 'hex': '#d7d7d7', 'rgb': (215, 215, 215), 'hsl': (0, 0, 84)},
    'lightsteelblue1': {'number': 189, 'hex': '#d7d7ff', 'rgb': (215, 215, 255), 'hsl': (240, 100, 92)},
    'yellow2': {'number': 190, 'hex': '#d7ff00', 'rgb': (215, 255, 0), 'hsl': (9, 100, 50)},
    'darkolivegreen1_': {'number': 191, 'hex': '#d7ff5f', 'rgb': (215, 255, 95), 'hsl': (75, 100, 68)},
    'darkolivegreen1': {'number': 192, 'hex': '#d7ff87', 'rgb': (215, 255, 135), 'hsl': (80, 100, 76)},
    'darkolivegreen': {'number': 192, 'hex': '#d7ff87', 'rgb': (215, 255, 135), 'hsl': (80, 100, 76)},
    'darkseagreen1': {'number': 193, 'hex': '#d7ffaf', 'rgb': (215, 255, 175), 'hsl': (90, 100, 84)},
    'honeydew2': {'number': 194, 'hex': '#d7ffd7', 'rgb': (215, 255, 215), 'hsl': (120, 100, 92)},
    'honeydew': {'number': 194, 'hex': '#d7ffd7', 'rgb': (215, 255, 215), 'hsl': (120, 100, 92)},
    'lightcyan1': {'number': 195, 'hex': '#d7ffff', 'rgb': (215, 255, 255), 'hsl': (180, 100, 92)},
    'lightcyan': {'number': 195, 'hex': '#d7ffff', 'rgb': (215, 255, 255), 'hsl': (180, 100, 92)},
    'red1': {'number': 196, 'hex': '#ff0000', 'rgb': (255, 0, 0), 'hsl': (0, 100, 50)},
    'deeppink2': {'number': 197, 'hex': '#ff005f', 'rgb': (255, 0, 95), 'hsl': (37, 100, 50)},
    'deeppink1_': {'number': 198, 'hex': '#ff0087', 'rgb': (255, 0, 135), 'hsl': (28, 100, 50)},
    'deeppink1': {'number': 199, 'hex': '#ff00af', 'rgb': (255, 0, 175), 'hsl': (18, 100, 50)},
    'deeppink': {'number': 199, 'hex': '#ff00af', 'rgb': (255, 0, 175), 'hsl': (18, 100, 50)},
    'magenta2': {'number': 200, 'hex': '#ff00d7', 'rgb': (255, 0, 215), 'hsl': (9, 100, 50)},
    'magenta1': {'number': 201, 'hex': '#ff00ff', 'rgb': (255, 0, 255), 'hsl': (300, 100, 50)},
    'magenta': {'number': 201, 'hex': '#ff00ff', 'rgb': (255, 0, 255), 'hsl': (300, 100, 50)},
    'orangered1': {'number': 202, 'hex': '#ff5f00', 'rgb': (255, 95, 0), 'hsl': (2, 100, 50)},
    'orangered': {'number': 202, 'hex': '#ff5f00', 'rgb': (255, 95, 0), 'hsl': (2, 100, 50)},
    'indianred1_': {'number': 203, 'hex': '#ff5f5f', 'rgb': (255, 95, 95), 'hsl': (0, 100, 68)},
    'indianred1': {'number': 204, 'hex': '#ff5f87', 'rgb': (255, 95, 135), 'hsl': (345, 100, 68)},
    'hotpink_': {'number': 205, 'hex': '#ff5faf', 'rgb': (255, 95, 175), 'hsl': (330, 100, 68)},
    'hotpink': {'number': 206, 'hex': '#ff5fd7', 'rgb': (255, 95, 215), 'hsl': (315, 100, 68)},
    'mediumorchid1': {'number': 207, 'hex': '#ff5fff', 'rgb': (255, 95, 255), 'hsl': (300, 100, 68)},
    'darkorange': {'number': 208, 'hex': '#ff8700', 'rgb': (255, 135, 0), 'hsl': (1, 100, 50)},
    'salmon1': {'number': 209, 'hex': '#ff875f', 'rgb': (255, 135, 95), 'hsl': (15, 100, 68)},
    'salmon': {'number': 209, 'hex': '#ff875f', 'rgb': (255, 135, 95), 'hsl': (15, 100, 68)},
    'lightcoral': {'number': 210, 'hex': '#ff8787', 'rgb': (255, 135, 135), 'hsl': (0, 100, 76)},
    'palevioletred1': {'number': 211, 'hex': '#ff87af', 'rgb': (255, 135, 175), 'hsl': (340, 100, 76)},
    'palevioletred': {'number': 211, 'hex': '#ff87af', 'rgb': (255, 135, 175), 'hsl': (340, 100, 76)},
    'orchid2': {'number': 212, 'hex': '#ff87d7', 'rgb': (255, 135, 215), 'hsl': (320, 100, 76)},
    'orchid1': {'number': 213, 'hex': '#ff87ff', 'rgb': (255, 135, 255), 'hsl': (300, 100, 76)},
    'orange1': {'number': 214, 'hex': '#ffaf00', 'rgb': (255, 175, 0), 'hsl': (1, 100, 50)},
    'orange': {'number': 214, 'hex': '#ffaf00', 'rgb': (255, 175, 0), 'hsl': (1, 100, 50)},
    'sandybrown': {'number': 215, 'hex': '#ffaf5f', 'rgb': (255, 175, 95), 'hsl': (30, 100, 68)},
    'lightsalmon1': {'number': 216, 'hex': '#ffaf87', 'rgb': (255, 175, 135), 'hsl': (20, 100, 76)},
    'lightsalmon': {'number': 216, 'hex': '#ffaf87', 'rgb': (255, 175, 135), 'hsl': (20, 100, 76)},
    'lightpink1': {'number': 217, 'hex': '#ffafaf', 'rgb': (255, 175, 175), 'hsl': (0, 100, 84)},
    'lightpink': {'number': 217, 'hex': '#ffafaf', 'rgb': (255, 175, 175), 'hsl': (0, 100, 84)},
    'pink1': {'number': 218, 'hex': '#ffafd7', 'rgb': (255, 175, 215), 'hsl': (330, 100, 84)},
    'plum': {'number': 219, 'hex': '#ffafff', 'rgb': (255, 175, 255), 'hsl': (300, 100, 84)},
    'plum1': {'number': 219, 'hex': '#ffafff', 'rgb': (255, 175, 255), 'hsl': (300, 100, 84)},
    'gold1': {'number': 220, 'hex': '#ffd700', 'rgb': (255, 215, 0), 'hsl': (0, 100, 50)},
    'lightgoldenrod2_': {'number': 221, 'hex': '#ffd75f', 'rgb': (255, 215, 95), 'hsl': (45, 100, 68)},
    'lightgoldenrod2': {'number': 222, 'hex': '#ffd787', 'rgb': (255, 215, 135), 'hsl': (40, 100, 76)},
    'navajowhite1': {'number': 223, 'hex': '#ffd7af', 'rgb': (255, 215, 175), 'hsl': (30, 100, 84)},
    'navajowhite': {'number': 223, 'hex': '#ffd7af', 'rgb': (255, 215, 175), 'hsl': (30, 100, 84)},
    'mistyrose1': {'number': 224, 'hex': '#ffd7d7', 'rgb': (255, 215, 215), 'hsl': (0, 100, 92)},
    'mistyrose': {'number': 224, 'hex': '#ffd7d7', 'rgb': (255, 215, 215), 'hsl': (0, 100, 92)},
    'thistle1': {'number': 225, 'hex': '#ffd7ff', 'rgb': (255, 215, 255), 'hsl': (300, 100, 92)},
    'thistle': {'number': 225, 'hex': '#ffd7ff', 'rgb': (255, 215, 255), 'hsl': (300, 100, 92)},
    'yellow1': {'number': 226, 'hex': '#ffff00', 'rgb': (255, 255, 0), 'hsl': (60, 100, 50)},
    'lightgoldenrod1': {'number': 227, 'hex': '#ffff5f', 'rgb': (255, 255, 95), 'hsl': (60, 100, 68)},
    'lightgoldenrod': {'number': 227, 'hex': '#ffff5f', 'rgb': (255, 255, 95), 'hsl': (60, 100, 68)},
    'khaki1': {'number': 228, 'hex': '#ffff87', 'rgb': (255, 255, 135), 'hsl': (60, 100, 76)},
    'khaki': {'number': 228, 'hex': '#ffff87', 'rgb': (255, 255, 135), 'hsl': (60, 100, 76)},
    'wheat1': {'number': 229, 'hex': '#ffffaf', 'rgb': (255, 255, 175), 'hsl': (60, 100, 84)},
    'wheat': {'number': 229, 'hex': '#ffffaf', 'rgb': (255, 255, 175), 'hsl': (60, 100, 84)},
    'cornsilk1': {'number': 230, 'hex': '#ffffd7', 'rgb': (255, 255, 215), 'hsl': (60, 100, 92)},
    'cornsilk': {'number': 230, 'hex': '#ffffd7', 'rgb': (255, 255, 215), 'hsl': (60, 100, 92)},
    'grey100': {'number': 231, 'hex': '#ffffff', 'rgb': (255, 255, 255), 'hsl': (0, 0, 100)},
    'grey3': {'number': 232, 'hex': '#080808', 'rgb': (8, 8, 8), 'hsl': (0, 0, 3)},
    'grey7': {'number': 233, 'hex': '#121212', 'rgb': (18, 18, 18), 'hsl': (0, 0, 7)},
    'grey11': {'number': 234, 'hex': '#1c1c1c', 'rgb': (28, 28, 28), 'hsl': (0, 0, 10)},
    'grey15': {'number': 235, 'hex': '#262626', 'rgb': (38, 38, 38), 'hsl': (0, 0, 14)},
    'grey19': {'number': 236, 'hex': '#303030', 'rgb': (48, 48, 48), 'hsl': (0, 0, 18)},
    'grey23': {'number': 237, 'hex': '#3a3a3a', 'rgb': (58, 58, 58), 'hsl': (0, 0, 22)},
    'grey27': {'number': 238, 'hex': '#444444', 'rgb': (68, 68, 68), 'hsl': (0, 0, 26)},
    'grey30': {'number': 239, 'hex': '#4e4e4e', 'rgb': (78, 78, 78), 'hsl': (0, 0, 30)},
    'grey35': {'number': 240, 'hex': '#585858', 'rgb': (88, 88, 88), 'hsl': (0, 0, 34)},
    'grey39': {'number': 241, 'hex': '#626262', 'rgb': (98, 98, 98), 'hsl': (0, 0, 37)},
    'grey42': {'number': 242, 'hex': '#6c6c6c', 'rgb': (108, 108, 108), 'hsl': (0, 0, 40)},
    'grey46': {'number': 243, 'hex': '#767676', 'rgb': (118, 118, 118), 'hsl': (0, 0, 46)},
    'grey50': {'number': 244, 'hex': '#808080', 'rgb': (128, 128, 128), 'hsl': (0, 0, 50)},
    'grey54': {'number': 245, 'hex': '#8a8a8a', 'rgb': (138, 138, 138), 'hsl': (0, 0, 54)},
    'grey58': {'number': 246, 'hex': '#949494', 'rgb': (148, 148, 148), 'hsl': (0, 0, 58)},
    'grey62': {'number': 247, 'hex': '#9e9e9e', 'rgb': (158, 158, 158), 'hsl': (0, 0, 61)},
    'grey66': {'number': 248, 'hex': '#a8a8a8', 'rgb': (168, 168, 168), 'hsl': (0, 0, 65)},
    'grey70': {'number': 249, 'hex': '#b2b2b2', 'rgb': (178, 178, 178), 'hsl': (0, 0, 69)},
    'grey74': {'number': 250, 'hex': '#bcbcbc', 'rgb': (188, 188, 188), 'hsl': (0, 0, 73)},
    'grey78': {'number': 251, 'hex': '#c6c6c6', 'rgb': (198, 198, 198), 'hsl': (0, 0, 77)},
    'grey82': {'number': 252, 'hex': '#d0d0d0', 'rgb': (208, 208, 208), 'hsl': (0, 0, 81)},
    'grey85': {'number': 253, 'hex': '#dadada', 'rgb': (218, 218, 218), 'hsl': (0, 0, 85)},
    'grey89': {'number': 254, 'hex': '#e4e4e4', 'rgb': (228, 228, 228), 'hsl': (0, 0, 89)},
    'grey93': {'number': 255, 'hex': '#eeeeee', 'rgb': (238, 238, 238), 'hsl': (0, 0, 93)},
}


def _color_conversion(color):
    """
    Converts a color name to its corresponding terminal number code if available; otherwise, returns the color as is.
    """
    return _named_colors_256[color.lower()]["number"] if str(color).lower() in _named_colors_256.keys() else color


def _color_string(color, is_bg=False):
    """
    Generate ANSI color code string for foreground or background color.

    :param color: supporting both named colors (converted via _color_conversion) and hex color codes.
    :param is_bg: If True, generate background color code. Default is False (foreground color).
    """
    if "#" in str(color):  # Hex color
        rgb = tuple(int(color.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
        return f'\x1b[{"48" if is_bg else "38"};2;{rgb[0]};{rgb[1]};{rgb[2]}m'
    else:  # ANSI color code
        return f'\033[{"48" if is_bg else "38"};5;{color}m'


def _style_string(bold: bool = False, underline: bool = False, italic: bool = False, blink: bool = False, reset: bool = False) -> str:
    """
    Generates a string of ANSI escape codes to apply text styles in terminal output.

    :param bold: (bool): If True, applies bold style to the text.
    :param underline: (bool): If True, applies underline style to the text.
    :param italic: (bool): If True, applies italic style to the text. (Note: Italic may not be supported in all terminals.)
    :param blink: (bool): If True, applies blinking style to the text. (Note: Blinking is generally discouraged due to accessibility concerns.)
    :param reset: (bool): Resets to default style

    :returns: str: A string containing the ANSI escape codes for the requested styles, ready to be prefixed to any text intended for terminal output.

    Example:
    >>> print(_style_string(bold=True, underline=True) + "This text will be bold and underlined." + _style_string(reset=True))
    This text will be bold and underlined.
    """
    # Initialize an empty list to hold the style codes
    style_codes = []

    # Append the ANSI codes for each enabled style
    if bold:
        style_codes.append('\033[1m')
    if underline:
        style_codes.append('\033[4m')
    if italic:
        style_codes.append('\033[3m')
    if blink:
        style_codes.append('\033[5m')
    if reset:
        style_codes.append('\x1b[0m')

    # Join and return the style codes as a single string
    return ''.join(style_codes)


def color_print(*args, sep: str = " ", end: str = "\n", color: int or str = "#FFFFFF", bg_color: int or str = None,
                bold: bool = False, underline: bool = False, italic: bool = False, blink: bool = False, **kwargs) -> None:
    """
    Print text with specified foreground color, background color, and text styles.

    end is added to the core string if end == \n making color_print a threadsafe line print

    :param color:
    - Can be hex e.g. #FFFFFF
    - Can be terminal number code e.g. 0 is black
    - Can be any of the following colors:
        "black", "maroon", "green", "olive", "navy", "purple", "plum", "gold", "pink", "slate", "magenta", "orange",
        "purple (system)", "teal", "silver", "grey", "red", "lime", "yellow", "blue", "fuchsia", "aqua", "white",
        "grey0", "navyblue", "darkblue", "blue3", "blue1", "darkgreen", "deepskyblue4", "dodgerblue3", "dodgerblue2",
        "green4", "springgreen4", "turquoise4", "deepskyblue3", "dodgerblue1", "green3", "springgreen3", "darkcyan",
        "lightseagreen", "deepskyblue2", "deepskyblue1", "springgreen2", "cyan3", "darkturquoise", "turquoise2",
        "green1", "springgreen1", "mediumspringgreen", "cyan2", "cyan1", "darkred", "deeppink4", "purple4",
        "purple3", "blueviolet", "orange4", "grey37", "mediumpurple4", "slateblue3", "royalblue1", "chartreuse4",
        "darkseagreen4", "paleturquoise4", "steelblue", "steelblue3", "cornflowerblue", "chartreuse3", "cadetblue",
        "skyblue3", "steelblue1", "palegreen3", "seagreen3", "aquamarine3", "mediumturquoise", "chartreuse2",
        "seagreen2", "seagreen1", "aquamarine1", "darkslategray2", "darkmagenta", "darkviolet", "lightpink4",
        "plum4", "mediumpurple3", "slateblue1", "yellow4", "wheat4", "grey53", "lightslategrey", "mediumpurple",
        "lightslateblue", "darkolivegreen3", "darkseagreen", "lightskyblue3", "skyblue2", "darkseagreen3",
        "darkslategray3", "skyblue1", "chartreuse1", "lightgreen", "palegreen1", "darkslategray1", "red3",
        "mediumvioletred", "magenta3", "darkorange3", "indianred", "hotpink3", "mediumorchid3", "mediumorchid",
        "mediumpurple2", "darkgoldenrod", "lightsalmon3", "rosybrown", "grey63", "mediumpurple1", "gold3", "darkkhaki",
        "navajowhite3", "grey69", "lightsteelblue3", "lightsteelblue", "yellow3", "darkseagreen2", "lightcyan3",
        "lightskyblue1", "greenyellow", "darkolivegreen2", "darkseagreen1", "paleturquoise1", "deeppink3", "magenta2",
        "hotpink2", "orchid", "mediumorchid1", "orange3", "lightpink3", "pink3", "plum3", "violet", "lightgoldenrod3",
        "tan", "mistyrose3", "thistle3", "plum2", "khaki3", "lightgoldenrod2", "lightyellow3", "grey84",
        "lightsteelblue1", "yellow2", "darkolivegreen1", "honeydew2", "lightcyan1", "red1", "deeppink2", "deeppink1",
        "magenta1", "orangered1", "indianred1", "hotpink", "darkorange", "salmon1", "lightcoral", "palevioletred1",
        "orchid2", "orchid1", "orange1", "sandybrown", "brown", "lightsalmon1", "lightpink1", "pink1", "plum1", "gold1",
        "navajowhite1", "mistyrose1", "thistle1", "yellow1", "lightgoldenrod1", "khaki1", "wheat1", "cornsilk1",
        "grey100", "grey3", "grey7", "grey11", "grey15", "grey19", "grey23", "grey27", "grey30", "grey35", "grey39",
        "grey42", "grey46", "grey50", "grey54", "grey58", "grey62", "grey66", "grey70", "grey74", "grey78", "grey82",
        "grey85", "grey89", "grey93"'

    - swaps: green: 2 -> 46
             green1: 46 -> 2
             purple: 129 -> 5
             purple (system): 5 -> 129
    - extra: plum: 219
             gold: 178
             slate: 99
             magenta: 201
             orange: 214
             pink: 13
             brown: 138

    :param bg_color: Background color, can be a hex code, color name, or ANSI color code. Default is None (no background color).
    :param bold: If True, print text in bold. Default is False.
    :param underline: If True, underline the text. Default is False.
    :param italic: If True, print text in italic. Not widely supported in terminals. Default is False.
    :param blink: If True, make the text blink. Not widely supported and generally discouraged. Default is False.
    :param sep: String inserted between values, default a space.
    :param end: String appended after the last value, default a newline.
    """
    # Convert colors and styles
    fg_color_code = _color_string(_color_conversion(color)) if color is not None else ""
    bg_color_code = _color_string(_color_conversion(bg_color), is_bg=True) if bg_color is not None else ""
    style_prefix = _style_string(bold=bold, underline=underline, italic=italic, blink=blink)
    style_suffix = _style_string(reset=True)
    # Construct the print string
    print_string = f"{style_prefix}{fg_color_code}{bg_color_code}{sep.join(map(str, args))}{style_suffix}{end}"
    print(print_string, sep=sep, end=end if end != "\n" else "", **kwargs)


def color_input(prompt: str, color: int or str = "#FFFFFF", bg_color: int or str = None, bold: bool = False,
                underline: bool = False, italic: bool = False, blink: bool = False) -> str:
    """
    Enhanced input function to display the prompt in specified color and style.

    :param prompt: (str): The prompt string, if given, is printed to standard output without a trailing newline before reading input.
    :param color: (int or str): Foreground color of the prompt, specified as a hex code, color name, or ANSI color code.
    :param bg_color: (int or str, optional): Background color of the prompt, specified in the same format as `color`.
    :param bold: (bool): If True, displays prompt in bold style.
    :param underline: (bool): If True, underlines the prompt.
    :param italic: (bool): If True, displays prompt in italic style. Note: may not be supported in all terminals.
    :param blink: (bool): If True, makes the prompt blink. Note: generally discouraged and may not be supported.

    If the user hits EOF (*nix: Ctrl-D, Windows: Ctrl-Z+Return), raise EOFError.
    On *nix systems, readline is used if available.

    :param color:
    - Can be hex e.g. #FFFFFF
    - Can be terminal number code e.g. 0 is black
    - Can be any of the following colors:
        "black", "maroon", "green", "olive", "navy", "purple", "plum", "gold", "pink", "slate", "magenta", "orange",
        "purple (system)", "teal", "silver", "grey", "red", "lime", "yellow", "blue", "fuchsia", "aqua", "white",
        "grey0", "navyblue", "darkblue", "blue3", "blue1", "darkgreen", "deepskyblue4", "dodgerblue3", "dodgerblue2",
        "green4", "springgreen4", "turquoise4", "deepskyblue3", "dodgerblue1", "green3", "springgreen3", "darkcyan",
        "lightseagreen", "deepskyblue2", "deepskyblue1", "springgreen2", "cyan3", "darkturquoise", "turquoise2",
        "green1", "springgreen1", "mediumspringgreen", "cyan2", "cyan1", "darkred", "deeppink4", "purple4",
        "purple3", "blueviolet", "orange4", "grey37", "mediumpurple4", "slateblue3", "royalblue1", "chartreuse4",
        "darkseagreen4", "paleturquoise4", "steelblue", "steelblue3", "cornflowerblue", "chartreuse3", "cadetblue",
        "skyblue3", "steelblue1", "palegreen3", "seagreen3", "aquamarine3", "mediumturquoise", "chartreuse2",
        "seagreen2", "seagreen1", "aquamarine1", "darkslategray2", "darkmagenta", "darkviolet", "lightpink4",
        "plum4", "mediumpurple3", "slateblue1", "yellow4", "wheat4", "grey53", "lightslategrey", "mediumpurple",
        "lightslateblue", "darkolivegreen3", "darkseagreen", "lightskyblue3", "skyblue2", "darkseagreen3",
        "darkslategray3", "skyblue1", "chartreuse1", "lightgreen", "palegreen1", "darkslategray1", "red3",
        "mediumvioletred", "magenta3", "darkorange3", "indianred", "hotpink3", "mediumorchid3", "mediumorchid",
        "mediumpurple2", "darkgoldenrod", "lightsalmon3", "rosybrown", "grey63", "mediumpurple1", "gold3", "darkkhaki",
        "navajowhite3", "grey69", "lightsteelblue3", "lightsteelblue", "yellow3", "darkseagreen2", "lightcyan3",
        "lightskyblue1", "greenyellow", "darkolivegreen2", "darkseagreen1", "paleturquoise1", "deeppink3", "magenta2",
        "hotpink2", "orchid", "mediumorchid1", "orange3", "lightpink3", "pink3", "plum3", "violet", "lightgoldenrod3",
        "tan", "mistyrose3", "thistle3", "plum2", "khaki3", "lightgoldenrod2", "lightyellow3", "grey84",
        "lightsteelblue1", "yellow2", "darkolivegreen1", "honeydew2", "lightcyan1", "red1", "deeppink2", "deeppink1",
        "magenta1", "orangered1", "indianred1", "hotpink", "darkorange", "salmon1", "lightcoral", "palevioletred1",
        "orchid2", "orchid1", "orange1", "sandybrown", "brown", "lightsalmon1", "lightpink1", "pink1", "plum1", "gold1",
        "navajowhite1", "mistyrose1", "thistle1", "yellow1", "lightgoldenrod1", "khaki1", "wheat1", "cornsilk1",
        "grey100", "grey3", "grey7", "grey11", "grey15", "grey19", "grey23", "grey27", "grey30", "grey35", "grey39",
        "grey42", "grey46", "grey50", "grey54", "grey58", "grey62", "grey66", "grey70", "grey74", "grey78", "grey82",
        "grey85", "grey89", "grey93"'

    - swaps: green: 2 -> 46
             green1: 46 -> 2
             purple: 129 -> 5
             purple (system): 5 -> 129
    - extra: plum: 219
             gold: 178
             slate: 99
             magenta: 201
             orange: 214
             pink: 13
             brown: 138
    """
    # Convert colors and styles
    fg_color_code = _color_string(_color_conversion(color)) if color is not None else ""
    bg_color_code = _color_string(_color_conversion(bg_color), is_bg=True) if bg_color is not None else ""
    style_prefix = _style_string(bold=bold, underline=underline, italic=italic, blink=blink)
    style_suffix = _style_string(reset=True)
    # Construct the print string
    prompt_string = f"{style_prefix}{fg_color_code}{bg_color_code}{prompt}{style_suffix}"
    return input(prompt_string)


class Color:
    """
    Allows for creating stylized text as objects for terminal output, supporting foreground and background colors,
    and styles such as bold, underline, italic, and blink. This can be useful for concatenating or storing colored strings.

    Usage:

    >>> print(Color(1, 2, 3, color="green"), "\t", Color("hello", color="orange"), "\t", Color([{}, ()], color="blue"))

    1 2 3   hello   [{}, ()]
      ^       ^        ^
      |       |        |__ blue
      |       |__ orange
      |__ green

    >>> print(Color("Sample text", color="green", bg="black", bold=True, underline=True))

    Sample text   <--- bold and underlined green text on a black background.

    """
    def __init__(self, *args, color: str = "white", bg_color: str = None, bold: bool = False, underline: bool = False,
                 italic: bool = False, blink: bool = False, sep: str = " ", end: str = ""):
        """
        text with specified foreground color, background color, and text styles.

        end is added to the core string if end == \n making color_print a threadsafe line print

        :param color:
        - Can be hex e.g. #FFFFFF
        - Can be terminal number code e.g. 0 is black
        - Can be any of the following colors:
            "black", "maroon", "green", "olive", "navy", "purple", "plum", "gold", "pink", "slate", "magenta", "orange",
            "purple (system)", "teal", "silver", "grey", "red", "lime", "yellow", "blue", "fuchsia", "aqua", "white",
            "grey0", "navyblue", "darkblue", "blue3", "blue1", "darkgreen", "deepskyblue4", "dodgerblue3", "dodgerblue2",
            "green4", "springgreen4", "turquoise4", "deepskyblue3", "dodgerblue1", "green3", "springgreen3", "darkcyan",
            "lightseagreen", "deepskyblue2", "deepskyblue1", "springgreen2", "cyan3", "darkturquoise", "turquoise2",
            "green1", "springgreen1", "mediumspringgreen", "cyan2", "cyan1", "darkred", "deeppink4", "purple4",
            "purple3", "blueviolet", "orange4", "grey37", "mediumpurple4", "slateblue3", "royalblue1", "chartreuse4",
            "darkseagreen4", "paleturquoise4", "steelblue", "steelblue3", "cornflowerblue", "chartreuse3", "cadetblue",
            "skyblue3", "steelblue1", "palegreen3", "seagreen3", "aquamarine3", "mediumturquoise", "chartreuse2",
            "seagreen2", "seagreen1", "aquamarine1", "darkslategray2", "darkmagenta", "darkviolet", "lightpink4",
            "plum4", "mediumpurple3", "slateblue1", "yellow4", "wheat4", "grey53", "lightslategrey", "mediumpurple",
            "lightslateblue", "darkolivegreen3", "darkseagreen", "lightskyblue3", "skyblue2", "darkseagreen3",
            "darkslategray3", "skyblue1", "chartreuse1", "lightgreen", "palegreen1", "darkslategray1", "red3",
            "mediumvioletred", "magenta3", "darkorange3", "indianred", "hotpink3", "mediumorchid3", "mediumorchid",
            "mediumpurple2", "darkgoldenrod", "lightsalmon3", "rosybrown", "grey63", "mediumpurple1", "gold3", "darkkhaki",
            "navajowhite3", "grey69", "lightsteelblue3", "lightsteelblue", "yellow3", "darkseagreen2", "lightcyan3",
            "lightskyblue1", "greenyellow", "darkolivegreen2", "darkseagreen1", "paleturquoise1", "deeppink3", "magenta2",
            "hotpink2", "orchid", "mediumorchid1", "orange3", "lightpink3", "pink3", "plum3", "violet", "lightgoldenrod3",
            "tan", "mistyrose3", "thistle3", "plum2", "khaki3", "lightgoldenrod2", "lightyellow3", "grey84",
            "lightsteelblue1", "yellow2", "darkolivegreen1", "honeydew2", "lightcyan1", "red1", "deeppink2", "deeppink1",
            "magenta1", "orangered1", "indianred1", "hotpink", "darkorange", "salmon1", "lightcoral", "palevioletred1",
            "orchid2", "orchid1", "orange1", "sandybrown", "brown", "lightsalmon1", "lightpink1", "pink1", "plum1", "gold1",
            "navajowhite1", "mistyrose1", "thistle1", "yellow1", "lightgoldenrod1", "khaki1", "wheat1", "cornsilk1",
            "grey100", "grey3", "grey7", "grey11", "grey15", "grey19", "grey23", "grey27", "grey30", "grey35", "grey39",
            "grey42", "grey46", "grey50", "grey54", "grey58", "grey62", "grey66", "grey70", "grey74", "grey78", "grey82",
            "grey85", "grey89", "grey93"'

        - swaps: green: 2 -> 46
                 green1: 46 -> 2
                 purple: 129 -> 5
                 purple (system): 5 -> 129
        - extra: plum: 219
                 gold: 178
                 slate: 99
                 magenta: 201
                 orange: 214
                 pink: 13
                 brown: 138

        :param bg_color: Background color, can be a hex code, color name, or ANSI color code. Default is None (no background color).
        :param bold: If True, print text in bold. Default is False.
        :param underline: If True, underline the text. Default is False.
        :param italic: If True, print text in italic. Not widely supported in terminals. Default is False.
        :param blink: If True, make the text blink. Not widely supported and generally discouraged. Default is False.
        :param sep: String inserted between values, default a space.
        :param end: String appended after the last value, default a newline.
        """
        fg_color_code = _color_string(_color_conversion(color)) if color else ''
        bg_color_code = _color_string(_color_conversion(bg_color), is_bg=True) if bg_color else ''
        style_prefix = _style_string(bold=bold, underline=underline, italic=italic, blink=blink)
        style_suffix = _style_string(reset=True)
        self.string = f"{style_prefix}{fg_color_code}{bg_color_code}{sep.join(map(str, args))}{style_suffix}{end}"

    def __str__(self):
        return self.string

    def __repr__(self):
        return f"<Color string='{self.string}'>"

    def __iadd__(self, other):
        self.string += str(other)
        return self


_last_identifier = None
_first_ever_print = True


def line_print(*args, sep: str = " ", color: str = "#FFFFFF", bg_color: str or int = None, bold: bool = False,
               underline: bool = False, italic: bool = False, blink: bool = False, identifier: str = None):
    """
    Enhanced printing function that supports overwriting the last printed line with the same identifier,
    and includes options for text color, background color, and styles such as bold, underline, italic, and blink.

    :param args: Arguments to be printed.
    :param sep: String inserted between values, default a space.
    :param color: Foreground color of the text.
    :param bg_color: Background color of the text.
    :param bold: If True, print in bold.
    :param underline: If True, underline the text.
    :param italic: If True, print in italic.
    :param blink: If True, text will blink.
    :param identifier: Unique identifier to control overwriting of lines.
      If two lines with the same identifier are sent immediately after one another they will rewrite the line.

    Usage:
    >>> line_print("Starting")
    >>> line_print("Status: working", identifier="status", color="green")
    [ALL PRINTS]
    Starting  <--- standard text styles
    Status: working  <--- green
    >>> line_print("Status: broken", identifier="status", color="red")
    [ALL PRINTS]
    Starting  <--- standard text styles
    Status: broken  <--- red  (replaced the previous green status line)
    >>> line_print("Something has happened", identifier="event", underline=True)
    [ALL PRINTS]
    Starting  <--- standard text styles
    Status: broken  <--- red
    Something has happened  <--- underlined
    """
    global _last_identifier, _first_ever_print
    # Convert colors and styles
    fg_color_code = _color_string(_color_conversion(color)) if color is not None else ""
    bg_color_code = _color_string(_color_conversion(bg_color), is_bg=True) if bg_color is not None else ""
    style_prefix = _style_string(bold=bold, underline=underline, italic=italic, blink=blink)
    style_suffix = _style_string(reset=True)
    print_string = f"{style_prefix}{fg_color_code}{bg_color_code}{sep.join(map(str, args))}{style_suffix}"
    # Determine whether to add a line break or to overwrite the line
    if identifier and identifier == _last_identifier:
        print(f"\r{print_string}", end="", flush=True)
    else:
        line_start = "" if _first_ever_print else "\n"
        print(f"{line_start}{print_string}", end="", flush=True)
    # Update Globals
    _first_ever_print = False
    _last_identifier = identifier


def reset_style():
    """
    Resets the terminal's color and style to the default settings.
    This can be useful after printing styled or colored text to ensure the terminal returns to its normal state.
    """
    print(_style_string(reset=True), end='')


def print_gradient(*args, sep: str = " ", start_color: str, end_color: str) -> None:
    """
    Prints text with a gradient from start_color to end_color.

    :param args: The text to print.
    :param sep: String inserted between values, default a space.
    :param start_color: The starting color name. (From _named_colors_256)
    :param end_color: The ending color name. (From _named_colors_256)

    Usage:
    >>> print_gradient("This Is In A Cool Gradient", 1, 2, 3, start_color="red", end_color="blue")
    This Is In A Cool Gradient 1 2 3  <--- Gradient from red to blue
    """
    start_rgb = _named_colors_256[start_color]["rgb"]
    end_rgb = _named_colors_256[end_color]["rgb"]
    text = sep.join(map(str, args))
    steps = len(text)
    for i, char in enumerate(text):
        # Calculate the intermediate color
        inter_rgb = tuple(start_rgb[j] + (end_rgb[j] - start_rgb[j]) * i // (steps - 1) for j in range(3))
        # Print each character with the calculated color
        print(f'\033[38;2;{inter_rgb[0]};{inter_rgb[1]};{inter_rgb[2]}m{char}', end='')
    reset_style()  # Reset the terminal style after printing


def test_terminal_color_set():
    """
    Prints a grid of terminal color codes and their visual representation.

    This function iterates through the 256-color set available in many modern terminal emulators,
    displaying each color along with its corresponding color code. The color codes are printed
    in a grid format, with each cell showing the color code in its respective color.

    The grid consists of 16 rows and 16 columns, covering the color codes from 0 to 255.
    Each color code is formatted as '\u001b[38;5;{color_code}m', which is the ANSI escape
    sequence for setting foreground text color in terminal emulators that support 256 colors.

    The function utilizes the _style_string function with the reset parameter set to True
    to reset the terminal's color settings after each line is printed. This ensures that
    the terminal's color state is returned to normal after the demonstration is complete.

    Usage:
        Simply call the function without any arguments to print the color grid:
        >>> test_terminal_color_set()

    Note:
        - This function is designed for terminals that support 256-color mode.
        - The appearance of colors may vary depending on the terminal emulator and its configuration.
    """
    for _ in range(0, 16):
        for __ in range(0, 16):
            color_code = str(_ * 16 + __)
            print(u"\u001b[38;5;" + color_code + "m " + color_code.ljust(4), end="")
        print(_style_string(reset=True))


def view_color_names():
    """
    Displays a terminal color chart with named colors.
    """
    _named_colors_256_new = {v['number']: k for k, v in _named_colors_256.items()}  # Assuming this mapping exists
    line_length = 0
    max_line_length = 100  # Maximum number of visible characters per line
    for i in range(0, 256):
        color_code = str(i)
        color_name = _named_colors_256_new.get(i, "Unknown").ljust(4)
        # Estimate the length of the sequence to be printed
        sequence_length = len(color_name) + 1
        # Check if adding this sequence would exceed the max line length
        if line_length + sequence_length > max_line_length:
            print(_style_string(reset=True))  # Reset styles before breaking the line
            line_length = 0  # Reset line length counter
        print(u"\u001b[38;5;" + color_code + "m " + color_name, end="")
        line_length += sequence_length
    print(_style_string(reset=True))  # Ensure styles are reset at the end


def object_print(obj, str_color: str or int = "green1", num_color: str or int = "steelblue1_", default_color: str or int = "white",
                 comma_color: str or int = "darkorange", dict_color: str or int = "white", list_color: str or int = "white",
                 tuple_color: str or int = "white", _print: bool = True):
    """
    Prints objects with type-specific colors for better visualization, supporting strings, numbers, dictionaries, lists, tuples, and sets.

    :param obj: (any): The object to be printed.
    :param str_color: (str or int, optional): Color for strings. Default is `green1`.
    :param num_color: (str or int, optional): Color for numbers (integers and floats). Default is `steelblue1_`.
    :param default_color: (str or int, optional): Default color for objects that don't match any other category. Default is `white`.
    :param comma_color: (str or int, optional): Color for commas separating items in collections. Default is `darkorange`.
    :param dict_color: (str or int, optional): Color for dictionary braces and colons. Default is `white`.
    :param list_color: (str or int, optional): Color for list brackets. Default is `white`.
    :param tuple_color: (str or int, optional): Color for tuple parentheses. Default is `white`.
    :param _print: (bool, optional): If True (default), prints the formatted output directly. If False, returns the formatted string instead.

    Usage:
    >>> object_print({'a': 1, 'b': [1, 2, 3], 'c': {'nested': 'dict'}}, str_color='red', num_color='blue', dict_color='yellow')
    # This prints the dictionary with "a", "b", "c", and 'nested' in red, numbers in blue, and the dictionary braces in yellow.

    Note:
    The function utilizes ANSI color codes and named colors as defined in the `Color` class. Color names correspond to either
    standard ANSI color names or custom defined mappings in the `Color` class. Hex values and ANSI color codes are also supported.

    :returns: None if _print is True. Otherwise, returns a `Color` object representing the colored string.
    """
    print_string = Color()
    if isinstance(obj, dict):
        print_string += Color("{", color=dict_color, end="")
        for i, (k, v) in enumerate(obj.items()):
            print_string += object_print(k, _print=False)
            print_string += Color(": ", color=dict_color, end="")
            print_string += object_print(v, _print=False)
            if i < len(obj)-1:
                print_string += Color(", ", color=comma_color)
        print_string += Color("}", color=dict_color, end="")
    elif isinstance(obj, list):
        print_string += Color("[", color=list_color, end="")
        for i, item in enumerate(obj):
            print_string += object_print(item, _print=False)
            if i < len(obj)-1:
                print_string += Color(", ", color=comma_color, end="")
        print_string += Color("]", color=list_color, end="")
    elif isinstance(obj, (set, frozenset)):
        print_string += Color("{", color=list_color, end="")
        for i, item in enumerate(obj):
            print_string += object_print(item, _print=False)
            if i < len(obj)-1:
                print_string += Color(", ", color=comma_color, end="")
        print_string += Color("}", color=list_color, end="")
    elif isinstance(obj, tuple):
        print_string += Color("(", color=tuple_color, end="")
        for i, item in enumerate(obj):
            print_string += object_print(item, _print=False)
            if i < len(obj)-1:
                print_string += Color(", ", color=comma_color, end="")
        print_string += Color(")", color=tuple_color, end="")
    elif isinstance(obj, str):
        print_string += Color(f"'{obj}'", color=str_color, end="")
    elif isinstance(obj, (int, float)):
        print_string += Color(str(obj), color=num_color, end="")
    else:
        print_string += Color(str(obj), color=default_color, end="")
    if _print:
        print(print_string)
    else:
        return print_string


def style(color: str or int = "#FFFFFF", bg_color: str or int = None, bold: bool = False, underline: bool = False,
          italic: bool = False, blink: bool = False, objects: bool = False):
    """
    Decorator to apply styles to all print statements within the decorated function.

    :param color: Foreground color of the text.
    :param bg_color: Background color of the text.
    :param bold: Apply bold style if True.
    :param underline: Apply underline style if True.
    :param italic: Apply italic style if True.
    :param blink: Apply blink style if True.
    :param objects: Prints objects with type-specific colors for better visualization, supporting strings, numbers, dictionaries, lists, tuples, and sets

    Usage:
    >>> @style(color="green")
    >>> def my_function():
    >>>     print("hiii")
    >>>     print("1", 2, [])
    >>>     color_print("test", color="red")
    >>>
    >>> my_function()

    hiii     <--- This will be green as builtin print was used
    1 2 []   <--- This will be green as builtin print was used
    test     <--- This will be red as color_print was used
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            original_print = builtins.print

            def styled_print(*printargs, **printkwargs):
                fg_color_code = _color_string(_color_conversion(color)) if color is not None else ""
                bg_color_code = _color_string(_color_conversion(bg_color), is_bg=True) if bg_color is not None else ""
                style_prefix = _style_string(bold=bold, underline=underline, italic=italic, blink=blink)
                style_suffix = _style_string(reset=True)
                if objects:
                    styled_args = [object_print(arg, _print=False) for arg in printargs]
                else:
                    styled_args = [style_prefix + fg_color_code + bg_color_code + str(arg) + style_suffix for arg in printargs]
                original_print(*styled_args, **printkwargs)

            builtins.print = styled_print
            try:
                return func(*args, **kwargs)
            finally:
                builtins.print = original_print
        return wrapper
    return decorator
