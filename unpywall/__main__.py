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
                    choices=['pdf_link', 'download_pdf', 'view_pdf'],
                    help='\tThe method you want to use.')
    ap.add_argument('-b',
                    '--backend',
                    type=str,
                    default='remote',
                    dest='backend',
                    choices=['remote', 'cache', 'snapshot'],
                    metavar='\b',
                    help='\tThe backend you want to use.')
    ap.add_argument('-e',
                    '--errors',
                    type=str,
                    default='raise',
                    dest='errors',
                    choices=['raise', 'ignore'],
                    metavar='\b',
                    help='\tThe error behaviour you want to use.')
    ap.add_argument('-f',
                    '--filename',
                    type=str,
                    dest='filename',
                    metavar='\b',
                    help='\tThe filename for downloading a PDF.')
    ap.add_argument('-m',
                    '--mode',
                    type=str,
                    default='viewer',
                    dest='mode',
                    choices=['viewer', 'browser'],
                    metavar='\b',
                    help='\tThe mode for viewing a PDF.')
    ap.add_argument('-p',
                    '--path',
                    type=str,
                    dest='filepath',
                    metavar='\b',
                    help='\tThe filepath for downloading a PDF.')
    ap.add_argument('-h',
                    '--help',
                    action='help',
                    default=SUPPRESS,
                    help='\tShow this help message and exit.')

    args = ap.parse_args()

    doi = args.doi

    if args.method == 'pdf_link':
        print(Unpywall.get_pdf_link(doi))

    if args.method == 'download_pdf':
        try:
            Unpywall.download_pdf_file(doi, args.filename, args.filepath)
            print('File was successfully downloaded.')
        except Exception:
            print('Could not download file.')

    if args.method == 'view_pdf':
        Unpywall.view_pdf(doi, mode=args.mode)


if __name__ == '__main__':
    main()
