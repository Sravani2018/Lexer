id_map     = {}

keywords = ["int", "float", "while", "until", "string", "if", "else", "boolean", "true", "false", "for", "printf", "struct", "return"]

operators  = ["+", "-", "*", "/", "%", "=", "equals", ">", "<", "and", "or", "not", "?", ":"]
delimiters = ["{", "}", "(", ")", "[", "]", ";"," "]
comments = ['#']
valid_delim = ['{', '(', '[', '+']

prev_op_delim = False

def is_comments(token):
    if token in comments:
        return True
    else:
        return False

def is_keyword(token):
    if token in keywords:
        return True
    else:
        return False

def is_delimiter(token):
    if token in delimiters:
        return True
    else:
        return False
    
def is_operator(token):
    if token in operators:
        return True
    else:
        return False
def is_int(token):
    try:
        if str(type(int(token))) == "<class 'int'>":
            return True
        else:
            return False
    except:
        return False
def is_float(token):
    try:
        if str(type(float(token))) == "<class 'float'>":
            return True
        else:
            return False
    except:
        return False 
def handel_token(token):
    global f_out
    global line
    f_out.write("HANDELING", token)
    find_type(token)
    for i, tok in enumerate(token):
        #tok = line[lb+i]
        if is_operator(tok):
            left_part, right_part = line[lb:lb+i], line[lb+i+1:]
            find_type(left_part)
            f_out.write("\nToken: '{}' is an operator".format(tok))
            handel_token(right_part)
def is_keyword(token):
    if token in keywords:
        return True
    else:
        return False

def is_ident(token):
    for i, char in enumerate(token):
        if i == 0 and not char.isalpha():
            return False
        if (not char.isalpha()) and (not char.isdigit()):
            return False
    return True
def is_valid(char):
    if char in delimiters or char in operators or char in comments or char.isalpha() or char.isdigit() or char == '.':
        return True
    return False
def is_ascii(s):
    return all(ord(c) < 128 for c in s)

xab = 0
for i in keywords:
    id_map[i] = xab
    xab+=1
for i in operators:
    id_map[i] = xab
    xab+=1
for i in delimiters:
    id_map[i] = xab
    xab+=1
for i in comments:
    id_map[i] = xab
    xab+=1
id_map["ident"] = xab
id_map["int"] = xab+1
id_map["float"] = xab+2
id_map["string"] = xab+3

def find_type(token):
    global f_out
    global line
    if len(token)==0:
        return 
    global lb
    global fp
    global prev_op_delim
    if is_operator(token):
        prev_op_delim = True
        f_out.write("\nLexeme: '{}'\t is an operator\t Token: {}".format(token, id_map[token]))
        lb = fp+1
        return
    elif is_delimiter(token):
        if token in valid_delim:
            prev_op_delim = True
        f_out.write("\nLexeme: '{}'\t is a Delimiter\t Token: {}".format(token, id_map[token]))
        lb = fp+1
        return
    elif is_keyword(token):
        prev_op_delim = False
        f_out.write("\nLexeme: '{}'\t is a keyword\t Token: {}".format(token, id_map[token]))
        lb = fp+1
        return 
    elif is_int(token):
        prev_op_delim = False
        f_out.write("\nLexeme: '{}'\t is an int\t Token: {}".format(token, id_map["int"]))
        lb = fp+1
        return
    elif is_float(token):
        prev_op_delim = False
        f_out.write("\nLexeme: '{}'\t is a float\t Token: {}".format(token, id_map["float"]))
        lb = fp+1
        return
    elif token[0] == '#':
        prev_op_delim = False
        f_out.write("\nLexeme: '{}'\t is a Comment\t Token: {}".format(line[fp:], id_map[token[0]]))
        return
    elif is_ident(token):
        prev_op_delim = False
        f_out.write("\nLexeme: '{}'\t is an Identifi\t Token: {}".format(token, id_map["ident"]))
        lb = fp+1
        return
    elif token[0] == '"':
        prev_op_delim = False
        f_out.write("\nLexeme: '{}'\t is a string\t Token: {}".format(token, id_map["string"]))
        lb = fp+1
        return
    else:
        prev_op_delim = False
        f_out.write("\nLexeme: '{}'\t is unidentified".format(token))
        #handel(token)
        

lb, fp = 0, 0
is_string = False
string = ""
def handle(debugging=False):
    global f_out
    global line
    global lb
    global fp
    global prev_op_delim
    global is_string
    global string
    global lin
    global line_no
    global length
    lb, fp = 0, 0
    for fp, char in enumerate(line):
    
        if is_string:
            if not is_ascii(char):
                f_out.write("\nCharacter: '{}'\tat pos:'{}'\t is invalid".format(char, fp))
            string += char
            if fp == len(line)-1 and char != '"':
                if line_no == length:
                    f_out.write("\nString: '{}' is not closed".format(string))
                string += '\\n'
            if char == '"':
                is_string = False
                if is_ascii(string):
                    find_type(string, f_out)
                else:
                    f_out.write("\nString: '{}' contains invalid character(s)".format(string))
                if lin != line_no:
                    f_out.write("\n\nline_no: '{}', len(line): '{}', content: '{}'".format(line_no, len(line), line))
                lb = fp + 1
            continue

        if debugging:
            f_out.write(lb, fp, "'{}'".format(char))
        
        if is_comments(char):#Get '#'
            if lb != fp:
                find_type(line[lb:fp], f_out)
            find_type(line[fp:], f_out, line)
            break

        if char == '"' and not is_string:
            #start of string
            if lb == fp:
                is_string = True
                string += char
            else:
                find_type(line[lb:fp], f_out)
                lb = fp+1
            continue

        if not is_valid(char):
            f_out.write("\nCharacer: '{}'\tat position: '{}'\t is invalid".format(char, fp))
            
        if (char == " " or char == '\t') and lb == fp: #Space and begin
            lb +=1
            if debugging:
                f_out.write("\nin char == ' ' or char == '\t'")
            continue
            
        if is_delimiter(char) or is_operator(char):

            if lb == fp and ((char != '+' and char != '-') or not prev_op_delim):
                find_type(char, f_out)
            
            lexeme = line[lb:fp]
            if fp == (len(line)-1) and lb == fp: #Nothing on the right and semicolon
                find_type(char, f_out)
                
            if lb > fp or len(lexeme) == 0: #Lexeme ="" or 
                continue   
                
            if debugging:
                f_out.write("\nHandeling: '{}', char: '{}'".format(lexeme, char), lb, fp)
                
            find_type(lexeme, f_out) 
            if line[fp] != " " and not prev_op_delim:
                if debugging:
                    f_out.write("\nChar: '{}'".format(char))
                find_type(char, f_out)
            elif prev_op_delim and char == '+' or char == '-':
                lb = fp
                prev_op_delim = False
            continue
        if fp == len(line)-1:
            find_type(line[lb:], f_out)             
        

def driver(in_file, out_file):
    global prev_op_delim
    global lin
    global line_no
    global length
    global f_out
    global line
    f_in = open(in_file, "r")
    content = list(f_in)
    f_out = open(out_file, "w")
    length = len(content)
    lin = 0
    for line_no, line in enumerate(content):
        prev_op_delim = False
        line_no+=1
        if line[-1] == '\n':
            line = line[:-1]                 #Remove '\n'
        
        if not is_string:
            lin = line_no
            f_out.write("\nline_no: '{}', len(line): '{}', content: '{}'".format(line_no, len(line), line))
        handle()#, debugging=True)
        if not is_string:
            f_out.write("\n")

line = []
f_out = 0
if __name__ == "__main__":
    driver("code.txt", "out_code.txt")
