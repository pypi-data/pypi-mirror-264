import pytest
from pyrandom2pm import pyrandom2pm
class Tests:
    @pytest.fixture
    def example_fixture(self):
        yield
    def test_sanity_check(self):
        # Making a test that always passes to make sure that there is no problem with pytest.
        expected = True
        actual = True
        assert expected == actual, "Expected True to be equal to True."
    # run multiple different test cases
    #@pytest.mark.parametrize("num_dice, num_sides", [(1, 6), (2, 6)])
    def test_randomDice_valid_input(self):
        num_dice = 2
        num_sides = 6
        result = pyrandom2pm.randomDice(num_dice, num_sides)  # Call the function with the correct parameters
        assert isinstance(result, int)
        assert 1 <= result <= num_dice * num_sides
    # def test_numDice(self):
    #     with pytest.raises(ValueError):
    #         randomDice.randomDice(None, None)
    #     with pytest.raises(ValueError):
    #         randomDice.randomDice(1, None)
    #     with pytest.raises(ValueError):
    #         randomDice.randomDice(None, 6)
    def test_randomDice_value_invalid(self):
        with pytest.raises(ValueError):
            pyrandom2pm.randomDice(0, 6)  # Should raise ValueError for num_dice = 0
        with pytest.raises(ValueError):
            pyrandom2pm.randomDice(3, 6)  # Should raise ValueError for num_dice > 2
        with pytest.raises(ValueError): # Should raise ValueError when all parameters are zero
            pyrandom2pm.randomDice(0, 0)
        with pytest.raises(ValueError):# Should raise ValueError for num_dice ==0
            pyrandom2pm.randomDice(1, 0)
    def test_randomDice_invalid_type(self):
        with pytest.raises(TypeError): # Should raise TypeError when any or both of the parameter are not integer
            pyrandom2pm.randomDice("Hello", "World")
        with pytest.raises(TypeError): # Should raise TypeError when any or both of the parameter are not integer
            pyrandom2pm.randomDice("Hello", 3)
        with pytest.raises(TypeError): # Should raise TypeError when any or both of the parameter are not integer
            pyrandom2pm.randomDice(1, "World")
        with pytest.raises(TypeError): # Should raise TypeError when any or both of the parameter are not integer
            pyrandom2pm.randomDice(248.88, 289.999)
        with pytest.raises(TypeError): # Should raise TypeError when any or both of the parameter are not integer
            pyrandom2pm.randomDice(248.88, 3)
        with pytest.raises(TypeError): # Should raise TypeError when any or both of the parameter are not integer
            pyrandom2pm.randomDice(1, 232434.2323)

        

        
    def test_randomNum_valid_input(self):
        num1 = -100
        num2 = 400
        result = pyrandom2pm.randomNum(num1,num2)  # Call the function with the correct parameters
        assert isinstance(result, int)
        assert num1 <= result <= num2
    def test_randomNum_value_invalid(self):
        with pytest.raises(ValueError):
            pyrandom2pm.randomNum(-1, -6) 
        with pytest.raises(ValueError):
            pyrandom2pm.randomNum(100, 0)  # Should raise ValueError for num = 0
    def test_randomNum_type_invalid(self):
        with pytest.raises(TypeError):
            pyrandom2pm.randomNum("Hello")  # Should raise TypeError for the input being string
        with pytest.raises(TypeError):
            pyrandom2pm.randomNum(248.888)  # Should raise TypeError for the input being float
    def test_randomCoin_valid_input(self):
        num_flip = 255
        result = pyrandom2pm.randomCoin(num_flip)  # Call the function with the correct parameters
        assert isinstance(result, str)
        assert result is not None
    def test_randomCoin_invalid_value_input(self):
        with pytest.raises(ValueError):
            pyrandom2pm.randomCoin(0)  # Should raise ValueError for num_flip = 0
        with pytest.raises(ValueError):
            pyrandom2pm.randomCoin(-200)  # Should raise ValueError for num_flip <0
    def test_randomCoin_invalid_type_input(self):
        with pytest.raises(TypeError):
            pyrandom2pm.randomCoin("Hello")  # Should raise TypeError for the input being string
        with pytest.raises(TypeError):
            pyrandom2pm.randomCoin(23.333)  # Should raise TypeError for the input being float
    
    def test_random8ball_valid_input(self):
        strn = "Hello, World?"
        result = pyrandom2pm.random8ball(strn)  # Call the function with the correct parameters
        assert isinstance(result, str)
        assert result is not None
    def test_random8ball_nonquestion_input(self):
        strn = "Hello, World"
        result = pyrandom2pm.random8ball(strn)  # Call the function with the correct parameters
        assert result ==  "That was not a question"
    def test_random8ball_invalid_input(self):
        with pytest.raises(TypeError):
             pyrandom2pm.random8ball(0)  # Should raise TypeError when the input is not a string
        with pytest.raises(TypeError):
             pyrandom2pm.random8ball(248.88)  # Should raise TypeError when the input is not a string