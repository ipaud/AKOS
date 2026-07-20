"""Minimal, stdlib-only YAML subset parser for AKOS.

AKOS's own YAML (metadata.yaml, rule registry files) is deliberately simple:
flat ``key: value`` maps, inline flow lists (``key: [a, b, c]``), and one or
two levels of nested maps/list-of-maps (``sources:`` -> list of
``{title, author, url}``). This parser handles exactly that subset and
nothing more, so AKOS never needs a pip dependency (PyYAML/ruamel) just to
read its own metadata.

Deliberately unsupported (raises YamlSubsetError with the offending line,
rather than silently mis-parsing): anchors/aliases (&, *), block scalars
(| or >), flow mappings ({a: b}), multi-document streams, tab indentation.
AKOS controls all the YAML this parser ever reads, so the fix for hitting
one of these is "simplify the YAML," not "extend the parser."

One real limitation worth stating plainly: a key or an unquoted scalar must
not itself contain the two-character sequence ": " (colon-space) except as
the intended key/value separator — this parser takes the *first* such
sequence on a line as the split point and does not attempt full quote-aware
scanning for the key. Quote the value if it needs an internal ": ".
"""

from __future__ import annotations

import re
from pathlib import Path


class YamlSubsetError(Exception):
    def __init__(self, message: str, line_no: int | None = None):
        self.line_no = line_no
        full = f"{message} (line {line_no})" if line_no else message
        super().__init__(full)


_INT_RE = re.compile(r"^-?\d+$")


def load(path) -> dict | list:
    """Parse a YAML-subset file from disk."""
    text = Path(path).read_text(encoding="utf-8")
    return loads(text)


def loads(text: str) -> dict | list:
    """Parse a YAML-subset document from a string."""
    tokens = _tokenize(text)
    if not tokens:
        return {}
    root_indent = tokens[0][1]
    value, idx = _parse_node(tokens, 0, root_indent)
    if idx != len(tokens):
        raise YamlSubsetError(
            "trailing content after root document — check indentation consistency",
            tokens[idx][0],
        )
    return value


# --- Tokenizing -------------------------------------------------------------


def _leading_ws(line: str) -> str:
    i = 0
    while i < len(line) and line[i] in (" ", "\t"):
        i += 1
    return line[:i]


def _strip_comment(line: str) -> str:
    """Remove a trailing '# comment', respecting quoted strings."""
    out = []
    in_single = in_double = False
    for i, c in enumerate(line):
        if c == "'" and not in_double:
            in_single = not in_single
        elif c == '"' and not in_single:
            in_double = not in_double
        elif c == "#" and not in_single and not in_double:
            if i == 0 or line[i - 1] in (" ", "\t"):
                break
        out.append(c)
    return "".join(out).rstrip()


def _tokenize(text: str):
    """Return a list of (line_no, indent, content) for every non-blank, non-comment line."""
    tokens = []
    for line_no, raw in enumerate(text.split("\n"), start=1):
        if raw.strip() == "":
            continue
        if "\t" in _leading_ws(raw):
            raise YamlSubsetError("tab characters in indentation are not supported", line_no)
        stripped = _strip_comment(raw)
        if stripped.strip() == "":
            continue
        content = stripped.lstrip(" ")
        indent = len(stripped) - len(content)
        content = content.rstrip()
        if content in ("---", "..."):
            continue  # document markers, ignored — AKOS files are single-document
        tokens.append((line_no, indent, content))
    return tokens


# --- Key/value splitting -----------------------------------------------------


def _split_key_value(s: str):
    """If `s` looks like 'key: rest' or 'key:', return (key, rest). Else None.

    The split point is the FIRST colon immediately followed by whitespace or
    end-of-string — this is what lets 'https://example.com' (colon followed
    by '/') and 'Ratio 4.5:1 minimum' (colon followed by a digit) correctly
    fail to match and fall through to scalar parsing, with no key-charset
    restriction needed (real AKOS content uses spaced keys like "Game Dev").
    """
    n = len(s)
    i = 0
    while i < n:
        if s[i] == ":":
            nxt = s[i + 1] if i + 1 < n else ""
            if nxt in ("", " ", "\t"):
                key = s[:i].strip()
                key = _unquote_if_wrapped(key)
                if key == "":
                    return None
                rest = s[i + 1 :].strip()
                return key, rest
        i += 1
    return None


def _unquote_if_wrapped(s: str) -> str:
    if len(s) >= 2 and s[0] == s[-1] == '"':
        return s[1:-1]
    if len(s) >= 2 and s[0] == s[-1] == "'":
        return s[1:-1]
    return s


# --- Scalars and flow lists ---------------------------------------------------


