
LOW_QUALITY_TRIGGERS = ["i don't know", 'cannot', 'not sure', 'unsure', 'no reliable', 'no information']

def is_low_quality_answer(ans: str) -> bool:
    if not ans:
        return True
    a = ans.lower()
    for t in LOW_QUALITY_TRIGGERS:
        if t in a:
            return True
    if len(a.split()) < 6:
        return True
    return False

from langchain.text_splitter import RecursiveCharacterTextSplitter
def rechunk_text(text: str, chunk_size: int = 500, overlap: int = 50):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    return splitter.split_text(text)
