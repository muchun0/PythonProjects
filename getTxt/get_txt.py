from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)
class GetTxt:

    def __init__(self, url, title_url_xpath, file_path, logger):
        self.url = url
        self.logger = logger
        self.title_url_xpath = title_url_xpath
        self.file_path = file_path
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(url)
        self.driver.implicitly_wait(20)
        self.title_urls = self.driver.find_element('xpath', title_url_xpath)
        self.title_url, self.title_text = self.get_title_url()

    def get_title_url(self):
        title_url = []
        title_text = []
        for element in self.title_urls.find_elements('tag name', 'li'):
            title = element.text
            # 获取a标签中的gref属性
            gref = element.find_element('tag name', 'a').get_attribute('href')
            title_url.append(gref)
            title_text.append(title)
        return title_url, title_text

    def save_to_txt(self) -> None:
        for i in range(len(self.title_url)):
            # 增加错误重试
            for j in range(3):
                try:
                    self.driver.get(self.title_url[i])
                    self.driver.implicitly_wait(20)
                    content = self.driver.find_element('class name', 'contentbox')
                    content_txt = content.text
                    # 保存到文件
                    self.load_to_txt(self.title_text[i], content_txt)
                    self.driver.close()
                    break

                except Exception as e:
                    self.logger.error(f'第{i}章下载失败，原因：{e}')
                    continue
                finally:
                    self.driver.quit()
                    self.driver = webdriver.Chrome(options=chrome_options)

    def load_to_txt(self, title, content):
        with open(self.file_path, 'a', encoding='utf-8') as file:
            file.write(title + '\n\n')
            # content = clear_content(content)
            file.write(content + '\n')

        self.logger.info(f"{title}已保存至 {self.file_path}")

    def run(self):
        self.save_to_txt()


if __name__ == '__main__':
    url = 'http://www.xheiyan.info/wodewanjiahaoxiongmeng/'
    index_url_xpath = '/html/body/div[4]/div[2]/div[4]/div/ul'
    file_path = r'D:\PythonProjects\PythonProjects\PythonProjects\getTxt\我的玩家好凶猛.txt'
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(20)
    index_url = driver.find_element('xpath', index_url_xpath)

    get_txt = GetTxt(url, index_url_xpath, file_path,logger=logging)
    get_txt.run()
