import logging

logging.basicConfig(filename='example.log', encoding='utf-8')


def log_to_file():
    i = 0
    while i < 10:
        logging.warning('привет')
        i += 1


if __name__ == '__main__':
    log_to_file()