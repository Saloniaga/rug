from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_text(
        text: str,
        chunk_size: int = 400,
        overlap: int = 50
):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap
    )

    chunks = splitter.split_text(text)

    print(f"\nCreated {len(chunks)} chunks\n")

    for i, chunk in enumerate(chunks):
        print("=" * 80)
        print(f"Chunk {i}")
        print("=" * 80)
        print(chunk[:300])
        print()

    return chunks