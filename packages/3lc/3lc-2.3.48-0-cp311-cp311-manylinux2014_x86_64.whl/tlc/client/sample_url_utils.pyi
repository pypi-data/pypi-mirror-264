from tlc.core.url import Url as Url
from typing import Iterator

def set_sample_url_prefix(prefix: Url) -> None:
    """Set the global variable for the sample URL prefix."""
def increment_and_get_sample_url(sample_name: str, suffix: str) -> Url:
    """Increment the sample Url index and return a Url corresponding to the given sample_name and suffix, and the
    current values of the global sample Url prefix and index.

    :param sample_name: The name of the part of the sample to generate the Url for.
    :param suffix: The suffix to be used for the sample Url.
    :return: The generated Url.
    """
def reset_sample_url() -> None:
    """Reset the global sample Url prefix and index."""
def sample_url_context(prefix: Url) -> Iterator[None]:
    """Context manager which sets the global sample Url prefix to the given prefix, and resets it after the context
    manager exits.

    :param prefix: The prefix to set the global sample Url prefix to.
    """
