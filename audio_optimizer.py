#!/usr/bin/env python3
"""
Audio Optimizer for Pearl QR
Converts audio files to highly optimized Opus format for QR code embedding
"""

import os
import sys
import subprocess
import tempfile
import argparse
import base64
import uuid
from pathlib import Path


def check_ffmpeg():
    """Check if FFmpeg is available"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=10)
        return result.returncode == 0
    except Exception:
        return False


def optimize_audio(input_file, output_file=None, duration=1.2, volume_boost=15.0, bitrate=6, 
                  print_command=False, print_base64_size=True, play_result=False):
    """
    Optimize audio file for QR code embedding using Opus codec
    
    Args:
        input_file: Path to input audio file
        output_file: Path to output Opus file (default: auto-generated)
        duration: Duration in seconds to keep (default: 1.2)
        volume_boost: Volume multiplier (default: 15.0)
        bitrate: Target bitrate in kbps (default: 6)
        print_command: Whether to print the FFmpeg command
        print_base64_size: Whether to print the Base64 encoded size
        play_result: Whether to play the resulting file (requires ffplay)
    
    Returns:
        Path to the optimized file
    """
    if not check_ffmpeg():
        print("Error: FFmpeg is not available. Please install FFmpeg first.")
        return None
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        return None
    
    # Generate output filename if not provided
    if output_file is None:
        input_path = Path(input_file)
        unique_id = str(uuid.uuid4())[:8]
        output_file = f"{input_path.stem}_optimized_{unique_id}.opus"
    
    # Build FFmpeg command with optimal parameters
    cmd = [
        'ffmpeg', '-i', input_file,
        '-af', f'highpass=f=80,lowpass=f=8000,volume={volume_boost}',
        '-c:a', 'libopus',
        '-b:a', f'{bitrate}k',
        '-ac', '1',
        '-ar', '8000',
        '-application', 'voip',
        '-vbr', 'off',
        '-compression_level', '10',
        '-frame_duration', '60',
        '-packet_loss', '0',
        '-t', str(duration),
        '-y', output_file
    ]
    
    if print_command:
        print("FFmpeg command:")
        print(" ".join(cmd))
    
    # Run FFmpeg command
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            print(f"Error: FFmpeg failed with code {result.returncode}")
            print(f"Error message: {result.stderr}")
            return None
        
        # Print file size and stats
        file_size = os.path.getsize(output_file)
        print(f"Optimized file saved to: {output_file}")
        print(f"File size: {file_size} bytes ({file_size/1024:.2f} KB)")
        
        # Calculate and print Base64 size for QR code embedding
        if print_base64_size:
            with open(output_file, 'rb') as f:
                audio_bytes = f.read()
            
            # Calculate Base64 encoded size
            base64_str = base64.b64encode(audio_bytes).decode('utf-8')
            base64_size = len(base64_str)
            
            # Calculate data URI size (for QR code embedding)
            data_uri = f"data:audio/ogg;codecs=opus;base64,{base64_str}"
            data_uri_size = len(data_uri)
            
            print(f"Base64 size: {base64_size} bytes ({base64_size/1024:.2f} KB)")
            print(f"Data URI size: {data_uri_size} bytes ({data_uri_size/1024:.2f} KB)")
            
            # Check if it will fit in a QR code
            qr_level40_capacity = 7089  # characters for QR Level 40
            if data_uri_size <= qr_level40_capacity:
                print(f"✅ Will fit in QR Level 40 (capacity: {qr_level40_capacity} characters)")
                print(f"   Used: {data_uri_size} characters ({data_uri_size/qr_level40_capacity*100:.1f}% of capacity)")
            else:
                print(f"❌ Too large for QR Level 40 (capacity: {qr_level40_capacity} characters)")
                print(f"   Exceeds by: {data_uri_size - qr_level40_capacity} characters")
                print(f"   Try reducing duration to {duration * qr_level40_capacity / data_uri_size:.1f} seconds")
        
        # Play the resulting file if requested
        if play_result:
            print("Playing optimized file...")
            subprocess.run(['ffplay', '-nodisp', '-autoexit', output_file], capture_output=True)
        
        return output_file
        
    except subprocess.TimeoutExpired:
        print("Error: FFmpeg command timed out")
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None


def main():
    """Main function to parse arguments and run optimization"""
    parser = argparse.ArgumentParser(description="Optimize audio files for QR code embedding")
    parser.add_argument("input", help="Input audio file path")
    parser.add_argument("-o", "--output", help="Output Opus file path (default: auto-generated)")
    parser.add_argument("-d", "--duration", type=float, default=1.2, 
                      help="Duration to keep in seconds (default: 1.2)")
    parser.add_argument("-v", "--volume", type=float, default=15.0, 
                      help="Volume boost multiplier (default: 15.0)")
    parser.add_argument("-b", "--bitrate", type=int, default=6, 
                      help="Target bitrate in kbps (default: 6)")
    parser.add_argument("-c", "--command", action="store_true", 
                      help="Print FFmpeg command")
    parser.add_argument("-p", "--play", action="store_true", 
                      help="Play the resulting file")
    
    args = parser.parse_args()
    
    optimize_audio(
        args.input, 
        args.output, 
        args.duration, 
        args.volume, 
        args.bitrate,
        args.command,
        True,
        args.play
    )


if __name__ == "__main__":
    main()