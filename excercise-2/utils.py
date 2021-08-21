
def textfile_to_list(textfile:str) -> list:
    
    with open(textfile, 'r') as open_file:
        content = open_file.read()
    
    ls_line_content = content.split('/n')

    return ls_line_content