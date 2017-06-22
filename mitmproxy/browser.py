from selenium import webdriver


def init_firefox_driver():
    try:
        proxy = "localhost"
        port = 8080

        profile = webdriver.FirefoxProfile()
        profile.set_preference('network.proxy.ssl_port', int(port))
        profile.set_preference('network.proxy.ssl', proxy)
        profile.set_preference('network.proxy.http_port', int(port))
        profile.set_preference('network.proxy.http', proxy)
        profile.set_preference('network.proxy.type', 1)

        driver = webdriver.Firefox(executable_path='./geckodriver', firefox_profile=profile)
        driver.set_page_load_timeout(15)
        driver.get('http://www.google.com')

    except Exception as e:
        print(e)
        driver.quit()
    finally:
        return driver





def main():
    driver = init_firefox_driver()
    driver.get("http://www.google.com")
    search_box = driver.find_element_by_name("q")
    search_box.clear()
    search_box.send_keys("imac")
    search_box.submit()

    driver.quit()


if __name__ == "__main__" :
    main()