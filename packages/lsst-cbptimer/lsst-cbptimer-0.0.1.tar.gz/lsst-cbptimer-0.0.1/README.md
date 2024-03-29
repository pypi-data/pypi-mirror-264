# cbptimer

This is a command line utility for use with logic timer units used in the calibration system for the colimated
beam projector (CBP) at the Rubin Observatory.  The utility leverages [pigpio](https://abyz.me.uk/rpi/pigpio/)
to generate CSV logs of &mu;-second ticks corresponding to edge events on the timer unit TTL trigger inputs.

## Logic Timer Design

The logic timer modules are built on the Raspberry Pi 4b platform, running AlmaLinux 9.  An [Adafruit Ultimate
GPS Hat](https://learn.adafruit.com/adafruit-ultimate-gps-hat-for-raspberry-pi) module is included to provide
GPS-assisted stabilization of the Raspberry Pi clock when GPS reception is available.

A 5V TTL trigger interface is also built out in the prototyping area of the GPS hat.  This utilizes a 74LVC245
for 5V to 3.3V level conversion, and provides jumperable 10K pull up/down and jumperable ground lift on the
TTL side.  The level-converted trigger input is wired through to Pi GPIO 16 via the hat.

<p align="center">
    <img src="images/logictimer.jpeg" height="300">
    <img src="images/schematic.png" height="300">
</p>

## Principle of Operation

The `pigpio` daemon uses the Raspberry Pi hardware DMA engine to sample GPIOs every 5&mu;s (by default). It
queues events recording observed edges, attaching timestamps from the system &mu;-second clock. The Python
side of `pigpio` then reads this queue at its leisure and generates Python callbacks which are used to write
out CSV records. The logged timestamps which are passed to the callbacks are the ones recorded by the daemon,
and are not derived from the Python callback time.

This arrangement should be sufficient for millisecond-accurate timing. If it is necessary to tighten this
further, we could consider configuring `pigpio` for a higher sample frequency (it can get down to a 1&mu;s
sample period) and/or cutting over to a real-time Linux kernel.

## Usage

This package is published on PyPI, so should be installable via:

    pip install lsst-cbptimer

It is assumed
that you will have previously installed `pigpio` (libraries and daemon) as a system-level dependency.  Once
installed:

    usage: cbptimer [-h] [--edge {rising,falling,either}] [--duration DURATION] [--outfile OUTFILE] [--version]

    Log trigger events from CBP calibration logic timer

    optional arguments:
      -h, --help            show this help message and exit
      --edge {rising,falling,either}
                            which types of triggers to log (default: rising)
      --duration DURATION   duration to monitor/log, in seconds (default: infinite; ^C or SIGINT to exit)
      --outfile OUTFILE     where to log (default: stdout)
      --version             show program's version number and exit

## Developer Quickstart

It is recommended to develop within a virtual environment.  The package can be installed in pip "editable" mode via:

    pip install -e .[dev]

The `[dev]` option here will ensure automatic installation of additional Python development support packages (`mypy`, `ruff`, `build`).  Linting and autoformatting can be accomplished via:

    ruff check .
    ruff format .

Type hinting may be checked via:

    mypy src
