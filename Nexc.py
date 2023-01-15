import owncloud


class Nexc:
    def __init__(self, user, pw, nextcloud_url):
        # Initialize Client
        self.client = owncloud.Client(nextcloud_url)
        self.client.login(user, pw) # ToDo: Create a seperate User to be used here

    def put_file(self, local_path, remote_path):
        """Puts a file on the owncloud and returns the public link"""
        self.client.put_file(remote_path, local_path)
        link_info = self.client.share_file_with_link(remote_path)
        return link_info.get_link()

