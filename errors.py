class Error(Exception):
    "Base class for exceptions"
    pass


class parsing_table_error(Error):
    "raised when T[X,t] possess more than one production"

    def __init__(self, production1, production2, invalid_sentence):
        Error.__init__(
            self,
            f"conflict betweeen {production1}  and {production2}, invalid sentence: {invalid_sentence}",
        )


class shift_reduce_error(Error):
    "raised when goto or action table in shift reduce parsers possess more than one production"

    def __init__(self, action1, action2, grammar, key=None):
        if action1[0] == action2[0] == "REDUCE":
            conflict = "Reduce-Reduce"
        else:
            conflict = "Shift-Reduce"

        Error.__init__(
            self,
            f"When analizing {key}, {conflict} conflict!!! betweeen {action1}  and {action2}. Grammar given is not {grammar}",
        )


class invalid_sentence_error(Error):
    "raised when w is not in G"

    def __init__(
        self,
        w,
        pos,
        actual_token,
        expected_token=None,
        message="",
        output=None,
        operations=None,
    ):
        if expected_token != None:
            Error.__init__(
                self,
                f"Invalid sentence {w}. Expected {expected_token} at position {pos} but received {actual_token} instead. {message}",
            )
        else:
            Error.__init__(
                self,
                f"Unexpected token {actual_token} at position {pos}. Invalid sentence {w}. {message}. Secuencia de derivaciones: {output}. Operaciones: {operations}",
            )


class non_regular_production_error(Error):
    def __init__(self, production):
        Error.__init__(
            self,
            f"production {production} most be of the form: A -> a, A -> e or A -> aX",
        )
