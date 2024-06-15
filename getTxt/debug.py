


# 初始化计数器
li_counter = 0


# 假设你有一个函数可以定位到<ul>元素中的特定<li>
def get_li_element(counter):
    # 这里只是一个示例，你需要根据实际情况定位<ul>和<li>
    ul_element = driver.find_element(By.CSS_SELECTOR, 'ul#your-ul-id')
    lis = ul_element.find_elements(By.TAG_NAME, 'li')
    if counter < len(lis):
        return lis[counter]
    else:
        return None


try:
    while True:
        # 获取当前要点击的<li>元素
        li_element = get_li_element(li_counter)
        if li_element is None:
            break  # 如果没有更多的<li>元素，则退出循环
        li_element.click()

        # 在这里添加逻辑来处理页面跳转后的内容
        # 例如，等待新页面加载完成并获取内容
        WebDriverWait(driver, 10).until(EC.title_contains('新页面的标题部分'))
        print(driver.title)
        # ... 其他操作 ...

        # 如果你需要返回到原始页面以继续点击下一个<li>
        # 注意：这可能会导致状态不一致或其他问题，尽量避免这样做
        # driver.get('原始页面的URL')  # 如果可能的话，避免这样做

        # 更新计数器以点击下一个<li>
        li_counter += 1

except (StaleElementReferenceException, NoSuchElementException):
    # 如果元素引用失效或找不到元素，尝试重新定位并继续
    # 在这个例子中，我们简单地捕获异常并退出循环，因为我们已经处理了所有<li>
    pass

finally:
    # 关闭WebDriver
    driver.quit()