"""Functions that allow a 1d and 2d parameter scan using the pixie16.

During the parameter scan, one or two settings are changed and a MCA
histogram. The histogram is integrated and plotted against the
parameter.

"""
from dataclasses import dataclass
import sys
import time
from typing import Optional

from matplotlib import pyplot as plt
import numpy as np
from rich.progress import Progress

from . import control

PARAMETERS = [
    ["TRIGGER_RISETIME", "μs", "FASTLENGTH"],
    ["TRIGGER_FLATTOP", "μs", "FASTGAP"],
    ["TRIGGER_THRESHOLD", "ADC units", "FASTTHRESH"],
    ["ENERGY_RISETIME", "μs", "SLOWLENGTH"],
    ["ENERGY_FLATTOP", "μs", "SLOWGAP"],
    ["TAU", "μs", "PREAMPTAU"],
    ["TRACE_LENGTH", "μs", "TRACELENGTH"],
    ["TRACE_DELAY", "μs", "TRIGGERDELAY"],
    ["VOFFSET", "V", "OFFSETDAC"],
    ["XDT", "μs", "XWAIT"],
    ["BASELINE_PERCENT", "%", "BASELINEPERCENT"],
    ["EMIN", "None", "ENERGYLOW"],
    ["BINFACTOR", "None", "LOG2EBIN"],
    ["CHANNEL_CSRA", "bit pattern", "CHANCSRA"],
    ["CHANNEL_CSRB", "bit pattern", "CHANCSRB"],
    ["BLCUT", "None", "BLCUT"],
    ["FASTTRIGBACKLEN", "μs", "FASTTRIGBACKLEN"],
    ["CFDDelay", "μs", "CFDDELAY"],
    ["CFDScale", "None", "CFDSCALE"],
    ["QDCLen0", "μs", "QDCLEN0"],
    ["QDCLen1", "μs", "QDCLEN1"],
    ["QDCLen2", "μs", "QDCLEN2"],
    ["QDCLen3", "μs", "QDCLEN3"],
    ["QDCLen4", "μs", "QDCLEN4"],
    ["QDCLen5", "μs", "QDCLEN5"],
    ["QDCLen6", "μs", "QDCLEN6"],
    ["QDCLen7", "μs", "QDCLEN7"],
    ["ExtTrigStretch", "μs", "EXTTRIGSTRETCH"],
    ["MultiplicityMaskL", "bit pattern", "MULTIPLICITYMASKL"],
    ["MultiplicityMaskH", "bit pattern", "MULTIPLICITYMASKH"],
    ["ExternDelayLen", "μs", "EXTERNDELAYLEN"],
    ["FtrigoutDelay", "μs", "FTRIGOUTDELAY"],
    ["ChanTrigStretch", "μs", "?"],
    ["VetoStretch", "μs", "?"],
]
PARAMETER_NAMES = [x[0] for x in PARAMETERS]


@dataclass
class ScanParameter:
    """A convenient class to store scan parameters."""

    name: str
    module: int
    channel: int
    start: float
    stop: float
    step: float

    def range(self) -> np.ndarray:
        """Return the values that should be scanned."""
        return np.linspace(
            self.start, self.stop, (self.stop - self.start) / self.step + 1
        )


def parameter_scan_1d(
    parameter: ScanParameter,
    dwelltime: int = 0,
    title: Optional[str] = None,
    savefile: Optional[str] = None,
):
    """Do a 1D parameter scan on the pixie16.

    This function assumes that the pixie16 is already booted and ready to take MCA data.
    """
    if parameter.name not in PARAMETER_NAMES:
        print(
            f"ERROR: parameter {parameter.name} not known. Needs ot be one of {','.join(PARAMETER_NAMES)}"
        )
        sys.exit(1)

    if title is None:
        title = "1d-Scan"

    myrange = parameter.range()

    X = []
    Y = []
    fig, ax = plt.subplots()

    with Progress() as progress:
        task = progress.add_task(total=len(myrange))
        for x in myrange:
            progress.update(task, description=f"Value: {x:.1f} ->")
            value = control.set_channel_parameter(
                parameter.name, x * 1e-3, parameter.module, parameter.channel
            )
            X.append(value)

            time.sleep(dwelltime)

            control.start_histogram_run()

            check = 1
            while check == 1:
                # Check Run Status
                plt.pause(1)
                check = control.check_run_status()
            out = control.read_histograms((parameter.module, parameter.channel))
            Y.append(np.sum(out))

            ax.clear()
            ax.set_title(title)
            ax.plot(X, Y, ".-")
            ax.set_xlabel(
                f"M{parameter.module}-ch{parameter.channel} {parameter.name} [ns]"
            )
            ax.set_ylabel("counts")
            fig.canvas.draw()
            plt.pause(0.001)
            progress.advance(task)

    if savefile:
        plt.savefig(savefile)
        print(f"saved plot in {savefile}")

    plt.show(block=True)
    return X, Y


def parameter_scan_2d(
    parameterA: ScanParameter,
    parameterB: ScanParameter,
    dwelltime: int = 0,
    title: Optional[str] = None,
    savefile: Optional[str] = None,
):
    """Do a 2D parameter scan on the pixie16.

    This function assumes that the pixie16 is already booted and ready to take MCA data.

    The data plotted will be from moduleB/channelB.
    """
    for parameter in [parameterA.name, parameterB.name]:
        if parameter not in PARAMETER_NAMES:
            print(
                f"ERROR: parameter {parameter.name} not known. Needs ot be one of {','.join(PARAMETER_NAMES)}"
            )
            sys.exit(1)

    if title is None:
        title = "2d-Scan"

    myrangeA = parameterA.range()
    myrangeB = parameterB.range()

    X = []
    Y = []
    Z = np.zeros((len(myrangeA), len(myrangeB)))

    fig, ax = plt.subplots()

    with Progress() as progress:
        task = progress.add_task(total=len(myrangeA) * len(myrangeB))
        for i, x in enumerate(myrangeA):
            Xvalue = control.set_channel_parameter(
                parameterA.name, x * 1e-3, parameterA.module, parameterA.channel
            )
            for j, y in enumerate(myrangeB):
                progress.update(description=f"X={x:.1f} Y={y:.1f} ->")
                Yvalue = control.set_channel_parameter(
                    parameterB.name, y * 1e-3, parameterB.module, parameterB.channel
                )
                X.append(Xvalue)
                Y.append(Yvalue)

                time.sleep(dwelltime)

                control.start_histogram_run()

                check = 1
                while check == 1:
                    # Check Run Status
                    plt.pause(1)
                    check = control.check_run_status()
                out = control.read_histograms((parameterB.module, parameterB.channel))
                Z[i, j] = np.sum(out)

                ax.clear()
                ax.set_title(title)
                ax.imshow(
                    Z.T,
                    origin="lower",
                    extent=[myrangeA[0], myrangeA[-1], myrangeB[0], myrangeB[-1]],
                )
                ax.set_xlabel(
                    f"M{parameterA.module}-ch{parameterA.channel} {parameterA.name} [ns]"
                )
                ax.set_ylabel(
                    f"M{parameterB.module}-ch{parameterB.channel} {parameterB.name} [ns]"
                )
                fig.canvas.draw()
                plt.pause(0.001)
                progress.advance(task)

    if savefile:
        plt.savefig(savefile)
        print(f"saved plot in {savefile}")

    plt.show(block=True)
    return X, Y, Z
