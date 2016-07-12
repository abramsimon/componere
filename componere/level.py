class Level:
    identifier = None
    order = None
    name = None

    def __init__(self, identifier, order=None, name=None):
        self.identifier = identifier
        self.order = order
        self.name = name

    @classmethod
    def from_values_dict(cls, identifier, values_dict):
    	if values_dict is None:
    		return None
    	order = values_dict.get("order")
    	name = values_dict.get("name")
    	return Level(identifier, order, name)

    @classmethod
    def from_collection_dict(cls, collection_dict):
    	if collection_dict is None:
    		return None

    	dict = {}
    	for identifier, values_dict in collection_dict.iteritems():
    		object = Level.from_values_dict(identifier, values_dict)
    		dict[identifier] = object
    	return dict
