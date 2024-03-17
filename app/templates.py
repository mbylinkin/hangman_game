from __future__ import annotations

template_round = """
    Round:{{round}}
    +---+
    |   |      Word: {{current_word}}
  {{head}} |    Errors: {{errors}}
  {{body}} |    Letter: {{letter}}
  {{legs}} |
        |
    =======
    -------------------------------------------------------------------------------------
    """

head_ascii = {
    0: '     ',
    1: '  O  ',
    2: '  O  ',
    3: '  O  ',
    4: '  O  ',
    5: '  O  ',
    6: '  O  ',
}

body_ascii = {
    0: '     ',
    1: '     ',
    2: '  |  ',
    3: '  /| ',
    4: '  /|\\',
    5: '  /|\\',
    6: '  /|\\',
}
legs_ascii = {
    0: '     ',
    1: '     ',
    2: '     ',
    3: '     ',
    4: '     ',
    5: '  /  ',
    6: '  / \\',
}

template_game_over = """
=====================================================================================
                                   GAME OVER!
                                   {{message}}

   Secret word:  {{secret_word}}
   Current word: {{current_word}}
   Round:        {{round}}
=====================================================================================
"""
