import gradio as gr
from hugchat import hugchat
from hugchat.login import Login

EMAIL = "sahilgowda204@gmail.com"
PASSWD = "Sahilgowda2004"
cookie_path_dir = "./cookies/"  
sign = Login(EMAIL, PASSWD)
cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)

chatbot = hugchat.ChatBot(cookies=cookies.get_dict())

def chat_function(message):
    response = chatbot.chat(message).wait_until_done()
    return response

def upload_function(file):
    return f"Uploaded: {file.name}"


with gr.Blocks() as demo:
    with gr.Row():
       
        with gr.Column(scale=1):
            gr.Markdown("## Chat Box")
            chatbox = gr.Chatbot(height=600)
            chat_input = gr.Textbox(show_label=False, placeholder="Type a message...")
            chat_button = gr.Button("Send")

            def update_chat(chatbox, message):                
                chatbox.append(("User", message))                
                response = chat_function(message)
                chatbox.append(("Bot", response))
                return chatbox

            chat_button.click(update_chat, [chatbox, chat_input], chatbox)

        
        with gr.Column(scale=1):
            gr.Markdown("## Generate Image")
            
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### Upload File")
                    file_input = gr.File()
                    upload_button = gr.Button("Upload")
                    suggestion = gr.Textbox(placeholder="Ask how to improve the image...")
                    # upload_response = gr.Textbox()
                    chat_response = gr.Textbox(placeholder="Suggestion how to Improve the image")
                    
                    
        

                    # def handle_upload(file, suggestion_text):
                    #     # Handle file upload and provide response
                    #     file_response = upload_function(file)
                    #     upload_response = gr.Textbox()
                    #     chat_response = chat_function(suggestion_text)
                    #     return file_response, chat_response, upload_response
                    
                    # upload_button.click(handle_upload, [file_input, suggestion], [upload_response, chat_response])

demo.launch()
