# FaSt_PUC
FaSt_PUC is a pretty unit converter.
It creates a string with suitable SI-prefix.

Written by Fabian Stutzki, fast@fast-apps.de

licensed under MIT

## Usage
The package has to be imported:

```python
import fast_puc
```

It can be used very easily:

```python
puc(1.0001)  # "1"
puc(1.0001, "m")  # "1m"
puc(0.991e-6, "s")  # "991ns"
puc(1030e-9, "m")  # "1.03µm"
```

Unit supports some special characters:

```python
puc(1.0001, " m")  # "1 m"  # space
puc(1.0001, "_m")  # "1_m"  # underscore
puc(0.911, "%")  # "91.1%"  # percent
puc(1001, "dB")  # "30dB"  # conversion to dB
puc(1030e-9, "!m")  # "1p03um"  # file name compatible
```