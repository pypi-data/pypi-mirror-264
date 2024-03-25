from unittest import defaultTestLoader, TextTestRunner

if __name__ == '__main__':
    suite = defaultTestLoader.discover('..')
    TextTestRunner(buffer=False).run(suite)
