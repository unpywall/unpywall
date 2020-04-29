from argparse import ArgumentParser, RawTextHelpFormatter, SUPPRESS
import textwrap
import uuid
import sys

from unpywall import Unpywall


class UnpywallArgumentParser(ArgumentParser):

    def error(self, message: str) -> None:
        print('error: {0}\n'.format(message), end='\n', file=sys.stderr)
        self.print_help()
        sys.exit(2)


class main:

    def __init__(self, test_args=None) -> None:
        self.test_args = test_args
        usage = textwrap.dedent("""unpywall <command> [<args>]

                \nCommand-line tool for interfacing the Unpaywall API
                                """)

        description = textwrap.dedent("""
                 These are common unpywall commands:

                    view        This command opens a local copy of a PDF from
                                a given DOI.
                    download    This command downloads a copy of a PDF from a
                                given DOI.
                    link        This command returns a link to an OA pdf
                                (if available).
                                      """)
        ap = UnpywallArgumentParser(prog='unpywall',
                                    usage=usage,
                                    description=description,
                                    formatter_class=RawTextHelpFormatter,
                                    add_help=False)

        ap.add_argument('command', help=SUPPRESS)
        ap.add_argument('-h',
                        '--help',
                        action='help',
                        default=SUPPRESS,
                        help=SUPPRESS)
        if self.test_args:
            args = ap.parse_args(self.test_args[0:1])
        else:
            args = ap.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unknown option: {}'.format(args.command))
            ap.print_help()
            sys.exit(1)
        getattr(self, args.command)()

    def __repr__(self) -> None:
        return None

    def view(self) -> None:
        ap = UnpywallArgumentParser(description=('This command opens a local'
                                                 ' copy of a PDF from a'
                                                 ' given DOI.'),
                                    formatter_class=RawTextHelpFormatter,
                                    add_help=False)
        ap.add_argument('doi',
                        type=str,
                        metavar='doi',
                        help='\tThe DOI of the document.')
        ap.add_argument('-m',
                        '--mode',
                        type=str,
                        default='viewer',
                        dest='mode',
                        choices=['viewer', 'browser'],
                        metavar='\b',
                        help='\tThe mode for viewing a PDF.')
        ap.add_argument('-b',
                        '--backend',
                        type=str,
                        default='remote',
                        dest='backend',
                        choices=['remote', 'cache', 'snapshot'],
                        metavar='\b',
                        help='\tThe backend you want to use.')
        ap.add_argument('-u',
                        '--progress',
                        type=bool,
                        default=False,
                        dest='progress',
                        metavar='\b',
                        help='\tShow progress bar.')
        ap.add_argument('-h',
                        '--help',
                        action='help',
                        default=SUPPRESS,
                        help=SUPPRESS)

        if self.test_args:
            args = ap.parse_args(self.test_args[1:])
        else:
            args = ap.parse_args(sys.argv[2:])

        Unpywall.view_pdf(args.doi, args.mode, progress=args.progress)

    def download(self) -> None:
        ap = UnpywallArgumentParser(description=('This command downloads a'
                                                 ' copy of a PDF from a'
                                                 ' given DOI.'),
                                    formatter_class=RawTextHelpFormatter,
                                    add_help=False)
        ap.add_argument('doi',
                        type=str,
                        metavar='doi',
                        help='\tThe DOI of the document.')
        ap.add_argument('-f',
                        '--filename',
                        type=str,
                        dest='filename',
                        metavar='\b',
                        help='\tThe filename for downloading a PDF.')
        ap.add_argument('-p',
                        '--path',
                        type=str,
                        default='.',
                        dest='filepath',
                        metavar='\b',
                        help='\tThe filepath for downloading a PDF.')
        ap.add_argument('-b',
                        '--backend',
                        type=str,
                        default='remote',
                        dest='backend',
                        choices=['remote', 'cache', 'snapshot'],
                        metavar='\b',
                        help='\tThe backend you want to use.')
        ap.add_argument('-u',
                        '--progress',
                        type=bool,
                        default=False,
                        dest='progress',
                        metavar='\b',
                        help='\tShow progress bar.')
        ap.add_argument('-h',
                        '--help',
                        action='help',
                        default=SUPPRESS,
                        help=SUPPRESS)

        if self.test_args:
            args = ap.parse_args(self.test_args[1:])
        else:
            args = ap.parse_args(sys.argv[2:])

        try:
            if not args.filename:
                args.filename = '{0}.pdf'.format(uuid.uuid4().hex)
            Unpywall.download_pdf_file(args.doi,
                                       filename=args.filename,
                                       filepath=args.filepath,
                                       progress=args.progress)
            print('File was successfully downloaded.')
        except Exception:
            print('Could not download file.')

    def link(self) -> None:
        ap = UnpywallArgumentParser(description=('This command returns a link'
                                                 ' to an OA pdf'
                                                 ' (if available).'),
                                    formatter_class=RawTextHelpFormatter,
                                    add_help=False)
        ap.add_argument('doi',
                        type=str,
                        metavar='doi',
                        help='\tThe DOI of the document.')
        ap.add_argument('-b',
                        '--backend',
                        type=str,
                        default='remote',
                        dest='backend',
                        choices=['remote', 'cache', 'snapshot'],
                        metavar='\b',
                        help='\tThe backend you want to use.')
        ap.add_argument('-h',
                        '--help',
                        action='help',
                        default=SUPPRESS,
                        help=SUPPRESS)

        if self.test_args:
            args = ap.parse_args(self.test_args[1:])
        else:
            args = ap.parse_args(sys.argv[2:])

        print(Unpywall.get_pdf_link(args.doi))


if __name__ == '__main__':
    main()
