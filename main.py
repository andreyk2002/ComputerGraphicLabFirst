from CMYK import CMYK
from HLS import HLS
from XYZ import XYZ
import numpy as np


def from_CMYK_to_HLS(cmyk: CMYK):
    r, g, b = from_CMYK_to_RGB(cmyk)
    return from_RGB_to_HLS(r, g, b)


def from_HLS_to_CMYK(hls: HLS):
    r, g, b = from_HLS_to_RGB(hls)
    return from_RGB_to_CMYK(r, g, b)


def from_HLS_to_XYZ(hls: HLS):
    r, g, b = from_HLS_to_RGB(hls)
    return from_RGB_to_XYZ(r, g, b)


def from_XYZ_to_HLS(xyz: XYZ):
    r, g, b = from_XYZ_to_RGB(xyz)
    if r > 255:
        r = 255
    if g > 255:
        g = 255
    if b > 255:
        b = 255
    return from_RGB_to_HLS(r, g, b)


def from_CMYK_to_RGB(cmyk: CMYK):
    r = 255 * (1 - cmyk.cyan) * (1 - cmyk.key)
    g = 255 * (1 - cmyk.magenta) * (1 - cmyk.key)
    b = 255 * (1 - cmyk.yellow) * (1 - cmyk.key)
    return round(r), round(g), round(b)


def from_RGB_to_CMYK(r, g, b):
    k = min(1 - r / 255., 1 - g / 255., 1 - b / 255.)
    c = (1 - r / 255. - k) / (1 - k)
    m = (1 - g / 255. - k) / (1 - k)
    y = (1 - b / 255. - k) / (1 - k)
    return CMYK(c, m, y, k)


def from_RGB_to_HLS(r, g, b):
    r /= 255.
    g /= 255.
    b /= 255.
    high = max(r, g, b)
    low = min(r, g, b)
    h, s, l = ((high + low) / 2,) * 3

    if high == low:
        h = 0.0
        s = 0.0
    else:
        d = high - low
        s = d / (2 - high - low) if l > 0.5 else d / (high + low)
        if high == r:
            h = 60 * (((g - b) / d) % 6)
        elif high == g:
            h = 60 * ((b - r) / d + 2)
        else:
            h = 60 * ((r - g) / d + 4)
    return HLS(h, l, s)


def from_HLS_to_RGB(hls: HLS):
    def value(_p, _q, _t):
        _t += 1 if _t < 0 else 0
        _t -= 1 if _t > 1 else 0
        if _t < 1 / 6:
            return _p + (_q - _p) * 6 * _t
        if _t < 1 / 2:
            return _q
        if _t < 2 / 3:
            _p + (_q - _p) * (2 / 3 - _t) * 6
        return _p

    lightness = hls.lightness
    saturation = hls.saturation
    hue = hls.hue / 360.
    if saturation == 0:
        return lightness, lightness, lightness
    else:
        q = 0
        if lightness < 0.5:
            q = lightness * (1 + saturation)
        else:
            q = lightness + saturation - lightness * saturation
        p = 2 * lightness - q
        r = value(p, q, hue + 1 / 3) * 255
        g = value(p, q, hue) * 255
        b = value(p, q, hue - 1 / 3) * 255
        return round(r), round(g), round(b)


def from_XYZ_to_RGB(xyz: XYZ):
    r = 3.2404542 * xyz.x - 1.5371385 * xyz.y - 0.4985314 * xyz.z
    g = -0.9692660 * xyz.x + 1.8760108 * xyz.y + 0.0415560 * xyz.z
    b = 0.0556434 * xyz.x - 0.2040259 * xyz.y + 1.0572252 * xyz.z
    return round(r * 255), round(g * 255), round(b * 255)


def from_RGB_to_XYZ(r, g, b):
    def __g(x):
        if x >= 0.04045:
            return ((x + 0.055) / 1.055) ** 2.4
        else:
            return x / 12.92

    rn = __g(r / 255) * 100
    gn = __g(g / 255) * 100
    bn = __g(b / 255) * 100
    m = np.array([
        [0.412453, 0.357580, 0.180423],
        [0.212671, 0.715160, 0.072169],
        [0.019334, 0.119193, 0.950227]
    ])
    rgb = np.array([rn, gn, bn]).T
    res = np.matmul(m, rgb)
    return XYZ(res[0], res[1], res[2])


if __name__ == '__main__':
    print(from_HLS_to_XYZ(HLS(359, 0.54, 0.50)))
    print(from_HLS_to_XYZ(HLS(51, 0.22, 0.34)))
    print(from_HLS_to_XYZ(HLS(45, 0.12, 0.09)))

    print(from_XYZ_to_HLS(XYZ(0.4125, 0.2127, 0.01933)))
    print(from_XYZ_to_HLS(XYZ(0.2022, 0.1043, 0.009478)))


