"""unit converts floats to strings with correct SI prefixes."""

import numpy as np


def puc(value=0, unit_si="", precision=3, verbose=False, filecompatible=False):
    """Formatting of values for scientific use of SI units

    from fasttools import unit
    unit(0.1,"m") == "100mm"
    unit(200e-9,"_s") == "200_ns"
    unit(1.000213, "m", precision=5) == "1000.2mm"
    unit(1.0001, " m") == "1 m"  # space
    unit(1.0001, "_m") == "1_m"  # space
    unit(0.911, "%") == "91.1%"  # percent
    unit(1001, "dB") == "30dB"  # dB
    unit(1030e-9, "!m") == "1p03um"

    The following wildcards can be used in the argument unit:
    - "dB" converts to decibels
    - "%" converts to percent
    - " " between number and unit
    - "_" between number and unit
    - "!" generates a filename compatible string "2p43nm"

    verbose=True returns additional information for scaling of vectors"""

    # preprocess input
    try:
        val = np.squeeze(value).astype(float)
    except ValueError as excpt:
        print("Cannot convert input to float")
        print(excpt)
        return value

    # process hidden options
    separator = ""
    if " " in unit_si:
        separator = " "
        unit_si = unit_si.replace(" ", "")
    elif "_" in unit_si:
        separator = "_"
        unit_si = unit_si.replace("_", "")

    if "!" in unit_si:
        filecompatible = True
        unit_si = unit_si.replace("!", "")

    sign = 1
    if val < 0:
        sign = -1
    val *= sign

    if type(precision) not in [float, int]:
        with np.errstate(divide="ignore", invalid="ignore"):
            exponent = np.floor(np.log10(np.min(np.abs(np.diff(precision)))))
        precision = np.abs(exponent - np.floor(np.log10(val))) + 1
    else:
        with np.errstate(divide="ignore", invalid="ignore"):
            exponent = np.floor(np.log10(val))

    if precision == 4 or precision == 5:
        # 1032.1 nm instead of 1.0321 µm
        exponent -= 3

    prefix = ""
    mult = 0

    if unit_si == "dB":
        string = (
            ("{0:." + str(int(precision)) + "g}").format(10 * np.log10(val)) + separator + unit_si
        )
    elif unit_si == "%":
        string = (
            ("{0:." + str(int(precision)) + "g}").format(sign * 100 * val) + separator + unit_si
        )
    else:
        # exponent = floor(log10(val));
        # error: calculation leads to 1e+3 µW instead of 1mW for 9.999e-4 input
        # error: Calculation gives infinity for 0W

        if exponent <= -19:
            prefix = ""
            mult = 0
        elif exponent <= -16:
            prefix = "a"
            mult = -18
        elif exponent <= -13:
            prefix = "f"
            mult = -15
        elif exponent <= -10:
            prefix = "p"
            mult = -12
        elif exponent <= -7:
            prefix = "n"
            mult = -9
        elif exponent <= -4:
            prefix = "µ"
            mult = -6
        elif exponent <= -1:
            prefix = "m"
            mult = -3
        elif exponent <= 2:
            prefix = ""
            mult = 0
        elif exponent <= 5:
            prefix = "k"
            mult = 3
        elif exponent <= 8:
            prefix = "M"
            mult = 6
        elif exponent <= 11:
            prefix = "G"
            mult = 9
        elif exponent <= 14:
            prefix = "T"
            mult = 12
        elif exponent <= 17:
            prefix = "P"
            mult = 15

        string = (
            ("{0:." + str(int(precision)) + "g}").format(sign * val * 10 ** (-mult))
            + separator
            + prefix
            + unit_si
        )
        if "e+03" in string:
            string = (
                ("{0:." + str(int(precision + 1)) + "g}").format(sign * val * 10 ** (-mult))
                + separator
                + prefix
                + unit_si
            )

    # Convert string to be filename compatible
    if filecompatible:
        string = string.replace("µ", "u")
        string = string.replace(".", "p")
        string = string.replace("/", "p")
        string = string.replace(" ", "_")

    if verbose:
        # Return string, multiplier and prefix
        return string, mult, prefix
    else:
        # Return just the formatted string
        return string
