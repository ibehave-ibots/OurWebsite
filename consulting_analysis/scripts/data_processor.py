def count_page_breaks(doc, pattern='___'):
    page_break_count = 0
    pages = []
    current_text = ""

    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            if run._r.xpath('.//w:br[@w:type="page"]'):
                page_break_count += 1
                if pattern in current_text:
                    pages.append(current_text.split(pattern)[0].strip())
                else:
                    pages.append(current_text.strip())
                current_text = ""
            else:
                current_text += run.text + '\n'
    
    if current_text.strip():
        if pattern in current_text:
            pages.append(current_text.split(pattern)[0].strip())
        else:
            pages.append(current_text.strip())

    return page_break_count, pages
