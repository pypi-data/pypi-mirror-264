import requests


class TripleClient:
    def __init__(self, token=None):
        self.session = requests.Session()
        self.if_login = False if token is None else True
        self.stored_data = None
        self.token = token

    def sendVerification(self, email):
        email_data = {
            "user_email": email,
            "language": "zh-CN"
        }
        email_response = self.session.post("https://api.tripleuni.com/v4/user/register/web/email.php", data=email_data)

        if email_response.status_code == 200:
            email_response_data = email_response.json()
            if email_response_data['code'] == 200:
                self.stored_data = email_response_data
                return True

        return False
    
    def verifyCode(self, vcode) -> bool:
        stored_data = self.stored_data
        verify_data = {
            "vcode_vcode": vcode,
            "vcode_key": stored_data['vcode_key'],
            "user_itsc": stored_data['user_itsc'],
            "user_email_suffix": stored_data['user_email_suffix'],
            "user_school_label": stored_data['user_school_label'],
            "language": "zh-CN"
        }
        varify_response = self.session.post("https://api.tripleuni.com/v4/user/register/web/verify.php", data=verify_data)

        if varify_response.status_code == 200:
            varify_response_data = varify_response.json()
            if varify_response_data['code'] == 200:
                self.token = varify_response_data['token']
                return True

        return False
    
    def getPostList(self, page=0):
        post_data = {
            "token": self.token,
            "page": page,
            "language": "zh-CN"
        }
        post_response = self.session.post("https://api.tripleuni.com/v4/post/list/all.php", data=post_data)

        if post_response.status_code == 200:
            post_response_data = post_response.json()
            if post_response_data['code'] == 200:
                return post_response_data
        
        return None
    
    def commentMsg(self, uniPostId, msg, real_name='false'):
        post_data = {
            "token": self.token,
            "uni_post_id": uniPostId,
            "comment_msg": msg,
            "language": "zh-CN",
            "user_is_real_name": real_name
        }

        post_response = self.session.post("https://api.tripleuni.com/v4/comment/post.php", data=post_data)

        if post_response.status_code == 200:
            post_response_data = post_response.json()
            if post_response_data['code'] == 200:
                return True
        
        return False
    
    def createChatSession(self, uni_post_id, real_name='false'):
        post_data = {
            "token": self.token,
            "uni_post_id": uni_post_id,
            "language": "zh-CN",
            "to_type": "post",
            "sender_is_real_name": real_name,
            "comment_order": "null"
        }

        post_response = self.session.post("https://api.tripleuni.com/v4/pm/chat/create.php", data=post_data)

        if post_response.status_code == 200:
            post_response_data = post_response.json()
            if post_response_data['code'] == 200:
                return post_response_data["chat_id"]
        
        return None

    def sendChatMsg(self, chat_id, msg):
        post_data = {
            "token": self.token,
            "chat_id": chat_id,
            "pm_msg": msg,
            "language": "zh-CN"
        }

        post_response = self.session.post("https://api.tripleuni.com/v4/pm/message/send.php", data=post_data)

        if post_response.status_code == 200:
            post_response_data = post_response.json()
            if post_response_data['code'] == 200:
                return True
        
        return False    
    
    def sendChatMsgToPost(self, uni_post_id, msg, real_name='false'):
        chat_id = self.createChatSession(uni_post_id, real_name)
        return self.sendChatMsg(chat_id, msg)
    
if __name__ == "__main__":
    token = ""
    client = TripleClient(token)

    chatId = client.createChatSession(706137)
    print(client.sendChatMsg(chatId, "test"))


    