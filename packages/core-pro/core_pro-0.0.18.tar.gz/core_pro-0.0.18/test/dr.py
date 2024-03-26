from src.core_pro import Drive


# url = '1vrcncbs1YGy9rWLBG3s35-mGpcUB8-A7'
# url = '1SU-YjuibMc1xO4KzDdVTSlODhLHrFXlx'
# a = Drive().get_file_info(url)

path = '/Users/xuankhang.do/Downloads/430795821_422470310440615_8279346032025540435_n.jpg'
folder_id = '127h31Zzw-mHnE_-vGEWc3ikKhs1MgQAf'
drive = Drive()
file_id = drive.upload(path, 'test.jpg', folder_id=folder_id)
drive.share_file(file_id, email='xuankhang.do@shopee.com')
