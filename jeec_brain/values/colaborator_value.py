from jeec_brain.values.value_composite import ValueComposite


class ColaboratorValue(ValueComposite):
	def __init__(self, colaborator):
		super(ColaboratorValue, self).initialize({})
		self.serialize_with(name=colaborator.name)
		self.serialize_with(istid=colaborator.istid)
		self.serialize_with(team=colaborator.team)
		self.serialize_with(linkedin_url=colaborator.linkedin_url)
