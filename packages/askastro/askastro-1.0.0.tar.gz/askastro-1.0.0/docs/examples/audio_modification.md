# Modifying user audio

By combining a few Astro tools, you can quickly record a user, transcribe their speech, modify it, and play it back.

!!! info "Audio extra"
    This example requires the `audio` extra to be installed in order to record and play sound:

    ```bash
    pip install askastro[audio]
    ```


!!! example "Modifying user audio"
    ```python
    import astro
    import astro.audio

    # record the user
    user_audio = astro.audio.record_phrase()

    # transcribe the text
    user_text = astro.transcribe(user_audio)

    # cast the language to a more formal style
    ai_text = astro.cast(
        user_text, 
        instructions="Make the language ridiculously formal",
    )

    # generate AI speech
    ai_audio = astro.speak(ai_text)

    # play the result
    ai_audio.play()
    ```

    !!! quote "User audio"
        "This is a test."
        
        <audio controls>
            <source src="/assets/audio/this_is_a_test.mp3" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
        

    !!! success "Astro audio"
        "This constitutes an examination."
        
        <audio controls>
            <source src="/assets/audio/this_is_a_test_2.mp3" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
