import dropbox
import datetime

from cover.settings import BASE_DIR

dropbox_token = "sl.AtcODiQD0hQkCeVUdva3PcxLT9M3Z2CDiI2_8Rthraf72OMtaA33Cn1siCxBIB-TdZn2ygRMf--ikaL71v7rZmYeXZdGdNn5JwGpOlIxeTL66XagauWngpyUG1PpzoI64qXYr3s"
kyo = datetime.date.today()
w_mae = kyo - datetime.timedelta(weeks=1)
today = kyo.strftime("%Y%m%d")
w_before = w_mae.strftime("%Y%m%d")

source_file_name = "tfc_cover.sqlite"
target_file_name = today + "_" + source_file_name
wbefore_file_name = w_before + "_" + source_file_name

dropbox_path = "/" + source_file_name + "/" + target_file_name
#dropbox_path = "/" + source_file_name + "/" + wbefore_file_name
source_path = BASE_DIR + "/" + source_file_name
wbefore_path = "/" + source_file_name + "/" + wbefore_file_name

client = dropbox.Dropbox(dropbox_token)
client.files_upload(open(source_path, "rb").read(), dropbox_path)
print("upload:{}".format(source_path))

client.files_delete(wbefore_path)
