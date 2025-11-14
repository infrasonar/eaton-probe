from libprobe.probe import Probe
from lib.check.ups import CheckUps
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = (
        CheckUps,
    )

    probe = Probe("eaton", version, checks)

    probe.start()
