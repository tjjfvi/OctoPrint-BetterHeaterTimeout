# OctoPrint-BetterHeaterTimeout

Turns off heaters after specified time being on and unused.

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/tjjfvi/OctoPrint-BetterHeaterTimeout/archive/master.zip

## Configuration

The checkbox enables/disables the timeout, and the number input changes the timeout length.

### After target temp changes vs after heating starts

If set to the former, changing the target temp will reset the timeout.

### Before/after GCODE

GCODE commands to run before/after the heaters are disabled.
You can use the placeholders `$heater`, `$time_elapsed`. and `$timeout`.
I think the names are pretty self-explanatory.


**Examples:**
```
M117 $heater timed out ; display that on the screen
```
```
M300 S100 P200 ; chirp
```
