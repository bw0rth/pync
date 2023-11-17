import pync


def main():
    pync.run('-vlky "import sys; sys.stdout.write(sys.stdin.read())" localhost 8000')


if __name__ == '__main__':
    main()