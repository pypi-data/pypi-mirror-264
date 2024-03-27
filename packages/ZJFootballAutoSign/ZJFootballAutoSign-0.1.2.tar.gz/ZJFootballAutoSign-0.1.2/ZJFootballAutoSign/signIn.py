def trySignIn(account,password,edgeDriverPath = ''):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.edge.service import Service
    from selenium.webdriver.edge.options import Options
    import time
    from os import getcwd
    edge_options = Options()
    edge_options.add_argument('--headless')
    edge_options.add_argument('--disable-gpu')
    edge_options.add_argument('--no-sandbox')
    edge_options.add_argument('--disable-dev-shm-usage')
    edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    time.sleep(0.5)
    driver = webdriver.Edge(service = Service(edgeDriverPath), options = edge_options ) 
    loginUrl = 'https://www.zhejiangfc1998.com/user/login'
    driver.get(loginUrl)
    driver.set_window_size(1920,1080)

    phoneInputBox = driver.find_element(by = By.XPATH , value='//*[@id="__layout"]/div/div[1]/div/div[2]/div/div/form/div[2]/div/div/input')
    passwordInputBox = driver.find_element(by = By.XPATH , value = '//*[@id="__layout"]/div/div[1]/div/div[2]/div/div/form/div[3]/div/div/input')
    loginConfirmButton = driver.find_element(by = By.XPATH , value='//*[@id="__layout"]/div/div[1]/div/div[2]/div/div/form/div[5]/div/div/button[1]')
    phoneInputBox.send_keys(account)
    passwordInputBox.send_keys(password)
    loginConfirmButton.click()

    time.sleep(1)
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(1)

    try:
        moreList = driver.find_element(by = By.XPATH,value='//*[@id="__layout"]/div/div[1]/div[1]/div/div[2]/div/div[4]')
    except:
        print("\n!!!!!账号%s登录页面未跳转,请检查账号密码是否正确!!!!!\n" % account)
        return "failed"
    
    moreList.click()
    centerButton = driver.find_element(by= By.XPATH , value= '//*[@id="__layout"]/div/div[2]/div[3]/div[5]/div/a[3]')
    time.sleep(1.5)
    centerButton.click()
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[-1])

    try:#假设未签到
        signButton = driver.find_element(by = By.XPATH , value = '//*[@id="__layout"]/div/div[1]/section/div[2]/div[2]/div[1]/div/ul/li/a/button')
        signButton.click()
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        statusText = driver.find_element(by = By.XPATH , value= '//*[@id="__layout"]/div/div[1]/section/div[2]/div[2]/div[1]/div/ul/li/a/button/span').text
    except:#已经签到
        statusText = driver.find_element(by = By.XPATH , value= '//*[@id="__layout"]/div/div[1]/section/div[2]/div[2]/div[1]/div/ul/li/div[2]').text

    driver.close()

    if statusText == "已完成":
        return "signed"
    elif statusText == "去签到":
        return "failed"
    else:
        return "ERROR OCCERED!!!"