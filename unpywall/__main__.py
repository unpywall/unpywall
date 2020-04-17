from argparse import ArgumentParser, RawTextHelpFormatter, SUPPRESS
import sys

from unpywall import Unpywall


class UnpywallArgumentParser(ArgumentParser):

    def error(self, message: str) -> None:
        print('error: {0}\n'.format(message), end='\n', file=sys.stderr)
        self.print_help()
        sys.exit(2)


def main():
    ap = UnpywallArgumentParser(prog='unpywall',
                                description=('Command-line tool for'
                                             + ' interfacing the Unpaywall'
                                             + ' API'),
                                formatter_class=RawTextHelpFormatter,
                                add_help=False)
    ap.add_argument('doi',
                    type=str,
                    metavar='doi',
                    help='\tThe DOI to be retrieved.')
    ap.add_argument('method',
                    type=str,
                    metavar='method',
                    help='\tThe method you want to use.')
    ap.add_argument('-b',
                    '--backend',
                    type=str,
                    default='remote',
                    dest='backend',
                    metavar='\b',
                    help='\tThe backend you want to use.')
    ap.add_argument('-e',
                    '--errors',
                    type=str,
                    default='raise',
                    dest='errors',
                    metavar='\b',
                    help='\tThe error behaviour you want to use.')
    ap.add_argument('-h',
                    '--help',
                    action='help',
                    default=SUPPRESS,
                    help='\tShow this help message and exit.')

    args = ap.parse_args()

    doi = args.doi
    errors = args.errors

    if args.method == 'get_pdf':
        print(Unpywall.get_pdf_link(doi, errors))


if __name__ == '__main__':
    main()
