import requests

url = "http://example.com/page?param1=value1&param2=value2&page="

for page_num in range(1, 6):  # 假设要获取前5页的内容
    page_url = url + str(page_num)
    response = requests.get(page_url)

    # 在这里处理网页内容，例如提取数据或进行其他操作
    # ...

    # 打印当前页的内容
    print(f"Page {page_num} - Response: {response.text}")
    