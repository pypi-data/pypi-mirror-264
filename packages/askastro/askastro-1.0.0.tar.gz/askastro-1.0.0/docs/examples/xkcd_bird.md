# xkcd bird classifier

[![](https://imgs.xkcd.com/comics/tasks.png)](https://xkcd.com/1425/)


!!! example "Is this a bird?"
    [![](https://images.unsplash.com/photo-1613891188927-14c2774fb8d7)](https://unsplash.com/photos/green-and-black-humming-bird-eLC1Bd3PLu4)
    ```python
    import astro

    photo = astro.beta.Image(
        "https://images.unsplash.com/photo-1613891188927-14c2774fb8d7",
    )

    result = astro.beta.classify(
        photo,
        labels=["bird", "not bird"]
    )
    ```

    !!! success "Yes!"
        ```python
        assert result == "bird"
        ```