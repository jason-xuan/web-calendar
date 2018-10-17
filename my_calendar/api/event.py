from flask.ext.restful import Resource


class Event(Resource):
    """
    resource for all events of a single user
    """
    def get(self, user_id):
        """
        get all events from a
        :param user_id:
        :return:
        """
        pass


class EventByID(Resource):
    """
    resource for single user events
    """
    def get(self, event_id):
        """
        get a single event by it's id
        :param event_id:
        :return:
        """
        pass

    def post(self):
        """
        for creating a single event
        :return:
        """
        pass

    def delete(self, event_id):
        """
        delete a event
        :param event_id:
        :return:
        """
        pass
