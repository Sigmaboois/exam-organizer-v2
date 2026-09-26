import re
import reader

def meta_extract(extracted_pdf):

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
        else:
            metadata["session"] = "March"
    else:
        print("There was no code in this exam.")

    # YEAR DECLARATION
    metadata["year"] = code_splitted[4]

    return metadata

if __name__ == "__main__":
    print("This is a test\n")
    pdf = input("Please paste in the pdf u want to extract the metadata from:\n")
    text = reader.read_file(pdf)
    print(meta_extract(text))