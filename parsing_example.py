from bs4 import BeautifulSoup
import requests, pandas as pd, numpy as np

url = ''
response = requests.get(url)
soup = BeautifulSoup(response.content, 'lxml')

product = soup.find_all("product")

frames = []
def cdata_parse(cdata):
    for cdata_code_index in range(len(cdata)):
            cdata[cdata_code_index] = cdata[cdata_code_index].replace("<![CDATA[", "").replace("]]>", "")
    return cdata

def format_as_list(bs4tag, listname):
    for list_code_index in bs4tag:
        listname.append(list_code_index.text)
    return listname

def color_loop(color, color_list, product_variant):
    for color_loop in product_variant:
        if color_loop.find("spec") is not None:
            color = color_loop.find_all("spec")
            for colorloop in color:
                if colorloop["name"] == "Color":
                    color_list.append(colorloop.get_text())
        else:
            color_list.append("")

def size_loop(size, size_list, product_variant):
    for size_loop in product_variant:
        if size_loop.find_all("spec") is not None:
            size = size_loop.find_all("spec")
            for sizeloop in size:
                if size["name"] == "Size":
                    size_list.append(size.get_text())
        else:
            size_list.append("")

for loopp in range(len(product)):

    product_name = product[loopp].find("name")
    product_variant = product[loopp].find_all("variant")
    category = product[loopp].find("maincategory")
    brand = product[loopp].find("brand")
    price = product[loopp].find_all("price")

    name_list, barcode_list, price_list, stock_list       = ([] for i in range(4))
    var_check, category_list, brand_list, stock_code_list = ([] for i in range(4))
    images_list, color, color_list, size, size_list       = ([] for i in range(5))

    barcode_not_found = ["Barcode Not Found!"]

    for image_loop in range(8):
        image = product[loopp].find_all('image' + str(image_loop))
        images_list = format_as_list(image, images_list)

    while("" in images_list):
        images_list.remove("")

    var_check = format_as_list(product_variant, var_check)
    name_list = format_as_list(product_name, name_list)
    category_list = format_as_list(category, category_list)
    brand_list = format_as_list(brand, brand_list)
    price_list = format_as_list(price, price_list)

    name_list = cdata_parse(name_list)
    category_list = cdata_parse(category_list)
    brand_list = cdata_parse(brand_list)

    if not var_check:
        # calculations for products without variants
        barcode = product[loopp].find("barcode")
        stock = product[loopp].find("stock")
        stock_code = product[loopp].find("stock_code")

        stock_list = format_as_list(stock, stock_list)
        stock_code_list = format_as_list(stock_code, stock_code_list)
        barcode_list = format_as_list(barcode, barcode_list)

        barcode_list = cdata_parse(barcode_list)
        stock_code_list = cdata_parse(stock_code_list)

    else:
        for ef in product_variant:
            barcode_list.append(ef.find("barcode").text)

        stock_code = product[loopp].find_all("product_id")
        stock = product[loopp].find_all("quantity")
        stock_code_list = format_as_list(stock_code, stock_code_list)
        stock_list = format_as_list(stock, stock_list)

        barcode_list = cdata_parse(barcode_list)
        stock_code_list = cdata_parse(stock_code_list)

        color_loop(color, color_list, product_variant)
        size_loop(size, color_list, product_variant)


    data = {'Name': name_list,
            'Barcode': barcode_list,
            'Price': price_list,
            'Stock': stock_list,
            'Color': color_list,
            'Size': size_list,
            'Category': category_list,
            'Brand': brand_list,
            'Stock_Code': stock_code_list,
            'Images': images_list
            }

    d = dict(Name = np.array(name_list), Barcode = np.array(barcode_list),
            Price = np.array(price_list), Stock = np.array(stock_list),
            Color = np.array(color_list), Size = np.array(size_list),
            Category = np.array(category_list), Brand = np.array(brand_list),
            Stock_Code = np.array(stock_code_list), Images = np.array(images_list))
    d = pd.DataFrame(dict([(k,pd.Series(v)) for k,v in d.items()]))
    frames.append(d)

result = pd.concat(frames)
result.to_excel (r'C:\Users\xxx\Desktop\xxx\xxx\xxx.xlsx', index = False, header=True)
