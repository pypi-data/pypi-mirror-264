import traceback
import click
import grpc
import tqdm
import detoxio.config as config
import detoxio.adapters.exceptions as exceptions

from detoxio.scanner import LLMScanner, LLMPrompt, LLMResponse
from detoxio.reporting import JSONLinesLLMScanReport
from detoxio.cli.utils import print_info, print_error, print_success, print_verbose, is_verbose
from detoxio.cli.inferencing import TransformersAdapter
from detoxio.cli.console import ConsoleReporter
from detoxio.adapters.grpc import get_secure_channel_with_token
from detoxio.adapters.prompts import get_prompts_service

@click.group()
def main():
    """
    An LLM vulnerability scanner built using the Detoxio API.
    Refer to https://docs.detoxio.ai for more information.
    """

@click.command("version", help="Print the version of the CLI tool")
def version():
    """
    Print the version of the CLI tool.
    """
    from importlib.metadata import version
    print_info(f"Detoxio CLI version: {version('detoxio')}")

@click.command("ping", help="Check API server reachability and authentication")
def ping():
    """
    Check if the API server is reachable and authenticated.
    """
    print_info("Attempting to ping remote server")

    key = config.load_key_from_env()
    channel = get_secure_channel_with_token(config.get_api_host(), config.get_api_port(), key)
    prompt_service = get_prompts_service(channel)

    try:
        prompt_service.ping()
        print_success("Server is reachable and authenticated")
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.PERMISSION_DENIED:
            print_error("Server is reachable but not authenticated")
        else:
            print_error(f"Server is not reachable: {e.details()}")

@click.command("scan", help="Scan a model from Hugging Face for security vulnerablities")
@click.option("--model", type=str, required=True, help="The model to scan")
@click.option("--count", type=int, help="The number prompts to generate for scanning", default=10)
@click.option("--jsonl", type=str, help="Output the results in JSONL format")
@click.option("--fast", is_flag=True, help="Use fast evaluation mode which is less accurate")
@click.option("--verbose", is_flag=True, help="Enable verbose mode")
def scan(model, count, jsonl, fast, verbose, *extra):
    """
    Scan a model from Hugging Face for security vulnerabilities.
    """
    key = config.load_key_from_env()
    scanner = LLMScanner(count=count, key=key)

    if fast:
        print_info("Using fast evaluation mode")
        scanner.use_fast_evaluation()

    print_info(f"Initializing model adapter for: {model} using Transformers")
    inference_adapter = TransformersAdapter(model_name=model)

    reporters = []
    if jsonl:
        file = open(jsonl, "w")
        reporters.append(JSONLinesLLMScanReport(file=file))

    print_info(f"Initializing scanner for testing with {count} prompt(s)")

    # We will manually handle the progress bar
    if not is_verbose():
        progress = tqdm.tqdm(total=count, desc="Scanning model", unit="prompt")
    else:
        print_verbose("Verbose mode is enabled, progress bar will not be displayed")

    # This is the callback function called by LLMScanner to
    # interact with an LLM using the provided prompt
    def prompt_handler(prompt: LLMPrompt) -> LLMResponse:
        print_verbose("Sending prompt to model for inference")
        output = inference_adapter.inference(prompt.content)

        if not is_verbose():
            progress.update(1)
            progress.refresh()

        print_verbose("Received response from model")
        return LLMResponse(content=output)

    if not is_verbose():
        progress.refresh()

    print_verbose("Starting scan")
    results = scanner.start(prompt_handler=prompt_handler)

    if not is_verbose():
        progress.close()

    print_success("Scan complete!")

    print_info(f"Writing reports using {len(reporters)} reporter(s)")
    for reporter in reporters:
        reporter.render(results)

    print_info("Rendering console report")
    console_reporter = ConsoleReporter()
    console_reporter.render(results)

main.add_command(ping)
main.add_command(scan)
main.add_command(version)

if __name__ == "__main__":
    # TODO: We should replace this exception handler with something
    # like sentry which should report the error detail
    try:
        main()
    except Exception as e:
        if isinstance(e, exceptions.AuthenticationError):
            print_error("Error: Authentication failed, please check your API key")
        elif isinstance(e, exceptions.TimeoutError):
            print_error("Error: Timeout occurred while communicating with the server")
        elif isinstance(e, exceptions.InternalServerError):
            print_error("Error: Internal server error occurred")
        else:
            print_error(f"Error: {e}")
            click.echo(traceback.format_exc(), err=True)

