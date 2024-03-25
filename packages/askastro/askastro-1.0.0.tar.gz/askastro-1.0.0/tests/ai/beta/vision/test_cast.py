import astro
import pytest
from pydantic import BaseModel, Field


class Location(BaseModel):
    city: str
    state: str = Field(description="The two letter abbreviation")


@pytest.mark.flaky(max_runs=3)
class TestVisionCast:
    def test_cast_ny(self):
        img = astro.beta.Image(
            "https://images.unsplash.com/photo-1568515387631-8b650bbcdb90"
        )
        result = astro.beta.cast(img, target=Location)
        assert result in (
            Location(city="New York", state="NY"),
            Location(city="New York City", state="NY"),
        )

    def test_cast_dc(self):
        img = astro.beta.Image(
            "https://images.unsplash.com/photo-1617581629397-a72507c3de9e"
        )
        result = astro.beta.cast(img, target=Location)
        assert result in (
            Location(city="Washington", state="DC"),
            Location(city="Washington", state="D.C."),
        )

    def test_cast_ny_images_input(self):
        img = astro.beta.Image(
            "https://images.unsplash.com/photo-1568515387631-8b650bbcdb90"
        )
        result = astro.beta.cast(data=None, images=[img], target=Location)
        assert result in (
            Location(city="New York", state="NY"),
            Location(city="New York City", state="NY"),
        )

    def test_cast_ny_image_input(self):
        img = astro.beta.Image(
            "https://images.unsplash.com/photo-1568515387631-8b650bbcdb90"
        )
        result = astro.beta.cast(data=img, target=Location)
        assert result in (
            Location(city="New York", state="NY"),
            Location(city="New York City", state="NY"),
        )

    def test_cast_ny_image_and_text(self):
        img = astro.beta.Image(
            "https://images.unsplash.com/photo-1568515387631-8b650bbcdb90"
        )
        result = astro.beta.cast(
            data="I see the empire state building",
            images=[img],
            target=Location,
        )
        assert result in (
            Location(city="New York", state="NY"),
            Location(city="New York City", state="NY"),
        )

    def test_cast_book(self):
        class Book(BaseModel):
            title: str
            subtitle: str
            authors: list[str]

        img = astro.beta.Image(
            "https://hastie.su.domains/ElemStatLearn/CoverII_small.jpg"
        )
        result = astro.beta.cast(img, target=Book)
        assert result == Book(
            title="The Elements of Statistical Learning",
            subtitle="Data Mining, Inference, and Prediction",
            authors=["Trevor Hastie", "Robert Tibshirani", "Jerome Friedman"],
        )


class TestAsync:
    async def test_cast_ny(self):
        img = astro.beta.Image(
            "https://images.unsplash.com/photo-1568515387631-8b650bbcdb90"
        )
        result = await astro.beta.cast_async(img, target=Location)
        assert result in (
            Location(city="New York", state="NY"),
            Location(city="New York City", state="NY"),
        )


class TestMapping:
    def test_map(self):
        ny = astro.beta.Image(
            "https://images.unsplash.com/photo-1568515387631-8b650bbcdb90"
        )
        dc = astro.beta.Image(
            "https://images.unsplash.com/photo-1617581629397-a72507c3de9e"
        )
        result = astro.beta.cast.map([ny, dc], target=Location)
        assert isinstance(result, list)
        assert result[0] in (
            Location(city="New York", state="NY"),
            Location(city="New York City", state="NY"),
        )
        assert result[1] in (
            Location(city="Washington", state="DC"),
            Location(city="Washington", state="D.C."),
        )

    @pytest.mark.flaky(reruns=3)
    async def test_async_map(self):
        ny = astro.beta.Image(
            "https://images.unsplash.com/photo-1568515387631-8b650bbcdb90"
        )
        dc = astro.beta.Image(
            "https://images.unsplash.com/photo-1617581629397-a72507c3de9e"
        )
        result = await astro.beta.cast_async.map([ny, dc], target=Location)
        assert isinstance(result, list)
        assert result[0] in (
            Location(city="New York", state="NY"),
            Location(city="New York City", state="NY"),
        )
        assert result[1] in (
            Location(city="Washington", state="DC"),
            Location(city="Washington", state="D.C."),
        )
