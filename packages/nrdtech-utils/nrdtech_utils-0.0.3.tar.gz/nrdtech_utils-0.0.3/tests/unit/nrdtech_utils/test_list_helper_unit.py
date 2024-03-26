from nrdtech_utils import list_helper


def test_convert_list_to_csv():
    input_ = [1, "hello world", 7.5, None, "okay"]
    expected_output = b"1,hello world,7.5,\\n,okay"
    output = list_helper.convert_list_to_csv(input_)
    assert output == expected_output


def test_chunk_list():
    input_ = [1, 2, 3, 4, 5]
    expected_output = [[1, 2], [3, 4], [5]]
    output = list_helper.chunk_list(input_, 2)
    assert output == expected_output
