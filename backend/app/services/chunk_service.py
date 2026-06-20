from langchain_text_splitters import RecursiveCharacterTextSplitter

# def chunk_text(
#         text: str,
#         chunk_size: int = 500,
#         overlap: int = 100
# ):
#     chunks = []

#     start = 0

#     while start < len(text):
#         end = start + chunk_size

#         chunks.append(text[start:end])

#         start += chunk_size - overlap

#     return chunks



def chunk_text(
        text: str,
        chunk_size: int = 800,
        overlap: int = 150
):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap
    )

    return splitter.split_text(text)