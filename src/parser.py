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

        # Qualifcation Extraction
        IGCSE_pattern = r"IGCSE|General Certificate of Secondary Education"
        O_level_pattern = r"O Level|Ordinary Level"
        AS_level_pattern = r"Cambridge International AS Level"
        AS_ALevel_pattern = r"AS & A Level|Advanced Subsidiary and Advanced Level|Advanced Subsidiary Level and Advanced Level|International Advanced Level"

        if re.search(IGCSE_pattern,extracted_pdf):
            metadata["qualification"] = "IGCSE"
        elif re.search(O_level_pattern,extracted_pdf):
            metadata["qualification"] = "O Level"
        elif re.search(AS_level_pattern,extracted_pdf):
            metadata["qualification"] = "AS"
        elif re.search(AS_ALevel_pattern,extracted_pdf):
            metadata["qualification"] = "AS & A Level"  

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
            metadata["year"] = "20" + code_splitted[4]

        else:
            print("There was no code in this exam.")

    if metadata["paper_type"] == "MS":
        # MS extraction logic

        new_code_paperv_pattern =r"(\d{4})/(\d{2}) (.+?) – Mark Scheme"
        new_code_paperv = re.search(new_code_paperv_pattern,extracted_pdf)
        
        if not new_code_paperv:
            old_code_paperv_pattern = r"(.+?) – (October/November|May/June|February/March|March|June) (\d{4})\s+(\d{4})\s+(\d{2})"
            old_code_paperv = re.search(old_code_paperv_pattern,extracted_pdf)

            
            if old_code_paperv:
                qual_in_old = old_code_paperv.group(1).strip().lower()
                if "igcse" in qual_in_old:
                    metadata["qualification"] = "IGCSE"
                elif "o level" in qual_in_old:
                    metadata["qualification"] = "O Level"
                elif "as level" in qual_in_old:
                    metadata["qualification"] = "AS"
                elif "a level" in qual_in_old:
                    metadata["qualification"] = "AS & A Level"

                metadata["session"] = old_code_paperv.group(2).strip()
                metadata["year"] = old_code_paperv.group(3).strip()
                metadata["subject_code"] = old_code_paperv.group(4).strip()
                old_pv = old_code_paperv.group(5)
                metadata["paper"] = old_pv[0]
                metadata["variant"] = old_pv[1]
        
        else:

            qual_in_new = new_code_paperv.group(3).strip().lower()
            if "igcse" in  qual_in_new:
                metadata["qualification"] = "IGCSE"
            elif "o level" in qual_in_new:
                metadata["qualification"] = "O Level"
            elif "as level" in qual_in_new:
                metadata["qualification"] = "AS"
            elif "a level" in qual_in_new:
                metadata["qualification"] = "AS & A Level"

            
            metadata["subject_code"] = new_code_paperv.group(1).strip()

            pv = new_code_paperv.group(2)
            metadata["paper"] = pv[0]
            metadata["variant"] = pv[1]

            new_year_session_pattern = r"mark schemes for the\s+(May/June|October/November|February/March|March|June)\s+(\d{4})"
            new_year_session = re.search(new_year_session_pattern,extracted_pdf)
            if new_year_session:
                session = new_year_session.group(1)
                if session == "June":
                    metadata["session"] = "May/June"
                elif session == "March":
                    metadata["session"] = "February/March"
                else:
                    metadata["session"] = session
                metadata["year"] = new_year_session.group(2).strip()


    return metadata

if __name__ == "__main__":
    print("This is a test\n")
    pdf = input("Please paste in the pdf u want to extract the metadata from:\n")
    text = reader.read_file(pdf)
    print(meta_extract(text))