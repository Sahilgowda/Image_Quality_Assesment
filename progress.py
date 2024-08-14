import gradio as gr

with gr.Blocks() as demo:
    cart = gr.State([])

    cart_size = gr.Number(label="Cart Size")
    gr.Button("Get Cart Size").click(lambda cart: len(cart), cart, cart_size)

demo.launch()