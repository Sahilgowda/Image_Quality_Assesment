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
    # Placeholder function for image generation
    return "Image would be generated based on: " + prompt

def check_image_quality(image, quality_method):
    # Placeholder function for image quality check
    return f"Image quality check using {quality_method} would be performed here."

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    with gr.Row():
        
        with gr.Column(scale=1):
            gr.Markdown("## Chat Box")
            chatbox = gr.Chatbot(height=600)
            chat_input = gr.Textbox(show_label=False, placeholder="Type a message...")
            chat_button = gr.Button("Send")
        
        
        with gr.Column(scale=2):
            gr.Markdown("## Image Quality Assessment")
           
            with gr.Row():
                with gr.Column(scale=1):
                    upload_box = gr.Image(label="Upload Image", type="pil", height=420, width=500)
                    with gr.Row():
                        upload_button = gr.Button("Upload")
                        check_upload_quality_button = gr.Button("Check Quality")
                    upload_quality_dropdown = gr.Dropdown(
                        choices=["CNNIQA", "HIQA", "Prompt Similarity", "Our Model"],
                        label="Select Quality Check Method",
                        visible=False
                    )
                with gr.Column(scale=1):
                    prompt_input = gr.Textbox(placeholder="Enter the prompt for image generation ...", label="Prompt")
                    generated_box = gr.Image(label="Generated Image", type="pil", height=300)
                    with gr.Row():
                        generate_button = gr.Button("Generate Image")
                        check_generated_quality_button = gr.Button("Check Quality")
                    generated_quality_dropdown = gr.Dropdown(
                        choices=["CNNIQA", "HIQA", "Prompt Similarity", "Our Model"],
                        label="Select Quality Check Method",
                        visible=False
                    )
            
           
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

    def show_quality_dropdown(dropdown):
        return gr.update(visible=True)

    def perform_quality_check(image, method):
        result = check_image_quality(image, method)
        return result

    chat_button.click(update_chat, [chatbox, chat_input], chatbox)
    generate_button.click(handle_image_generation, prompt_input, generated_box)
    upload_button.click(handle_upload, upload_box, upload_box)

    check_upload_quality_button.click(show_quality_dropdown, None, upload_quality_dropdown)
    check_generated_quality_button.click(show_quality_dropdown, None, generated_quality_dropdown)

    upload_quality_dropdown.change(perform_quality_check, [upload_box, upload_quality_dropdown], chatbox)
    generated_quality_dropdown.change(perform_quality_check, [generated_box, generated_quality_dropdown], chatbox)

demo.launch()
