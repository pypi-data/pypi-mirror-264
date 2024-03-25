# Recording video

Astro has utilities for working with video data beyond generating speech and transcription. To use these utilities, you must install Astro with the `video` extra:

```bash
pip install askastro[video]
```

## Recording video

Astro can record video from your computer's camera. The result is a stream of `Image` objects, which can be used any of Astro's image tools, including captioning, classification, and more.

### Recording continuously

The `record_background` function records video continuously in the background. This is useful for recording video while doing other tasks or processing the data in real time.

The result of `record_background` is a `BackgroundVideoRecorder` object, which can be used to control the recording (including stopping it) and to access the recorded video as a stream of images. Images are queued and can be accessed by iterating over the recorder's `stream` method.

```python
import astro
import astro.video

recorder = astro.video.record_background()

counter = 0
for image in recorder.stream():
    counter += 1
    # process each image
    astro.beta.caption(image)

    # stop recording
    if counter == 3:
        recorder.stop()
```