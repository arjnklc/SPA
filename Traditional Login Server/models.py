from app import db

# User model. It contains id which is primary key and auto increment, username and K
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    K = db.Column(db.String(1200), index=True, unique=False)

    def __repr__(self):
        return "id: {0} username: {1} K: {2} \n".format(self.id, self.username, self.K)
