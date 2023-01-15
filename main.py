from Nexc import Nexc
from echo_bot import RawTextReplier
from YTDownloader import YTDownloader
import json
import re
from os.path import join
from os import remove

# load config
with open("./config.json", "r") as config_file:
    config = json.load(config_file)
    user = config["user"]
    pw = config["pw"]
    nextcloud_url = config["nextcloud_url"]
    nexc_dest_folder_path = config["nexc_dest_folder_path"]
    bot_token = config["bot_token"]
    local_temp_storage_path = config["local_temp_storage_path"]



# handle message
def handle_message(message):
    # extract link
    yt_pattern = r"http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?"
    if not re.findall(yt_pattern, message):
        print("no link found")
        return
    video_id = re.findall(yt_pattern, message)[0][0]
    
    # confirm request
    
    # download from youtube
    downloader = YTDownloader(local_temp_storage_path)
    output_file = downloader.download(video_id)
    if not output_file:
        print("download failed")
        return
    output_path = join(local_temp_storage_path, output_file)
    
    # upload to owncloud
    nexc = Nexc(user, pw, nextcloud_url)
    link = nexc.put_file(output_path, join(nexc_dest_folder_path, output_file))

    # delete local copy
    remove(output_path)

    # reply with link
    return link

# start bot
bot = RawTextReplier(token=bot_token,
                     reply_function=handle_message, 
                     start_message=("insert start message here"))
bot.run()
