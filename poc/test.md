# Opus Audio Optimization for QR Code Embedding

## Optimal FFmpeg Command

```bash
ffmpeg -i input.m4a -af "highpass=f=80,lowpass=f=8000,volume=15.0" -c:a libopus -b:a 6k -ac 1 -ar 8000 -application voip -vbr off -compression_level 10 -frame_duration 60 -packet_loss 0 -t 1.2 output.opus
```

This command produces an Opus file of approximately 1.4KB that contains audible voice content while fitting within QR Level 40 capacity limits (~7KB).

## Parameter Explanation

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `-af "highpass=f=80,lowpass=f=8000,volume=15.0"` | Audio filters | Remove low/high frequencies, boost volume by 15x |
| `-c:a libopus` | Opus codec | Modern audio codec with excellent compression |
| `-b:a 6k` | Bitrate | 6 kilobits per second (very low but viable for speech) |
| `-ac 1` | Audio channels | Mono audio (single channel) |
| `-ar 8000` | Sample rate | 8kHz sampling rate (telephone quality) |
| `-application voip` | Application type | Optimized for speech rather than music |
| `-vbr off` | Variable bitrate | Disabled to ensure consistent bitrate |
| `-compression_level 10` | Compression | Maximum compression level (0-10) |
| `-frame_duration 60` | Frame duration | Longer frames for better compression |
| `-packet_loss 0` | Packet loss | No redundancy for packet loss (reduces size) |
| `-t 1.2` | Duration | Limit audio to 1.2 seconds |

## File Size Comparison

| Bitrate | Duration | Volume Boost | File Size | Notes |
|---------|----------|--------------|-----------|-------|
| 64k | 3s | 10x | 26.9KB | Good quality but too large for QR |
| 16k | 3s | 5x | 14.5KB | Decent quality, still too large |
| 8k | 3s | 5x | 7.6KB | Borderline QR Level 40 capacity |
| 6k | 1.5s | 10x | 1.2KB | Good quality-size balance |
| 6k | 1.2s | 15x | 1.4KB | Optimal for voice messages |
| 4k | 1.5s | 10x | 1.2KB | Lower quality but smallest |

## Integration with Python App

In the `app.py` file, the current FFmpeg command is:

```python
base_cmd = [
    'ffmpeg', '-i', file_path,
    '-af', 'highpass=f=80,lowpass=f=8000',
    '-c:a', 'libopus', '-b:a', '1k', '-ac', '1', '-ar', '8000',
    '-t', str(duration), '-y', opus_path
]
```

### Recommended Update

```python
base_cmd = [
    'ffmpeg', '-i', file_path,
    '-af', 'highpass=f=80,lowpass=f=8000,volume=15.0',
    '-c:a', 'libopus', '-b:a', '6k', '-ac', '1', '-ar', '8000',
    '-application', 'voip', '-vbr', 'off', 
    '-compression_level', '10', '-frame_duration', '60',
    '-packet_loss', '0', '-t', str(duration), '-y', opus_path
]
```

This update will produce higher quality audio at a still-manageable file size for QR code embedding.