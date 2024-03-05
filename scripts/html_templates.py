import streamlit as st


css = '''
<style>

body {color: blue;}

#MainMenu {visibility: hidden;}

footer {visibility: hidden;}

header {visibility: hidden;}          

.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #FFFFFF;
    color: #0D003F;
}
.chat-message.bot {
    background-color: #0D003F;
    color: #FFFFFF;
}
.chat-message .avatar {
  width: 20%;
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
}

.appview-container .main .block-container{
    padding-top: 2rem;
}


#root > div > div.withScreencast > div > div > div > section.css-vk3wp9.e1akgbir11 > div.css-6qob1r.e1akgbir3 {
    background-color:white !important;
    -webkit-box-sizing: content-box;
    -moz-box-sizing: content-box;
    box-sizing: content-box;
    border: 1px solid rgba(49, 51, 63, 0.2);
    -webkit-border-radius: 5px;
    border-radius: 5px;
    font: normal 16px/1 Arial, Helvetica, sans-serif;
    color: #0D003F;
    -o-text-overflow: ellipsis;
    text-overflow: ellipsis;
}   
#root > div:nth-child(1) > div.withScreencast > div > div > div > section.css-vk3wp9.e1akgbir11 > div.css-6qob1r.e1akgbir3 > div.css-79elbk.e1akgbir10 {
    background-color:white;
}   

#root > div > div.withScreencast > div > div > div > section.css-vk3wp9.e1akgbir11 > div.css-6qob1r.e1akgbir3 > div.css-79elbk.e1akgbir10 > ul > li > div > a{
    background-color: white;
    color: red;

}
#root > div:nth-child(1) > div.withScreencast > div > div > div > section.st-emotion-cache-14rvwma.eczjsme11 > div.st-emotion-cache-6qob1r.eczjsme3{
    background-color:white;
}   

#root > div > div.withScreencast > div > div > div > section.css-vk3wp9.e1akgbir11 > div.css-6qob1r.e1akgbir3 > div.css-e3xfei.e1akgbir4 > div > div > div > div > div > button{
    width: 100%;
    font-weight: bold;
}

#root > div > div.withScreencast > div > div > div > section.css-vk3wp9.e1akgbir11 > div.css-6qob1r.e1akgbir3 > div.css-e3xfei.e1akgbir4 > div > div > div > div> div > div > label{
    text-size-adjust: 100%;
    -webkit-font-smoothing: auto;
    user-select: auto;
    font: normal 16px/1 Arial, Helvetica, sans-serif;
    color: #0D003F;
    -webkit-tap-highlight-color: transparent;
    box-sizing: border-box;
    margin-top: 0px;
    margin-bottom: 0px;
    border-top-left-radius: 0.25rem;
    border-top-right-radius: 0.25rem;
    border-bottom-right-radius: 0.25rem;
    border-bottom-left-radius: 0.25rem;
    display: flex;
    cursor: pointer;
    -webkit-box-orient: horizontal;
    -webkit-box-direction: normal;
    flex-direction: row;
    -webkit-box-align: start;
    align-items: start;
    margin-right: 1rem;
    padding-left: 10px;
    padding-right: 2px;
}

#root > div:nth-child(1) > div.withScreencast > div > div > div > section.st-emotion-cache-14rvwma.eczjsme11 > div.st-emotion-cache-6qob1r.eczjsme3 > div.st-emotion-cache-79elbk.eczjsme10 > ul {
 margin-top: 50px;
}

div.stButton button {
    width: 100%;
}

div.stRadio {
    width: 100%;
    background-color:#2B2A2A;
    color: white
}



</style>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://th.bing.com/th/id/OIP.B9NQmVV2CpJRAG6EoWWYDQAAAA?w=158&h=123&c=7&r=0&o=5&dpr=2&pid=1.7" style="height: 78px; width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://th.bing.com/th/id/OIP.GIXeDVtGmcWaqi4GfS2QJAHaFP?pid=ImgDet&rs=1">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''
