from flask import Flask
import subprocess

app = Flask(__name__)

# The RTSP stream URL and the Mux RTMP ingest URL and Stream Key
RTSP_STREAM_URL = "http://192.168.8.41/mjpeg/1"
MUX_RTMP_URL = "rtmp://global-live.mux.com:5222/app/9c908ef6-fb4d-8f0e-200d-48ec2b6e1f19"

@app.route('/start-stream', methods=['GET'])
def start_stream():
    # Construct the FFmpeg command
    ffmpeg_command = [
        'ffmpeg',
        '-i', RTSP_STREAM_URL,       # Input RTSP stream URL
        '-f', 'flv',                 # Output format (FLV for Mux)
        MUX_RTMP_URL                # Mux RTMP URL (your stream key)
    ]

    try:
        # Start the FFmpeg process
        subprocess.Popen(ffmpeg_command)
        return "Streaming started successfully!", 200
    except Exception as e:
        return f"Error occurred: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
