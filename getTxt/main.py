from get_txt import GetTxt
import json
from utils import get_book_info_by_name
from logging_config import get_logger


def main(book_name):
    logger = get_logger(book_name)
    # load book_config
    with open('book_config.json', 'r', encoding='utf-8') as f:
        book_config = json.load(f)
    book_info = get_book_info_by_name(book_config, book_name)
    if book_info is None:
        logger.error('未找到该书籍')
        return

    # get book txt
    get_txt = GetTxt(url=book_info['book_url'], title_url_xpath=book_info['index_url_xpath'],
                     file_path=book_info['file_path'], logger=logger)
    get_txt.run()


if __name__ == '__main__':
    book_name = '太初'
    main(book_name)
