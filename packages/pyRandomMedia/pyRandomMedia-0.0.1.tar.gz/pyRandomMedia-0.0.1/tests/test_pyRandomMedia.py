import pytest
from src.pyRandomMedia.pyMediaFunctions import get_song
from src.pyRandomMedia.pyMediaFunctions import get_news
from src.pyRandomMedia.pyMediaFunctions import get_random_TV_show

class Tests:
    def test_sanity_check(self):
        expected = True  # the value we expect to be present
        actual = True  # the value we see in reality
        assert actual == expected, "Expected True to be equal to True!"
    
    #Tests for Song Function:
    def test_song_inputs(self):
        actual = get_song("Pop")[1]["genre"]
        assert "Pop" in actual, f"Expected the genre to contain the word Pop, but {actual} does not contain Pop."
        actual = get_song("Hip Hop", artist="Eminem")
        assert "Hip Hop" in actual[1]["genre"] and "Eminem" in actual[1]["artist"], f"Expected the genre string to contain Hip Hop and the artist string to contain Eminem, but {actual} does not fulfill these conditions."
        actual = get_song("Pop", song_name="Stressed")
        assert "Stressed" in actual[0] and "Pop" in actual[1]["genre"], f"Expected the name of the song to contain Stressed and the genre to contain Pop, but {actual} does not fulfill these conditions"

    def test_type_error(self):
        with pytest.raises(TypeError):
            get_song("Pop", release_date=2011)
    
    def test_song_not_found(self):
        actual = get_song("Grime")
        assert actual == "No songs found in our list", f"Expected to not find a song because there are no Grime songs in songs_file, but {actual} was found."
    
    #Tests for News Function:

    def test_newsValues(self):
        curr = get_news();
        for item in curr:
            assert isinstance(item, dict), "Each item in the array must be a dictionary"
            assert 'title' in item, "Each dictionary must have a 'title' key"
            assert 'link' in item, "Each dictionary must have a 'link' key"
            assert 'pubDate' in item, "Each dictionary must have a 'pubDate' key"
            assert 'url' in item["source"], "Each source must have a 'url' key"
            assert 'name' in item["source"], "Each source must have a 'name' key"

    def test_inTitle(self):
        inTitleString = "a"
        curr = get_news({ "inTitle": inTitleString })
        for item in curr:
            assert isinstance(item, dict), "Each item in the array must be a dictionary"
            assert 'title' in item, "Each dictionary in the array must have a 'title' key"
            assert isinstance(item['title'], str), "The 'title' key in each dictionary must be a string"
            assert inTitleString in item['title'], f"The substring '{inTitleString}' is not present in the title: {item['title']}"

    def test_maxNum(self):
        curr = get_news({ "num": 10 })
        assert len(curr) <= 10, "The number of articles should be less than or equal to num value"
    
    #Tests for TV show function

    def test_return_type(self):
        """Test if the return type of get_random_TV_show is a dictionary."""
        result = get_random_TV_show()
        assert isinstance(result, dict), "Expected result to be a dictionary."

    def test_dictionary_keys(self):
        """Test if the dictionary has the correct keys."""
        expected_keys = ['title', 'director', 'cast', 'release_year']
        result = get_random_TV_show()
        for key in expected_keys:
            assert key in result, f"Missing '{key}' in the result dictionary."

    def test_non_empty_values(self):
        """Test that the values for each key in the dictionary are not empty."""
        result = get_random_TV_show()
        for key, value in result.items():
            assert value, f"Expected '{key}' to have a non-empty value."


           

