import csv
import io


COMMENT_COLUMN_ALIASES = (
    "comment",
    "comments",
    "text",
    "body",
    "content",
    "message",
    "review",
)


def find_comment_column(fieldnames):
    normalized_fieldnames = {
        str(fieldname).strip().lower(): fieldname for fieldname in fieldnames or []
    }
    for alias in COMMENT_COLUMN_ALIASES:
        if alias in normalized_fieldnames:
            return normalized_fieldnames[alias]

    raise ValueError("CSV must include a Comment, comments, or text column.")


def _text_stream_from_source(csv_source):
    if hasattr(csv_source, "read"):
        csv_source.seek(0)
        content = csv_source.read()
        csv_source.seek(0)
        if isinstance(content, bytes):
            content = content.decode("utf-8-sig")
        return io.StringIO(content)

    return open(csv_source, "r", encoding="utf-8-sig", newline="")


def load_comments_from_csv(csv_source):
    text_stream = _text_stream_from_source(csv_source)
    close_stream = text_stream is not csv_source
    try:
        reader = csv.DictReader(text_stream)
        comment_column = find_comment_column(reader.fieldnames)
        comments = [
            str(row.get(comment_column, "")).strip()
            for row in reader
            if str(row.get(comment_column, "")).strip()
        ]
    finally:
        if close_stream:
            text_stream.close()

    if not comments:
        raise ValueError("CSV does not contain any non-empty comments.")

    return comments
