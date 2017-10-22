class Projects(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	description = db.Column(db.String(100), unique=True)

	def __init__(self, name, description):
		self.name = name
		self.description = description

	def __repr__(self):
		return '<Name %r>' % self.name