from libprobe.probe import Probe
from lib.check.ups import check_ups
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = {
        'ups': check_ups,
    }

    probe = Probe("eaton", version, checks)

    probe.start()
