from typing import Mapping, Sequence, Tuple, Union


def fetch_smalltable_rows(
    table_handle: int,
    keys: Sequence[Union[bytes, str]],
    require_all_keys: bool = False,
) -> Mapping[bytes, Tuple[str, ...]]:
    """Fetches rows from a Smalltable.

    Retrieves rows pertaining to the given keys from the Table instance
    represented by table_handle.  String keys will be UTF-8 encoded.

    Args:
        table_handle: An open smalltable.Table instance.
        keys: A sequence of strings representing the key of each table
          row to fetch.  String keys will be UTF-8 encoded.
        require_all_keys: If True only rows with values set for all keys will be
          returned.

    Returns:
        A dict mapping keys to the corresponding table row data
        fetched. Each row is represented as a tuple of strings. For
        example:

        {b'Serak': ('Rigel VII', 'Preparer'),
         b'Zim': ('Irk', 'Invader'),
         b'Lrrr': ('Omicron Persei 8', 'Emperor')}

        Returned keys are always bytes.  If a key from the keys argument is
        missing from the dictionary, then that row was not found in the
        table (and require_all_keys must have been False).

    Raises:
        IOError: An error occurred accessing the smalltable.
    """
    raise NotImplementedError


class SampleClass:
    """Summary of class here.

    Longer class information....
    Longer class information....

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """

    likes_spam: bool
    eggs: int

    def __init__(self, likes_spam: bool = False):
        super().__init__()
        """Inits SampleClass with blah."""
        self.likes_spam = likes_spam
        self.eggs = 0

    def public_method(self):
        """Performs operation blah."""

    @staticmethod
    def test_method(a: int, b: int) -> int:
        """Short description.

        long description.

        Args:
            a: number a
            b: number b

        Returns:
            a number of sum of a nad b
        """
        raise NotImplementedError

    @property
    def test_property(self) -> str:
        """test_property description."""
        raise NotImplementedError

    @classmethod
    def test_classmethod(cls, a: int) -> None:
        raise NotImplementedError
