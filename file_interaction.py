def append_to_file(file_name, text_to_append):
    """Append the given text as a new line at the end of file"""
    with open(file_name, "a") as file_object:
        file_object.write(text_to_append + "\n")