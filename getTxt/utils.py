# 根据爬取到的内容，将章节标题和内容进行整理，并保存为txt文件。
# import re
import json



# dirty_words = '小提示：按 回车[Enter]键 返回书目，按 ←键 返回上一页， 按 →键 进入下一页。'
# def clear_content(content, dirty_words=None):
#     # 清除内容中的换行符和空格
#     content = content.replace('\n', '').replace('\r', '')
#
#     # 清除内容中的指定字符串
#     content = re.sub(dirty_words, '', content)
#
#     return content





def get_book_info_by_name(json_data, book_name):
    # 将 JSON 字符串转换为 Python 字典（如果已经是字典，则跳过这一步）
    if isinstance(json_data, str):
        json_data = json.loads(json_data)

        # 遍历 books 列表以查找匹配的 book_name
    for book in json_data.get('books', []):
        if book.get('books_name') == book_name:
            # 返回找到的 book_info
            return book.get('books_info')

            # 如果没有找到匹配的 book_name，则返回 None
    return None