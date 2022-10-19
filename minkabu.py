import bs4
import requests

def minkabu(companyName : str, delisting=False) -> dict :
    
    """
    This function 'minkabu' retrieves the securities code from the name of a Japanese 
    listed company.
    In doing so, it scrapes the website to obtain the most recent data for the dataset. It should 
    be used with care to avoid burdening the partner network.

    Args:
        companyName (str): Name of the company you wish to search. ex."トヨタ"
        delisting (bool): Flag which determine whether to include delisted companies. 
                            False if not included, True if included.

    Returns:
        dict: A dictionary whose key is the company name and whose value is its security code.

    """

    #VARIABLES
    URL : str
    res : requests.models.Response
    soup : bs4.BeautifulSoup
    foundCodeName : bs4.element.ResultSet
    code : str
    name : str
    foundCode : bs4.element.Tag
    foundCodeReplaced : str
    foundName : bs4.element.Tag
    foundNameReplaced : str
    
    result : dict

    ### PROCESS ###

    URL = r"https://minkabu.jp/stock/find?tag="
    URL += companyName

    res = requests.get(URL)
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    foundCodeName = soup.find_all("td", class_="vamd bgwt")


    #銘柄検索の結果
    result = {}
    for element in foundCodeName :
        element.text.replace(" ", "")

        code = ""
        for i in range(8, 12) :
            code += element.text[i]
        
        #上場廃止の場合は、delistingFlagがTrueになっているときだけ含める。
        if code == "上場廃止" and delisting==False :
            continue

        name = ""
        for i in range(19, len(element.text)-2) : #必ず最後にふたつ空白が来るので
            name += element.text[i]

        result[name] = code


    #銘柄検索の結果、単一の候補が見つかった場合、違うページに遷移するので、その対応。
    if result == {} :
        try :
            #証券コード
            foundCode = soup.find("div", class_="stock_label")
            foundCodeReplaced = foundCode.text.replace(" ", "") #この変換は必要。
            code = ""
            for i in range(1, 5) :
                code += foundCodeReplaced[i]

            #名前
            foundName = soup.find("p", class_="md_stockBoard_stockName")
            foundNameReplaced = foundName.text.replace(" ", "") #この変換は必要。
            name = foundNameReplaced

            #resultを完成させる
            result[name] = code
        except :
            return {}

    return result


if __name__ == "__main__" :
    companyName = "ニトリ"
    print(minkabu(companyName))