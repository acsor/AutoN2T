# AutoN2T
Simple Python script to evaluate a batch of `*.tst` files by means of the
`HardwareSimulator.[sh|bat]` command-line interface from the [Nand2tetris
project](https://www.nand2tetris.org/).

## Usage
On the first run, you'll need to specify the location of the
`HardwareSimulator.[sh|bat]` executable. You can do that likeso:

```
./auton2t.py executable <path to executable>
```

Afterwards checking the completion of any `*.hdl` file will be as easy as doing:

```
./auton2t.py report <directory containing *.tst files>
```

As an example

```
auton2t report nand2tetris/homeworks/first/
```

would yield on a hypothetical `nand2tetris/homeworks/first/` directory

```
[Hardware Simulator executable in /home/acsor/installs/nand2tetris/tools/HardwareSimulator.sh]

DMux4Way.tst         End of script - Comparison ended successfully
Not.tst              End of script - Comparison ended successfully
DMux8Way.tst         End of script - Comparison ended successfully
Mux16.tst            End of script - Comparison ended successfully
Nand16.tst           End of script - Comparison ended successfully
Or.tst               End of script - Comparison ended successfully
And16.tst            End of script - Comparison ended successfully
Or8Way.tst           End of script - Comparison ended successfully
Or16.tst             End of script - Comparison ended successfully
Mux.tst              End of script - Comparison ended successfully
Not16.tst            End of script - Comparison ended successfully
DMux.tst             End of script - Comparison ended successfully
Mux4Way16.tst        End of script - Comparison ended successfully
Xor.tst              End of script - Comparison ended successfully
Mux8Way16.tst        End of script - Comparison ended successfully
And.tst              End of script - Comparison ended successfully
```


## Testing
`AutoN2T` provides **no (unit) testing** -- mind you, this was just supposed to
be a two-hour break from university duties and I intend not to allocate any
more time to it. If some CPU gets hot please feel free to report it to the
Issues or (better yet) Pull Requests page ;-).

## About
`AutoN2T` is built on top of the `argparse` module for the command-line
interface and retrocompatible `subprocess` high-level APIs. Everything else is
just pure Python.
