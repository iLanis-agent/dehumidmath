# Dehumid Math

Dehumidifier honesty. The pint count on the box was measured in a warmer room than your basement.

- Landing: `index.html`
- App: `app.html` (loads `engine.js`)

## What it does

In 2019 the test changed. A dehumidifier's pint count is measured in a lab room, and the 2019
lab room is cooler than the 2012 one - so today's 50-pint box is yesterday's 70-pint box, and
your basement is cooler than either lab. Three panels of honest arithmetic:

- **The label truth** - translates a pint rating between the 2012 and 2019 test scales.
- **The room truth** - weighs room size and dampness (labeled sizing norms, 2012 scale)
  against the unit's label, converting standards first: required versus offered, with the
  margin or the shortfall.
- **The bucket truth** - daily pull versus bucket size, in hours between emptyings.

## Norms used (labeled, illustrative)

- 2019-scale pints = 2012-scale pints x 0.72 (approximate standards-shift norm).
- Room need, 2012 scale: 10/12/14/16 pints a day at 500 square feet for
  damp / very damp / wet / extremely wet, plus 4/5/6/7 pints per further 500 square feet.

Every figure is hypothetical arithmetic on labeled norms, not a statement about any real
room, unit or installation. Follow the manufacturer's sizing guidance and manual.

## Tests

`oracle.py` generates `expected.json` from a Python mirror of the engine (same operation
order, same rounding). `node test.js` checks the JavaScript engine against it:

```
python3 oracle.py
node test.js
```
