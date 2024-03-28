import polars as pl
from polars_ngrams import ngrams


def test_ngrams():
    df = pl.DataFrame(
        {
            "words": [
                ["this", "is", "not", "pig", "latin"],
                ["this", "is", "a", "list", "of", "words"],
                ["Albert Einstein", "was", "a", "German", "physicist"],
                [
                    "Leonhard Euler",
                    "was",
                    "an",
                    "impressive",
                    "mathematician",
                    "who",
                    "excelled",
                    "in",
                    "many",
                    "fields",
                ],
            ],
        }
    )
    result = df.select(ngrams=ngrams("words", n=2))

    expected_df = pl.DataFrame(
        {
            "ngrams": [
                [["this", "is"], ["is", "not"], ["not", "pig"], ["pig", "latin"]],
                [
                    ["this", "is"],
                    ["is", "a"],
                    ["a", "list"],
                    ["list", "of"],
                    ["of", "words"],
                ],
                [
                    ["Albert Einstein", "was"],
                    ["was", "a"],
                    ["a", "German"],
                    ["German", "physicist"],
                ],
                [
                    ["Leonhard Euler", "was"],
                    ["was", "an"],
                    ["an", "impressive"],
                    ["impressive", "mathematician"],
                    ["mathematician", "who"],
                    ["who", "excelled"],
                    ["excelled", "in"],
                    ["in", "many"],
                    ["many", "fields"],
                ],
            ],
        }
    )

    assert result.equals(expected_df)