def _parse_scalar(s: str):
    s = s.strip()
    if s == "":
        return None
    if len(s) >= 2 and s[0] == s[-1] == '"':
        return s[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    if len(s) >= 2 and s[0] == s[-1] == "'":
        return s[1:-1].replace("''", "'")
    if s in ("true", "True", "TRUE"):
        return True
    if s in ("false", "False", "FALSE"):
        return False
    if s in ("null", "Null", "NULL", "~"):
        return None
    if _INT_RE.match(s):
        return int(s)
    # Deliberately no float coercion: version strings ("1.0.0") and dates
    # ("2026-07-09") both look numeric-with-dots; keeping everything else as
    # a plain string avoids silent type surprises the schema layer would
    # then have to work around.
    return s


def _split_flow_items(inner: str):
    items = []
    current = []
    in_single = in_double = False
    depth = 0
    for ch in inner:
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        if ch == "," and not in_single and not in_double and depth == 0:
            items.append("".join(current))
            current = []
            continue
        if ch in "[{":
            depth += 1
        elif ch in "]}":
            depth -= 1
        current.append(ch)
    if current:
        items.append("".join(current))
    return items


def _parse_flow_list(s: str, line_no: int):
    if not (s.startswith("[") and s.endswith("]")):
        raise YamlSubsetError("malformed flow list (missing ']')", line_no)
    inner = s[1:-1].strip()
    if inner == "":
        return []
    return [_parse_scalar(item.strip()) for item in _split_flow_items(inner)]


# --- Structural parsing -------------------------------------------------------


def _parse_node(tokens, start, indent):
    if start >= len(tokens):
        return None, start
    line_no, tok_indent, content = tokens[start]
    if tok_indent != indent:
        raise YamlSubsetError("unexpected indentation", line_no)
    if content == "-" or content.startswith("- "):
        return _parse_list(tokens, start, indent)
    return _parse_map(tokens, start, indent)


def _consume_value(tokens, i, indent, rest, line_no, container, key):
    """Assign container[key] from `rest` (the text after 'key:'), consuming
    a nested block from tokens[i:] if `rest` was empty. Returns the new i."""
    if rest == "":
        if i < len(tokens) and tokens[i][1] > indent:
            nested_indent = tokens[i][1]
            value, i = _parse_node(tokens, i, nested_indent)
        else:
            value = None
        container[key] = value
        return i
    if rest in ("|", ">") or rest.startswith("|") or rest.startswith(">"):
        raise YamlSubsetError("block scalars ('|' or '>') are not supported", line_no)
    if rest.startswith("&") or rest.startswith("*"):
        raise YamlSubsetError("anchors/aliases ('&'/'*') are not supported", line_no)
    if rest.startswith("["):
        container[key] = _parse_flow_list(rest, line_no)
        return i
    if rest.startswith("{"):
        raise YamlSubsetError("flow mappings ('{...}') are not supported", line_no)
    container[key] = _parse_scalar(rest)
    return i


def _parse_map(tokens, start, indent):
    result = {}
    i = start
    while i < len(tokens):
        line_no, tok_indent, content = tokens[i]
        if tok_indent < indent:
            break
        if tok_indent > indent:
            raise YamlSubsetError("unexpected indentation increase", line_no)
        if content == "-" or content.startswith("- "):
            raise YamlSubsetError("expected a mapping entry, found a list item", line_no)
        kv = _split_key_value(content)
        if kv is None:
            raise YamlSubsetError("expected 'key: value'", line_no)
        key, rest = kv
        i += 1
        i = _consume_value(tokens, i, indent, rest, line_no, result, key)
    return result, i


def _parse_list(tokens, start, indent):
    result = []
    i = start
    while i < len(tokens):
        line_no, tok_indent, content = tokens[i]
        if tok_indent != indent or not (content == "-" or content.startswith("- ")):
            break
        item_content = content[1:].strip()
        consumed_prefix_len = len(content) - len(item_content)
        virtual_indent = indent + consumed_prefix_len
        i += 1

        if item_content == "":
            if i < len(tokens) and tokens[i][1] > indent:
                nested_indent = tokens[i][1]
                value, i = _parse_node(tokens, i, nested_indent)
            else:
                value = None
            result.append(value)
            continue

        kv = _split_key_value(item_content)
        if kv is None:
            result.append(_parse_scalar(item_content))
            continue

        # "- key: value" — this item is a map. Consume this key, then any
        # sibling keys of the same map at `virtual_indent`.
        item_map = {}
        key, rest = kv
        i = _consume_value(tokens, i, virtual_indent, rest, line_no, item_map, key)
        while i < len(tokens):
            sub_line_no, sub_indent, sub_content = tokens[i]
            if sub_indent != virtual_indent:
                break
            if sub_content == "-" or sub_content.startswith("- "):
                break
            skv = _split_key_value(sub_content)
            if skv is None:
                break
            skey, srest = skv
            i += 1
            i = _consume_value(tokens, i, virtual_indent, srest, sub_line_no, item_map, skey)
        result.append(item_map)
    return result, i
