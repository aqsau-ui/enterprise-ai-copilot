def chunk_text(
    text: str,
    chunk_size: int = 350,
    overlap: int = 75
) -> list[str]:
    """
    Split text into overlapping word-based chunks.

    Smaller chunks help retrieval find more precise
    pieces of information while overlap preserves context.
    """

    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n")
        if paragraph.strip()
    ]

    chunks = []
    current_words = []

    for paragraph in paragraphs:
        paragraph_words = paragraph.split()

        # If adding this paragraph keeps the chunk
        # within the target size, keep it together.
        if len(current_words) + len(paragraph_words) <= chunk_size:
            current_words.extend(paragraph_words)

        else:
            if current_words:
                chunks.append(" ".join(current_words))

            # Keep some previous context.
            overlap_words = current_words[-overlap:]

            current_words = (
                overlap_words + paragraph_words
            )

            # Handle very large paragraphs.
            while len(current_words) > chunk_size:
                chunks.append(
                    " ".join(current_words[:chunk_size])
                )

                current_words = current_words[
                    chunk_size - overlap:
                ]

    if current_words:
        chunks.append(" ".join(current_words))

    return chunks