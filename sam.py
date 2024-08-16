import gradio as gr
from hugchat import hugchat
from hugchat.login import Login

EMAIL = "sahilgowda204@gmail.com"
PASSWD = "Sahilgowda2004"
cookie_path_dir = "./cookies/"

sign = Login(EMAIL, PASSWD)
cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)
chatbot = hugchat.ChatBot(cookies=cookies.get_dict())

def progress_bar(progress):
    return f"""
    <div style="border: 1px solid #ccc; border-radius: 5px; padding: 2px; width: 100%; background-color: #f0f0f0;">
        <div style="width: {progress}%; background-color: #4caf50; height: 20px; border-radius: 5px;">
        </div>
    </div>
    <p style="text-align: center;">{progress}%</p>
    """

def chat_function(message):
    response = chatbot.chat(message).wait_until_done()
    return response

def generate_image(prompt):
    return "Image would be generated based on: " + prompt

def check_image_quality(image, quality_method):
    return f"Image quality check using {quality_method} would be performed here."

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    with gr.Row():
        with gr.Column(scale=1):
            gr.HTML("""
            <div style='border: 2px solid #4F46E5; background-color: #4F46E5; color: white; border-radius: 8px; padding: 10px;'>
                <h2 style='font-family: Arial, sans-serif;'>Chat Box</h2>
            </div>
            """)
            chatbox = gr.Chatbot(height=600)
            chat_input = gr.Textbox(show_label=False, placeholder="Type a message...")
            chat_button = gr.Button("Send")
        
        with gr.Column(scale=2):
            gr.HTML("""
            <div style='border: 2px solid #4F46E5; background-color: #4F46E5; color: white; border-radius: 8px; padding: 10px;'>
                <h2 style='font-family: Arial, sans-serif;'>Image Quality Assessment</h2>
            </div>
            """)
            
           
            gr.HTML("""
            <div style='border: 2px solid #4F46E5; background-color:#4F46E5; color: white; border-radius: 8px; padding: 10px; margin-bottom: 10px;'>
                <h3 style='font-family: Arial, sans-serif;'>TrCNN Score</h3>
            </div>
            """)
            gr.HTML(progress_bar(70))
            
            
            gr.HTML("""
            <div style='border: 2px solid #4F46E5; background-color: #4F46E5; color: white; border-radius: 8px; padding: 10px; margin-bottom: 10px;'>
                <h3 style='font-family: Arial, sans-serif;'>CNNIQA Score</h3>
            </div>
            """)
            gr.HTML(progress_bar(70))
            
           
            gr.HTML("""
            <div style='border: 2px solid #4F46E5; background-color: #4F46E5; color: white; border-radius: 8px; padding: 10px; margin-bottom: 10px;'>
                <h3 style='font-family: Arial, sans-serif;'>Our Model Score</h3>
            </div>
            """)
            gr.HTML(progress_bar(90))
           
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
