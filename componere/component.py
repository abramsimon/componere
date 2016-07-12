class Component:
	identifier = None
	name = None
	level_identifier = None
	type = None
	team_identifier = None
	area_identifier = None
	description = None
	git = None
	release_date = None
	dependency_identifiers = None

	def __init__(
		self,
		identifier,
		name=None,
		level_identifier=None,
		type=None,
		team_identifier=None,
		area_identifier=None,
		description=None,
		git=None,
		release_date=None,
		dependency_identifiers=None
	):
		self.identifier = identifier
		self.name = name
		self.level_identifier = level_identifier
		self.type = type
		self.team_identifier = team_identifier
		self.area_identifier = area_identifier
		self.description = description
		self.git = git
		self.release_date = release_date
		self.dependency_identifiers = dependency_identifiers

	@classmethod
	def from_values_dict(cls, identifier, values_dict):
		if values_dict is None:
			return None
		name = values_dict.get("name")
		level = values_dict.get("level")
		type = values_dict.get("type")
		team_identifier = values_dict.get("team")
		area_identifier = values_dict.get("area")
		description = values_dict.get("description")
		git = values_dict.get("git")
		release_date = values_dict.get("release-date")
		dependency_identifiers = values_dict.get("dependencies")

		return Component(
			identifier,
			name,
			level,
			type,
			team_identifier,
			area_identifier,
			description,
			git,
			release_date,
			dependency_identifiers
		)

	@classmethod
	def from_collection_dict(cls, collection_dict):
		if collection_dict is None:
			return None

		dict = {}
		for identifier, values_dict in collection_dict.iteritems():
			object = Component.from_values_dict(identifier, values_dict)
			dict[identifier] = object
		return dict
