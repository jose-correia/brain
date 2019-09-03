from jeec_brain.values.value_composite import ValueComposite


class APIErrorValue(ValueComposite):
    """Used to represent an error that might occur in the API.

    Attributes:
        error_message: A string describing the error message
    """

    def __init__(self, error_message):
        super(APIErrorValue, self).initialize({})
        self.serialize_with(error=error_message)
