css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
body{
    background: linear-gradient(to bottom, #ffffff, #007bff);
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-container {
            max-width: 600px;
            margin: auto;
            padding: 1rem;
            overflow-y: scroll;
            height: 400px;
            border-radius: 0.5rem;
            background: linear-gradient(to bottom, #ffffff, #007bff);
        }
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''
bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://www.pngitem.com/pimgs/m/122-1223088_one-bot-discord-avatar-hd-png-download.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
    </div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://e7.pngegg.com/pngimages/348/800/png-clipart-man-wearing-blue-shirt-illustration-computer-icons-avatar-user-login-avatar-blue-child.png">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''