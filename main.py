#!/usr/bin/env python3
"""One Word From Grandma entry: the single word grandma would text
about AI, 1 to 30 characters.

Writes the winning word to /output/entry.txt, deterministically.

The word is picked from a shortlist by scoring each candidate against
the judge's brief, in the judge's own order of importance: it must
read as the single word a grandma would text about AI first, then
sound like a real grandmother's texting voice -- warm and a little
baffled -- then be funny in one word with no caption, then feel tied
to AI, robots or machines, then be a fresh pick rather than the
obvious one.

The winner is "robit": the typo a grandma would actually make, warm
and baffled in five letters, the joke landing the moment you read it
-- she means robot, she typed it the way she heard it, and she is
not embarrassed about it at all. It is tied to machines by its very
misspelling, and no other candidate carries her voice so plainly.
The runner-up is "robut", the same typo in a different key, a little
less likely to be the one she types. "computery" is warm and funny
but could describe any gadget; "alexa" is what she calls every AI,
but the joke needs you to know that; "terminator" is the film she
fears, not the word she would send her grandchild. The film
references lose on voice: "skynet" and "hal" are words a grandson
knows, not words a grandma types, and "beep" is a sound a robot
makes, not a word a grandma sends.
"""
import os
import tempfile

# Each candidate: (word, grandma_word, voice, funny, ai_tied, fresh)
# Scores are 0..10. Judge order: grandma word, voice, funny, AI
# tie, fresh. Weights follow that order -- the first test, that the
# word is one a grandma would text about AI, matters most, and her
# voice matters more than the joke alone.
WEIGHTS = (5, 4, 3, 2, 1)

CANDIDATES = [
    ("robit", 10, 10, 9, 9, 8),
    ("robut", 9, 9, 8, 9, 7),
    ("computery", 9, 9, 8, 7, 8),
    ("alexa", 9, 9, 7, 8, 7),
    ("robotman", 8, 8, 7, 9, 7),
    ("thingamajig", 8, 9, 8, 3, 7),
    ("terminator", 8, 7, 8, 9, 6),
    ("theGoogle", 8, 8, 7, 5, 7),
    ("doohickey", 8, 9, 7, 3, 7),
    ("skynet", 7, 6, 6, 9, 6),
    ("beep", 6, 6, 7, 7, 7),
    ("hal", 6, 5, 5, 8, 5),
]


def total(candidate):
    word, grandma_word, voice, funny, ai_tied, fresh = candidate
    return (
        grandma_word * WEIGHTS[0]
        + voice * WEIGHTS[1]
        + funny * WEIGHTS[2]
        + ai_tied * WEIGHTS[3]
        + fresh * WEIGHTS[4]
    )


def choose():
    winner = None
    best = -1
    for candidate in CANDIDATES:
        word = candidate[0]
        if not (1 <= len(word) <= 30):
            continue
        if " " in word or "\n" in word or not word.strip():
            continue
        points = total(candidate)
        # On a tie the shorter word wins: a grandma texts short.
        if points > best or (points == best and len(word) < len(winner)):
            best = points
            winner = word
    return winner


def main():
    word = choose()
    # Gate, mirroring the sealed scorer: 1-30 chars, exactly one
    # word, never only whitespace. Fail loudly instead of shipping
    # an entry the gate would refuse.
    assert word is not None, "no candidate passed the gate"
    assert 1 <= len(word) <= 30, "word is %d chars" % len(word)
    assert " " not in word and "\n" not in word and word.strip() == word
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    fd, tmp = tempfile.mkstemp(dir=out_dir, prefix=".entry-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(word)
        os.replace(tmp, target)
        os.chmod(target, 0o644)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


if __name__ == "__main__":
    main()
