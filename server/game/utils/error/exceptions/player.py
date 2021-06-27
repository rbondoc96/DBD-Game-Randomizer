class PlayerImproperlyConfigured(Exception):

    def __str__(self):
        return "Player was not configured correctly."