#file_name = "code_update.html"

#複数ファイル名取得
from glob import glob

files = glob("*.html")

for file_name in files:
    with open(file_name) as f:
        data_lines = f.read()

    # 文字列置換
    #print('data_lines', data_lines)
    data_lines = data_lines.replace("loc/loc_base.html", "po/po_base.html")

    # 同じファイル名で保存
    with open(file_name, mode="w") as f:
        f.write(data_lines)
