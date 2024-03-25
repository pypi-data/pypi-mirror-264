# Hogwarts sorting hat

![](hogwarts_patch.webp){width="400"}


!!! example "Hogwarts sorting hat"
    ```python
    import astro

    student = "Brave, daring, chivalrous, and sometimes a bit reckless."

    house = astro.classify(
        student,
        labels=["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]
    )
    ```

    !!! success "Welcome to Gryffindor!"
        ```python
        assert house == "Gryffindor"
        ```