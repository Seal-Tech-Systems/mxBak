import argparse
import datetime
import sys
from os import path

DEFAULT_X = 320
DEFAULT_Y = 240
DEFAULT_Q = 60
DIR = 'backups'
NOW = datetime.datetime.now().strftime("%m%d%Y")
IMAGES_DIR = path.join(DIR, 'images', NOW)
CONFIGS_DIR = path.join(DIR, 'configs', NOW)
LOGGING_ENABLED = False


def _is_int(n):
    try:
        int(n)
    except ValueError:
        return False
    else:
        return True


def query_yes_no(question, default="yes"):
    """
    http://code.activestate.com/recipes/577058/
    Ask a yes/no question via raw_input() and return their answer.
    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def query_int(question, default=None):
    if default and not _is_int(default):
        raise ValueError("invalid default answer: '%s'" % default)
    prompt = ""
    if default is None:
        prompt = " [value] "
    elif default:
        prompt = " [%s] " % default
    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return default
        elif _is_int(choice):
            return choice
        else:
            sys.stdout.write("Please respond with integer number \n")


class Args(object):
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", "--input", type=str,
                            help="specify name of input file, default: "
                                 "'CONFIGS_FOLDER/input.csv'",
                            default='input.csv')
        parser.add_argument("-n", "--non-interactive", help="Interactive mode", action='store_true')
        parser.add_argument("-s", "--backupstills", help="Backup stills", action='store_true')
        parser.add_argument("-x", "--xsize", help="Still X size, default %s" % DEFAULT_X, default=DEFAULT_X)
        parser.add_argument("-y", "--ysize", help="Still Y size, default %s" % DEFAULT_Y, default=DEFAULT_Y)
        parser.add_argument("-q", "--quality", help="Still quality, default %s" % DEFAULT_Q, default=DEFAULT_Q)
        parser.add_argument("-g", "--generateinfo", help="Generate info file", action='store_true')
        parser.add_argument("-c", "--backupconfigs", help="Backup config files", action='store_true')
        self.args = parser.parse_args()


class Config(object):
    def __init__(self, args):
        self._args = args
        self._opts = self._noninteractive_cfg if args.non_interactive else self.interactive_cfg
        self._opts['input'] = self._args.input
        self._opts['current_date'] = NOW
        self._opts['logging'] = LOGGING_ENABLED
        self._opts['output_dir'] = DIR
        self._opts['info_output_filename'] = path.join(CONFIGS_DIR, 'info.csv')
        self._opts['images_dir'] = IMAGES_DIR
        self._opts['configs_dir'] = CONFIGS_DIR

    @property
    def opts(self):
        return self._opts

    @property
    def _noninteractive_cfg(self):
        return {
            'x': self._args.xsize,
            'y': self._args.ysize,
            'q': self._args.quality,

            'backupstills': self._args.backupstills,
            'generateinfo': self._args.generateinfo,
            'backupconfig': self._args.backupconfigs,
        }

    @property
    def interactive_cfg(self):
        print('You are in interactive mode now, read docs to find out how to run in non-interactive mode')

        x = query_int("Enter Still X Size", default=320)
        y = query_int("Enter Still Y Size", default=240)
        q = query_int("Enter Still Quality", default=60)
        backup_stills = query_yes_no("Backup stills?")
        generate_info = query_yes_no("Generate CSV?")
        backup_configs = query_yes_no("Backup configs?")
        return {
            'x': x,
            'y': y,
            'q': q,

            'backupstills': backup_stills,
            'generateinfo': generate_info,
            'backupconfig': backup_configs,
        }


opts = Config(Args().args).opts
