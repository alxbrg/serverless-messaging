def find_by_recipient(recipient):
    return [{'recipient': recipient}]


def create(recipient, body, email_address=None, phone_number=None):
    return {'recipient': recipient}
