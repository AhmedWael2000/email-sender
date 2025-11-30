"""
Improved script to create a Windows-compatible ICO file with proper format
"""
from PIL import Image
import os

def create_windows_ico(input_png, output_ico):
    """
    Create a proper Windows ICO file from PNG
    Windows ICO files need specific size layers for best compatibility
    """
    try:
        print(f"📂 Loading image: {input_png}")
        img = Image.open(input_png)
        
        # Convert to RGBA if needed
        if img.mode != 'RGBA':
            print(f"   Converting from {img.mode} to RGBA...")
            img = img.convert('RGBA')
        
        print(f"   Original size: {img.size}")
        
        # Windows standard icon sizes
        # 256x256 is the max for Windows ICO format (not 512)
        icon_sizes = [
            (16, 16),    # Small icons in lists
            (24, 24),    # Small toolbar icons  
            (32, 32),    # Standard small icon
            (48, 48),    # Standard medium icon
            (64, 64),    # Large icon
            (128, 128),  # Extra large icon
            (256, 256),  # Jumbo icon (Vista+)
        ]
        
        print(f"\n🔄 Creating icon layers...")
        icon_images = []
        
        for size in icon_sizes:
            print(f"   Creating {size[0]}x{size[1]} layer...")
            # Use high-quality LANCZOS resampling
            resized = img.resize(size, Image.Resampling.LANCZOS)
            icon_images.append(resized)
        
        # Save as ICO with all size layers
        print(f"\n💾 Saving to: {output_ico}")
        icon_images[0].save(
            output_ico,
            format='ICO',
            sizes=[(img.width, img.height) for img in icon_images]
        )
        
        # Verify the file was created
        if os.path.exists(output_ico):
            file_size = os.path.getsize(output_ico)
            print(f"\n✅ Icon created successfully!")
            print(f"   File: {output_ico}")
            print(f"   Size: {file_size:,} bytes")
            print(f"   Layers: {len(icon_sizes)} sizes")
            print(f"   Sizes: {', '.join([f'{s[0]}x{s[1]}' for s in icon_sizes])}")
            return True
        else:
            print(f"\n❌ Error: Icon file was not created!")
            return False
        
    except Exception as e:
        print(f"\n❌ Error creating icon: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Windows ICO Creator")
    print("=" * 60)
    print()
    
    input_file = "email_icon.png"
    output_file = "email_icon.ico"
    
    success = create_windows_ico(input_file, output_file)
    
    if success:
        print(f"\n{'=' * 60}")
        print("✅ DONE! You can now use email_icon.ico with PyInstaller")
        print("=" * 60)
    else:
        print(f"\n{'=' * 60}")
        print("❌ FAILED! Please check the error above")
        print("=" * 60)
