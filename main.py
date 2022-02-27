import math
from tkinter import colorchooser

import converters
from CMYK import CMYK
from HLS import HLS
from XYZ import XYZ
import tkinter as tk
import re
import numpy as np

values = [[0 for i in range(0, 4)], [0 for i in range(0, 3)],
          [0 for i in range(0, 3)]]
window = tk.Tk()

inputs = [[tk.Entry(window) for i in range(0, 4)], [tk.Entry(window) for i in range(0, 3)],
          [tk.Entry(window) for i in range(0, 3)]]


def setValues(_values: [], _inputs: [], _new_values: [], ndigits: int = 0):
    for i in range(0, len(_values)):
        _values[i] = round(_new_values[i] * 100, ndigits)
        _inputs[i].delete(0, tk.END)
        _inputs[i].insert(0, str(_values[i]))


def choose_color():
    color_code = colorchooser.askcolor(title="Choose color")
    rgbTuple = color_code[0]
    hls = converters.from_RGB_to_HLS(rgbTuple[0], rgbTuple[1], rgbTuple[2])
    values[1][0] = hls.hue
    values[1][1] = hls.lightness * 100
    values[1][2] = hls.saturation * 100
    change_colors_value(1)
    print(color_code)


def inputEntered(event):
    target: tk.Entry = event.widget
    grid = target.grid_info()
    _row = grid.get('row')
    _column = grid.get('column')
    _row = math.floor(_row / 2)
    _column = math.floor(_column / 2)
    valueStr: str = target.get()

    try:
        value = float(valueStr)
    except ValueError:
        return
    value = check_boundaries(value, _column, _row)
    if value != values[_row][_column]:
        values[_row][_column] = value
        change_colors_value(_row)


def check_boundaries(value: float, value_column, value_row):
    if value < 0:
        return 0
    if value_row == 2:
        return value
    elif value_row == 1 and value_column == 0:
        if value > 360:
            return 360
    elif value > 100:
        return 100
    return value


def change_colors_value(_row):
    if _row == 0:
        cmyk = CMYK(values[0][0] / 100, values[0][1] / 100, values[0][2] / 100, values[0][3] / 100)
        setValues(values[0], inputs[0], [cmyk.cyan, cmyk.magenta, cmyk.yellow, cmyk.key])

        hls = converters.from_CMYK_to_HLS(cmyk)
        setValues(values[1], inputs[1], [hls.hue / 100, hls.lightness, hls.saturation])

        xyz = converters.from_HLS_to_XYZ(hls)
        setValues(values[2], inputs[2], [xyz.x / 100, xyz.y / 100, xyz.z / 100], 4)
    elif _row == 1:
        hls = HLS(values[1][0], values[1][1] / 100, values[1][2] / 100)
        setValues(values[1], inputs[1], [hls.hue / 100, hls.lightness, hls.saturation])

        cmyk = converters.from_HLS_to_CMYK(hls)
        setValues(values[0], inputs[0], [cmyk.cyan, cmyk.magenta, cmyk.yellow, cmyk.key])

        xyz = converters.from_HLS_to_XYZ(hls)
        setValues(values[2], inputs[2], [xyz.x / 100, xyz.y / 100, xyz.z / 100], 4)
    else:
        xyz = XYZ(values[2][0], values[2][1], values[2][2])
        setValues(values[2], inputs[2], [xyz.x / 100, xyz.y / 100, xyz.z / 100], 4)

        hls = converters.from_XYZ_to_HLS(xyz)
        setValues(values[1], inputs[1], [hls.hue / 100, hls.lightness, hls.saturation])

        cmyk = converters.from_HLS_to_CMYK(hls)
        setValues(values[0], inputs[0], [cmyk.cyan, cmyk.magenta, cmyk.yellow, cmyk.key])


if __name__ == '__main__':
    window.title(" Color conversion app")
    window.geometry("840x400")
    tk.Label(window, text="CMYK color value").grid(row=0)
    tk.Label(window, text="cyan:").grid(row=1, column=0)
    tk.Label(window, text="magenta:").grid(row=1, column=2)
    tk.Label(window, text="yellow:").grid(row=1, column=4)
    tk.Label(window, text="key").grid(row=1, column=6)

    tk.Label(window, text="HLS color value").grid(row=2)
    tk.Label(window, text="hue:").grid(row=3, column=0)
    tk.Label(window, text="lightness:").grid(row=3, column=2)
    tk.Label(window, text="saturation:").grid(row=3, column=4)

    tk.Label(window, text="XYZ color value").grid(row=4)
    tk.Label(window, text="x:").grid(row=5, column=0)
    tk.Label(window, text="y:").grid(row=5, column=2)
    tk.Label(window, text="z:").grid(row=5, column=4)

    row = 1
    column = 1
    for rowInputs in inputs:
        for _input in rowInputs:
            _input.grid(row=row, column=column)
            _input.bind("<FocusOut>", lambda event, obj=_input: inputEntered(event))
            column += 2
        row += 2
        column = 1
    tk.Button(window, text="Select color",
              command=choose_color).grid(row=8, column=3)
    window.mainloop()
    # print(from_HLS_to_XYZ(HLS(359, 0.54, 0.50)))
    # print(from_HLS_to_XYZ(HLS(51, 0.22, 0.34)))
    # print(from_HLS_to_XYZ(HLS(45, 0.12, 0.09)))
    #
    # print(from_XYZ_to_HLS(XYZ(0.4125, 0.2127, 0.01933)))
    # print(from_XYZ_to_HLS(XYZ(0.2022, 0.1043, 0.009478)))
    #
