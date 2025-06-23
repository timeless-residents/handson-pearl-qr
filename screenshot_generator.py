from PIL import Image, ImageDraw, ImageFont
import io

# Create a 1080x1920 image with a gradient background
def create_screenshot():
    # Set dimensions
    width, height = 1080, 1920
    
    # Create a new image with white background
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Create gradient background (purple to light blue)
    for y in range(height):
        r = int(100 + (150 - 100) * y / height)  # 100 to 150
        g = int(50 + (200 - 50) * y / height)    # 50 to 200
        b = int(200 + (255 - 200) * y / height)  # 200 to 255
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Draw header area
    draw.rectangle([(0, 0), (width, 120)], fill=(40, 40, 80, 180))
    
    # Draw app title
    title_font_size = 60
    try:
        title_font = ImageFont.truetype("Arial", title_font_size)
    except IOError:
        title_font = ImageFont.load_default()
    
    draw.text((width//2, 70), "Pearl Memorial QR", fill=(255, 255, 255), 
              font=title_font, anchor="mm")
    
    # Draw a QR code placeholder
    qr_size = 500
    qr_top = 300
    draw.rectangle(
        [(width//2 - qr_size//2, qr_top), 
         (width//2 + qr_size//2, qr_top + qr_size)], 
        outline=(0, 0, 0), width=10, fill=(255, 255, 255))
    
    # Draw QR code internal pattern
    pattern_size = 100
    positions = [(width//2 - qr_size//4, qr_top + qr_size//4),
                (width//2 + qr_size//4, qr_top + qr_size//4),
                (width//2 - qr_size//4, qr_top + 3*qr_size//4)]
    
    for pos in positions:
        draw.rectangle(
            [(pos[0] - pattern_size//2, pos[1] - pattern_size//2),
             (pos[0] + pattern_size//2, pos[1] + pattern_size//2)],
            fill=(0, 0, 0))
        draw.rectangle(
            [(pos[0] - pattern_size//2 + 20, pos[1] - pattern_size//2 + 20),
             (pos[0] + pattern_size//2 - 20, pos[1] + pattern_size//2 - 20)],
            fill=(255, 255, 255))
    
    # Add some dots to make it look like a QR code
    dot_size = 20
    for x in range(10):
        for y in range(10):
            if (x + y) % 3 == 0 and x > 2 and y > 2:
                pos_x = width//2 - qr_size//2 + x * (qr_size // 10)
                pos_y = qr_top + y * (qr_size // 10)
                draw.rectangle([(pos_x, pos_y), (pos_x + dot_size, pos_y + dot_size)], fill=(0, 0, 0))
    
    # Draw text under QR code
    text_font_size = 40
    try:
        text_font = ImageFont.truetype("Arial", text_font_size)
    except IOError:
        text_font = ImageFont.load_default()
    
    draw.text((width//2, qr_top + qr_size + 100), "Scan to remember", 
              fill=(40, 40, 80), font=text_font, anchor="mm")
    
    # Add action buttons
    button_width, button_height = 300, 80
    button_y = qr_top + qr_size + 200
    
    # Record button
    draw.rounded_rectangle(
        [(width//2 - button_width - 20, button_y),
         (width//2 - 20, button_y + button_height)],
        radius=10, fill=(60, 100, 220))
    draw.text((width//2 - button_width//2 - 20, button_y + button_height//2), 
              "Record", fill=(255, 255, 255), font=text_font, anchor="mm")
    
    # Play button
    draw.rounded_rectangle(
        [(width//2 + 20, button_y),
         (width//2 + button_width + 20, button_y + button_height)],
        radius=10, fill=(60, 180, 120))
    draw.text((width//2 + button_width//2 + 20, button_y + button_height//2), 
              "Play", fill=(255, 255, 255), font=text_font, anchor="mm")
    
    # Add bottom navigation bar
    draw.rectangle([(0, height - 120), (width, height)], fill=(40, 40, 80))
    
    # Navigation icons
    icon_positions = [(width//4, height - 60),
                     (width//2, height - 60),
                     (3*width//4, height - 60)]
    icon_labels = ["Home", "Scan", "Settings"]
    
    for i, (pos, label) in enumerate(zip(icon_positions, icon_labels)):
        draw.ellipse([(pos[0] - 30, pos[1] - 30), (pos[0] + 30, pos[1] + 30)], 
                    fill=(255, 255, 255, 180))
        draw.text((pos[0], pos[1] + 50), label, fill=(255, 255, 255), 
                font=text_font, anchor="mm")
    
    # Save the image
    target_path = "/Users/studio/work/github/handson-pearl-qr/voice-memorial-qr/static/screenshot1.webp"
    img.save(target_path, format="WEBP", quality=90)
    print(f"Screenshot saved to {target_path}")

if __name__ == "__main__":
    create_screenshot()