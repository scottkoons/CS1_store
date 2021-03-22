from models import *
from app import app

db.drop_all()
db.create_all()

product1 = Product(name='Happy Fun Ball', price=1000, stock=10, description="It's happy, it's fun... It's HAPPY FUN BALL!",
                   image='https://upload.wikimedia.org/wikipedia/en/thumb/6/65/Happy_fun_ball.jpg/300px-Happy_fun_ball.jpg')
db.session.add(product1)

product2 = Product(name='Bobo Socks', price=4949, stock=5, description="These are the socks worn by Bobo The Monkey Boy",
                   image='http://127.0.0.1:5000/_uploads/images/bobo-socks_1.jpeg')
db.session.add(product2)

product3 = Product(name='Flash Gordon Wig', price=10099, stock=25, description="The wig is just plain HOT. Now you can become the saviour of the universe!",
                   image='http://127.0.0.1:5000/_uploads/images/flash_gordon_wig_1.jpeg')
db.session.add(product3)

product4 = Product(name='Cool T-Shirt', price=2400, stock=15, description="OLE '59ER AMBER ALE™ T-SHIRT",
                   image='http://0.0.0.0:5000/_uploads/images/ole59er-front.jpeg')
db.session.add(product4)


db.session.commit()
