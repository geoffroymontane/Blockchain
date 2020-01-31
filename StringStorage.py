# The text is to be stored in this string


author = ''
filename = ''
type = ''

def storeString1(inString):
    global author
    author = inString
    # Do something with the string
    print('Author is: ',author)
    return

def storeString2(inString):
    global filename
    filename = inString
    # Do something with the string
    print('filename is: ',filename)
    return

def storeString3(inString):
    global type
    type = inString
    # Do something with the string
    print('type is: ',type)
    return
