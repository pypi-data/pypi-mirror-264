import ctypes
from dataclasses import dataclass
import platform
import pkg_resources

# Determine the shared library file based on the platform
if platform.system().lower() == "linux":
    lib_file = "library_linux.so"
elif platform.system().lower() == "windows":
    raise Warning("Windows is not supported.")
else:
    lib_file = "library.so"  # Fallback or default to non-Linux

# Try to load the library from the package resources
so_path = pkg_resources.resource_filename("last_layer", f"lib/{lib_file}")

try:
    library = ctypes.cdll.LoadLibrary(so_path)
except OSError as e:
    # Fallback to trying to load directly in case of failure
    for path in [f"lib/{lib_file}", f"/var/task/last_layer/{lib_file}"]:
        try:
            library = ctypes.cdll.LoadLibrary(f"lib/{lib_file}")
            break
        except OSError:
            continue
    else:
        raise RuntimeError(f"Failed to load shared library {lib_file}") from e

Threats = [
    "MixedLangMarker",
    "InvisibleUnicodeDetector",
    "MarkdownLinkDetector",
    "HiddenTextDetector",
    "Base64Detector",
    "SecretsMarker",
    "ProfanityDetector",
    "PiiMarker",
    "ExploitClassifier",
    "ObfuscationDetector",
    "CodeFilter",
]


@dataclass
class RiskModel:
    query: str
    markers: dict
    passed: bool
    # score: float


def deserialize(prompt: str, serialized_str: str) -> RiskModel:
    parts = serialized_str.split("|")
    passed = parts[0] == "1"
    markers = {}

    if not passed:
        for part in parts[1:]:
            index, message = part.split(":", 1)
            index = int(index)
            markers[Threats[index]] = message
    # Assuming default values for query and score for demonstration purposes
    return RiskModel(
        query=prompt,
        markers=markers,
        passed=passed,
    )


heuristic = library.heuristicP
heuristic.restype = ctypes.c_void_p
heuristic.argtypes = [ctypes.c_char_p]


def scan_prompt(prompt: str) -> RiskModel:
    # this is a pointer to our string
    farewell_output = heuristic(prompt.encode("utf-8"))
    if farewell_output is None:
        raise ValueError("Failed to scan prompt err#1")
    # we dereference the pointer to a byte array
    farewell_bytes = ctypes.string_at(farewell_output).decode("utf-8")
    # library.freeCString(farewell_output)
    return deserialize(prompt, farewell_bytes)


scan_llm = scan_prompt


def version():
    return "0.1.0"
