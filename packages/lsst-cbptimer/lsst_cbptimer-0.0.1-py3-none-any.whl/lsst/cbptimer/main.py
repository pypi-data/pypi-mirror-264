import argparse
import importlib.metadata
import pathlib
import signal
import sys
import time

import pigpio  # type: ignore[import-untyped]

PIN = 16  # GPIO pin to monitor
PULL = pigpio.PUD_UP  # internal pull-up/down config for that pin

_edge_from_string = {  # for looking up edge arguments
    "rising": pigpio.RISING_EDGE,
    "falling": pigpio.FALLING_EDGE,
    "either": pigpio.EITHER_EDGE,
}


# to gracefully exit on ^C / SIGNIT
def signal_handler(*_):
    print()  # noqa: T201
    sys.exit(130)


signal.signal(signal.SIGINT, signal_handler)


def main() -> None:
    parser = argparse.ArgumentParser(description="Log trigger events from CBP calibration logic timer")
    parser.add_argument(
        "--edge",
        choices=["rising", "falling", "either"],
        default="rising",
        help="which types of triggers to log (default: %(default)s)",
    )
    parser.add_argument(
        "--duration",
        type=int,
        help="duration to monitor/log, in seconds (default: infinite; ^C or SIGINT to exit)",
    )
    parser.add_argument(
        "--outfile",
        type=pathlib.Path,
        help="where to log (default: stdout)",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"{parser.prog} {importlib.metadata.version('lsst-cbptimer')}",
    )
    args = parser.parse_args()

    if args.outfile is None:
        args.outfile = pathlib.Path("/dev/stdout")

    with args.outfile.open("w") as f:

        def edge_callback(_: int, level: int, tick: int) -> None:
            print(f"{level},{tick}", file=f)

        # setup pigpio pin state and callback...
        pi = pigpio.pi()
        pi.set_mode(PIN, pigpio.INPUT)
        pi.set_pull_up_down(PIN, PULL)
        pi.callback(PIN, _edge_from_string[args.edge], edge_callback)

        # summarize to user what we're up to...
        edge_desc = "both rising and falling" if args.edge == "either" else args.edge
        duration_plural = "s" if args.duration != 1 else ""
        duration_desc = f"for {args.duration} second{duration_plural}" if args.duration is not None else ""
        exit_prompt = "(^C to exit)" if args.duration is None else ""
        print(f"Logging {edge_desc} edges to {f.name} {duration_desc}{exit_prompt}...")  # noqa: T201

        # idle for requested duration or indefinitely...
        if args.duration is not None:
            time.sleep(args.duration)
        else:
            signal.pause()
