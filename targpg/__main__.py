"""Run Targpg from the command line"""
import sys

from targpg import Targpg, tglog, targpg_parser


def main():
    """Run from the command line, use `--help` to see usage"""
    parser = targpg_parser()
    args = parser.parse_args()

    try:
        tar = Targpg(
            filename=args.archive,
            passfile=args.passfile,
            autocreate=args.autocreate,
        )
    except KeyboardInterrupt:
        tglog.info("\nExiting program, cya later")
        sys.exit(1)

    try:
        if args.list:
            tar.list()
        if args.add:
            tar.add(
                *args.add,
                directory=args.directory,
                unique=args.unique,
                update=args.update,
            )
        if args.extr is not None:
            tar.extract(*args.extr, outdir=args.output)
    except (KeyboardInterrupt, FileNotFoundError):
        tglog.info("\nExiting program, cya later")
    # pylint: disable=broad-except
    except Exception as e:
        tglog.error("error; %s", e)
    else:
        if args.add:
            tar.save()
    finally:
        tar.exit()


if __name__ == "__main__":
    main()
