import re
import reader

def meta_extract(extracted_pdf):

    # Initialization of metadata dictionary
    metadata = {
        "qualification" : None,
        "subject_name" : None,
        "subject_code" : None,
        "year" : None,
        "session" : None,
        "paper" : None,
        "variant" : None,
        "paper_type" : None
    }

    # paper_type extraction
    if "MARK SCHEME" in extracted_pdf:
        metadata["paper_type"] = "MS"
    else:
        metadata["paper_type"] = "QP"
    
    # parser logic depending on type of paper
    if metadata["paper_type"] == "QP":
        # Initialization of code patterns and search object
        code_pattern = r"\d{4}/\d{2}/\w/\w/\d{2}"
        codematch = re.search(code_pattern,extracted_pdf)

        # IF TO CHECK IF CODEMATCH FOUND ANYTHING
        if codematch:
            code = codematch.group()
        else:
            code = None

        if code is not None:
            # CODE SPLITTING AND DECLARATION OF SUBJECT CODE
            code_splitted = code.split("/")
            metadata["subject_code"] = code_splitted[0]

            # PAPER AND VARIANT DECLARATION
            paper_variant = code_splitted[1]
            paper = paper_variant[0]
            variant = paper_variant[1]
            metadata["paper"] = paper
            metadata["variant"] = variant

            # SESSION DECLARATION
            if code_splitted[2] == "O":
                metadata["session"] = "October/November"
            elif code_splitted[2] == "M":
                metadata["session"] = "May/June"
            elif code_splitted[2] == "F":
                metadata["session"] = "February/March"
            
            # YEAR DECLARATION
            metadata["year"] = code_splitted[4]
            
        else:
            print("There was no code in this exam.")

    elif metadata["paper_type"] == "MS":
        print("This is temporary")
        # MS extraction logic goes here     

    return metadata

if __name__ == "__main__":
    print("This is a test\n")
    pdf = input("Please paste in the pdf u want to extract the metadata from:\n")
    text = reader.read_file(pdf)
    print(meta_extract(text))