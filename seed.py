from models import *
from app import app

db.drop_all()
db.create_all()

# u1 = User(username="bobo", password="bcrypt.generate_password_hash(test)",
#           email="scottkoons@gmail.com")
# p1 = Product(name="ducky",
#              price=9999,
#              stock=5,
#              description="you love ducky mo-mo",
#              image="https://media.tumblr.com/tumblr_lqjdbeTyqO1qdww83.jpg")

# p2 = Product(
#     name="Flash Gordon",
#     price=5999,
#     stock=15,
#     description="king of impossible",
#     image="https://i.ebayimg.com/images/g/fucAAOSwY3hdiQAK/s-l400.jpg")

# db.session.add_all([p1, p2])
# db.session.add(u1)
# db.session.commit()
