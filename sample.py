from SearchDospara import SearchDospara

output = ""
print('検索したい商品を入力してください 例:3070ti')
for data in SearchDospara().get(input()):
    item = data.get()
    output += "名前："
    output += item.itemname
    output += "\n値段(税込み)："
    output += str(item.uriamt_tax) + "円"
    output += "\nURL："
    output += "https://www.dospara.co.jp/5shopping/detail_parts.php?ic={itemcode}".format(itemcode=item.itemcode)
    output += "\n"
print(output)