
from SearchDospara import SearchDospara

# print(SearchDospara().get("3060ti")[0].get())

output = ""
for data in SearchDospara().get("3060ti"):
    item = data.get()
    output += item.itemname
    output += "\n"
    output += str(item.uriamt_tax) + "円"
    output += "\n"
    output += "https://www.dospara.co.jp/5shopping/detail_parts.php?ic={itemcode}".format(itemcode=item.itemcode)
    output += "\n"
print(output)