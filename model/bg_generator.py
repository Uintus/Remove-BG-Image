from model_loader.generator_bg_loader import pipe

def generate_bg(elements, style, preferred_colors):
    
    prompt = f"Create a high-quality background image featuring the following elements: {elements}. The image should have a {style} style, with a color palette of {preferred_colors}. Ensure a visually appealing composition that is not too cluttered, making it suitable as a background."

   
    return pipe(prompt=prompt).images[0] 

# print(torch.cuda.is_available())
