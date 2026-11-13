# BinPack — Schema-to-Python Binary Serialization Compiler

BinPack compiles a small schema language into Python classes for packing structured records into binary data and unpacking individual records. A browser interface lets you compile a schema, serialize a JSON array, inspect the resulting bytes and compare binary size with the submitted JSON text.

The project demonstrates compiler construction and data representation: tokenization, parsing, semantic checks, intermediate representation and code generation.

## Example

Define a record in the schema language:

```text
struct Player {
    int health;
    string[20] name;
}
```

The compiler produces a Python `Player` class with:

| Generated member | Purpose |
| --- | --- |
| `FORMAT = '<i20s'` | Little-endian 32-bit signed integer followed by a 20-byte string field |
| `SIZE = 24` | Fixed byte length of one record |
| `pack()` | Encode an instance into bytes |
| `Player.unpack(data)` | Decode one complete record |
| `serialize_list(data_list)` | Serialize a list of dictionaries into concatenated records |

For `Player(100, "Aditya")`, the 24-byte result is:

```text
640000004164697479610000000000000000000000000000
```

## Compiler pipeline

| Stage | Module | Responsibility |
| --- | --- | --- |
| Lexical analysis | `lexer.py` | Recognize keywords, identifiers, numbers and punctuation; track line and column positions |
| Parsing | `parser.py` | Build a structure definition and its field list |
| Semantic analysis | `semantic.py` | Check duplicate fields, supported types and positive string lengths |
| Intermediate representation | `intermediate.py` | Map fields to Python `struct` format codes and byte sizes |
| Size calculation | `optimizer.py` | Add the total record size to the IR |
| Code generation | `codegen.py` | Emit a Python class and a list serialization helper |

`compiler.py` coordinates these stages. The size-calculation pass adds metadata; it does not perform compression or change the schema's field layout.

## Supported schema

- One `struct` declaration with semicolon-terminated fields.
- `int`: a signed 32-bit integer encoded as four bytes.
- `string[N]`: a fixed-width field of `N` bytes.
- Little-endian byte order with no automatic alignment padding.
- Declaration order determines the binary layout.

For predictable generated Python, use ordinary Python-compatible class and field names, avoiding Python keywords and collisions with generated members such as `pack`, `unpack`, `FORMAT` and `SIZE`.

Strings are UTF-8 encoded and null padded. The width is a byte budget, not a character count. Keep encoded text within that budget: Python's `struct` truncates overlong byte strings, which can split a multibyte character and make decoding fail.

## Run the browser demo locally

The compiler core uses only the Python standard library. The web API additionally requires Flask and Flask-CORS.

### 1. Set up the project

```bash
git clone https://github.com/AdityaChhimwal/binpack.git
cd binpack
python -m venv .venv
```

Activate the environment:

| Shell | Command |
| --- | --- |
| macOS / Linux | `source .venv/bin/activate` |
| Windows PowerShell | `.\.venv\Scripts\Activate.ps1` |
| Windows Command Prompt | `.venv\Scripts\activate.bat` |

```bash
python -m pip install Flask Flask-Cors
python backend/app.py
```

The API runs at `http://127.0.0.1:5000`, matching the address in `frontend/script.js`.

### 2. Serve the frontend

In a second terminal at the repository root:

```bash
python -m http.server 8080 --directory frontend --bind 127.0.0.1
```

Open [http://127.0.0.1:8080](http://127.0.0.1:8080). The size comparison chart loads Chart.js from a CDN and requires internet access.

### 3. Compile and serialize

Paste the Player schema above and choose **Compile**. Then paste this JSON array into the data field and choose **Serialize**:

```json
[{"health":100,"name":"Aditya"},{"health":80,"name":"Mira"}]
```

The result is **48 bytes**: two records of 24 bytes each. The exact single-line JSON shown above is **60 UTF-8 bytes**. Extra whitespace or different values change the JSON size; binary size stays fixed for the same schema and record count.

The interface also accepts a JSON file upload. It displays generated Python, binary hex output, byte counts and a comparison chart.

## Use the compiler from Python

Run this from the repository root to write the generated module:

```bash
python -c "from pathlib import Path; from compiler import compile_code; result = compile_code(Path('examples/player.pack').read_text()); Path('player_generated.py').write_text(result['code'])"
```

Then use the generated code:

```python
from player_generated import Player, serialize_list

player = Player(100, "Aditya")
packed = player.pack()
restored = Player.unpack(packed)

assert len(packed) == Player.SIZE == 24
assert (restored.health, restored.name) == (100, "Aditya")

records = [
    {"health": 100, "name": "Aditya"},
    {"health": 80, "name": "Mira"},
]
binary = serialize_list(records)
assert len(binary) == 48

second = Player.unpack(binary[Player.SIZE : 2 * Player.SIZE])
assert (second.health, second.name) == (80, "Mira")
```

The binary stream does not embed the schema or record count. A reader needs the same schema and must split the bytes into `SIZE`-byte records.

## HTTP API

| Method | Endpoint | Request | Response |
| --- | --- | --- | --- |
| POST | `/compile` | JSON object with a `schema` string | `generated_code` and `ir` |
| POST | `/serialize` | JSON object with `schema` and `data` strings | `binary_hex`, `json_size` and `binary_size` |

For `/serialize`, `data` is JSON array text encoded as a string inside the request, matching the browser client.

## Current scope

- Educational local prototype with one record schema, integers and fixed-width strings. Nested structures, variable-length fields, floating-point types and schema evolution are not implemented.
- Fixed-width encoding can be smaller or larger than JSON depending on the schema and data. The size comparison is not a general compression or performance benchmark.
- Some invalid schemas call `sys.exit` in the lexer, parser or semantic analyzer rather than returning structured compiler errors. Consistent API error handling remains an improvement.
- The serialization endpoint executes generated Python, and the server starts in Flask debug mode. Use the current demo locally with trusted schemas; it has not been hardened for public hosting.
