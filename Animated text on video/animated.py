from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.video.fx.all import fadein, fadeout
from moviepy.video.fx import scroll

def generate_text_animation(text, duration, fontsize=70, color='white', position='center', fps=30, animation_style='none'):
    """
    Generate animated text clip with specified parameters and animation style.
    """
    text_clip = TextClip(text, fontsize=fontsize, color=color)
    
    if animation_style == 'scroll':
        text_clip = scroll(text_clip, wigglyness=3, x_speed=10)
    elif animation_style == 'fadein':
        text_clip = text_clip.fadein(1)
    elif animation_style == 'fadeout':
        text_clip = text_clip.fadeout(1)
    elif animation_style == 'move_left_to_right':
        text_clip = text_clip.set_position(lambda t: (200*t, 'center'), relative=True)
    
    text_clip = text_clip.set_position(position).set_duration(duration)
    return text_clip.set_fps(fps)



def inject_text_into_video(video_path, text_script, output_path):
    """
    Inject animated text into a video.
    """
    video_clip = VideoFileClip(video_path)
    clips = [video_clip]
    text_clips = []

    for text_item in text_script:
        text = text_item['text']
        start_time = text_item['start_time']
        duration = text_item['duration']
        animation_params = text_item.get('animation_params', {})
        text_clip = generate_text_animation(text, duration, **animation_params)
        text_clip = text_clip.set_start(start_time)
        text_clips.append(text_clip)

    for i in range(len(text_clips) - 1):
        text_clips[i] = fadeout(text_clips[i], duration=0.5).fadein(duration=0.5)

    final_clip = CompositeVideoClip(clips + text_clips)
    final_clip = final_clip.set_duration(video_clip.duration)
    final_clip.write_videofile(output_path, codec='libx264', fps=30)

if __name__ == "__main__":
    video_path = r"C:\Users\garvi\Desktop\Code\Heart Disease Prediction\Animated text on video\Recording 2024-04-01 212515.mp4"
    output_path = r"C:\Users\garvi\Desktop\Code\Heart Disease Prediction\Animated text on video\output.mp4"
    text_script = [
        {'text': "Watermark", 'start_time': 2, 'duration': 3, 'animation_params': {'fontsize': 20, 'color': 'white','animation_style':'fadein'}},
    ]
    inject_text_into_video(video_path, text_script, output_path)
