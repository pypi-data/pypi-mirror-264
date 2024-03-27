<p align="center">
  <img width = 100 src="https://raw.githubusercontent.com/coreyspohn/lod_unit/main/docs/_static/logo.png" alt="lod_unit logo" />
</p>

# lod_unit

This is set up to make it easy to keep coronagraph information in λ/D space with an astropy unit called `lod` ("<ins>L</ins>ambda <ins>O</ins>ver <ins>D</ins>"). Convert into angular units (or vise versa) with an astropy [Equivalency](https://docs.astropy.org/en/stable/units/equivalencies.html) relationship `lod_eq`. See documentation [here](https://lod-unit.readthedocs.io).

## Installation
```bash
pip install lod_unit
```
## Use
Typical use will look like
```python
import astropy.units as u
from lod_unit import lod, lod_eq

diam = 10*u.m
lam = 500*u.nm
separation_lod = 3 * lod
separation_lod.to(u.arcsec, lod_eq(lam, diam))
>> <Quantity 0.03093972 arcsec>

separations_as = [0.1, 0.5, 1]*u.arcsec
separations_as.to(lod, lod_eq(lam, diam))
>> <Quantity [ 9.69627362, 48.48136811, 96.96273622] λ/D>
```

### Gosh Corey, that's a lot of releases with no changes

This was a testing place for GitHub tools on the assumption no one would
notice. Go away.
