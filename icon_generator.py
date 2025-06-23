from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

# Create directory if it doesn't exist
output_dir = "/Users/studio/work/github/handson-pearl-qr/voice-memorial-qr/static"
os.makedirs(output_dir, exist_ok=True)

def create_gradient_background(size, color1, color2):
    """Create a linear gradient background"""
    # Convert hex colors to RGB
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    color1_rgb = hex_to_rgb(color1)
    color2_rgb = hex_to_rgb(color2)
    
    # Create array for the gradient
    width, height = size
    image = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Draw the gradient (top to bottom)
    for y in range(height):
        # Calculate the ratio of the current y-coordinate to the total height
        ratio = y / height
        
        # Interpolate between the two colors
        r = int(color1_rgb[0] * (1 - ratio) + color2_rgb[0] * ratio)
        g = int(color1_rgb[1] * (1 - ratio) + color2_rgb[1] * ratio)
        b = int(color1_rgb[2] * (1 - ratio) + color2_rgb[2] * ratio)
        
        # Draw a line of the calculated color
        draw.line([(0, y), (width, y)], fill=(r, g, b))
        
    return image

def create_icon(size, color1="#667eea", color2="#764ba2", emoji="🐚"):
    """Create an icon with a gradient background and emoji in the center"""
    # Create the gradient background
    icon = create_gradient_background((size, size), color1, color2)
    
    # Use a system font that should be available (fallback to default if not found)
    try:
        # For emoji rendering, use Apple Color Emoji on macOS
        font = ImageFont.truetype("AppleColorEmoji", size // 2)
    except IOError:
        # Fallback to a default font
        font = ImageFont.load_default()
    
    # Create a drawing context
    draw = ImageDraw.Draw(icon)
    
    # Calculate text size to center it
    # This is approximate as getting exact emoji dimensions can be tricky
    emoji_width = size // 2
    emoji_height = size // 2
    position = ((size - emoji_width) // 2, (size - emoji_height) // 2)
    
    # Draw the emoji
    draw.text(position, emoji, font=font, embedded_color=True)
    
    return icon

# Generate icons
sizes = [192, 512]
for size in sizes:
    icon = create_icon(size)
    icon_path = os.path.join(output_dir, f"icon-{size}.png")
    icon.save(icon_path)
    print(f"Created {icon_path}")

print("Icon generation complete!")