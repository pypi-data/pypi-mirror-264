# Description: Common data models for the SDK

# Data class representing a generated prompt
class LLMPrompt:
    def __init__(self, content: str, role="user"):
        self.role = role
        self.content = content

    def text(self):
        return self.content

# Data class representing a prompt response from an LLM model
class LLMResponse:
    def __init__(self, content: str):
        self.content = content

# Data class representing the result of a prompt and response
# evaluation for security vulnerabilities
class LLMScanResult:
    def __init__(self):
        self.results = []

    # Store the raw protobuf response from the API for
    # rendering into various forms
    def add_raw_result(self, response):
        self.results.append(response)

    def __iter__(self):
        return iter(self.results)

