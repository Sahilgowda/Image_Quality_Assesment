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

def generate_image(prompt):
   
    return "Image would be generated based on: " + prompt

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    with gr.Row():
        # Left column for chat
        with gr.Column(scale=1):
            gr.Markdown("## Chat Box")
            chatbox = gr.Chatbot(height=600)
            chat_input = gr.Textbox(show_label=False, placeholder="Type a message...")
            chat_button = gr.Button("Send")

       
        with gr.Column(scale=2):
            gr.Markdown("## Image Generation and Analysis")
            
            
            with gr.Row():
                with gr.Column(scale=1):
                    upload_box = gr.Image(label="Upload Image", type="pil", height=400,width=500)
                    upload_button = gr.Button("Upload")
                with gr.Column(scale=1):
                    prompt_input = gr.Textbox(placeholder="Enter the prompt for image generation ...", label="Prompt")
                    generated_box = gr.Image(label="Generated Image", type="pil", height=300)
                    generate_button = gr.Button("Generate Image", variant="primary", size="sm")

            
            graph_output = gr.Plot(label="Analysis Graph")

    def update_chat(chatbox, message):                
        chatbox.append(("User", message))                
        response = chat_function(message)
        chatbox.append(("Bot", response))
        return chatbox

    def handle_image_generation(prompt):
        
        return generate_image(prompt)

    def handle_upload(image):
        return image

    chat_button.click(update_chat, [chatbox, chat_input], chatbox)
    generate_button.click(handle_image_generation, prompt_input, generated_box)
    upload_button.click(handle_upload, upload_box, upload_box)

demo.launch()
