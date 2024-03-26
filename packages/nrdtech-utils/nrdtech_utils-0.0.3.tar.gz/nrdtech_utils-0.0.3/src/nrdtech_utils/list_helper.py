import csv
import io


def convert_list_to_csv(data: list) -> bytes:
    """Convert a list to a CSV file handling quotes and special characters correctly

    :param data: list of data that will be converted to CSV
    :return: CSV string in bytes
    """
    data_with_converted_nulls = ["\\n" if a is None else a for a in data]
    output = io.StringIO()
    writer = csv.writer(output, delimiter=",", quoting=csv.QUOTE_MINIMAL)
    writer.writerow(data_with_converted_nulls)
    return bytes(output.getvalue().strip(), "utf-8")


def chunk_list(original_list: list, chunk_size: int) -> list:
    """Convert a list of elements to a list of lists where the maximum size of each inner list is chunk_size

    :param original_list: list of items to be chunked
    :param chunk_size: maximum size of each list chunk
    :return: list of lists that are no bigger than chunk_size
    """
    return [
        original_list[i : i + chunk_size]
        for i in range(0, len(original_list), chunk_size)
    ]
