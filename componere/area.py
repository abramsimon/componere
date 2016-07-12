class Area:
	identifier = None
	name = None
	parent_identifier = None

	def __init__(self, identifier, name=None, parent_identifier=None):
		self.identifier = identifier
		self.name = name
		self.parent_identifier = parent_identifier

	@classmethod
	def from_values_dict(cls, identifier, values_dict):
		if values_dict is None:
			return None
		identifier = identifier
		name = values_dict.get("name")
		parent_identifier = values_dict.get("parent")
		return Area(identifier, name, parent_identifier)

	@classmethod
	def from_collection_dict(cls, collection_dict):
		if collection_dict is None:
			return None

		dict = {}
		for identifier, values_dict in collection_dict.iteritems():
			object = Area.from_values_dict(identifier, values_dict)
			dict[identifier] = object
		return dict
