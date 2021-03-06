#!/usr/bin/env python
# vim:fileencoding=utf-8
from __future__ import (unicode_literals, division, absolute_import,
                        print_function)

__license__ = 'GPL v3'
__copyright__ = '2013, Kovid Goyal <kovid at kovidgoyal.net>'

import sys, os, importlib

from PyQt4.Qt import QIcon

from calibre.constants import islinux
from calibre.gui2 import Application, ORG_NAME, APP_UID, setup_gui_option_parser, detach_gui
from calibre.ptempfile import reset_base_dir
from calibre.utils.config import OptionParser

def option_parser():
    parser =  OptionParser(_('''\
%prog [opts] [path_to_ebook]

Launch the calibre edit book tool.
'''))
    setup_gui_option_parser(parser)
    parser.add_option('--edit-file', help=_(
        'Edit the named file inside the book'))
    return parser

def gui_main(path=None, notify=None):
    _run(['ebook-edit', path], notify=notify)

def _run(args, notify=None):
    # Ensure we can continue to function if GUI is closed
    os.environ.pop('CALIBRE_WORKER_TEMP_DIR', None)
    reset_base_dir()

    # The following two lines are needed to prevent circular imports causing
    # errors during initialization of plugins that use the polish container
    # infrastructure.
    importlib.import_module('calibre.customize.ui')
    from calibre.gui2.tweak_book.ui import Main

    parser = option_parser()
    opts, args = parser.parse_args(args)
    if getattr(opts, 'detach', False):
        detach_gui()
    override = 'calibre-edit-book' if islinux else None
    app = Application(args, override_program_name=override)
    app.load_builtin_fonts()
    app.setWindowIcon(QIcon(I('tweak.png')))
    Application.setOrganizationName(ORG_NAME)
    Application.setApplicationName(APP_UID)
    main = Main(opts, notify=notify)
    sys.excepthook = main.unhandled_exception
    main.show()
    if len(args) > 1:
        main.boss.open_book(args[1], edit_file=opts.edit_file, clear_notify_data=False)
    app.exec_()

def main(args=sys.argv):
    _run(args)

if __name__ == '__main__':
    main()

