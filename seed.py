"""Seeding files for sample users"""

from models import db, User, Post, Tag, PostTag
from app import app

# Create all tables
with app.app_context():
    db.drop_all()
    db.create_all()


# Add Users
daniel = User(first_name="Daniel", last_name="Louise",
              image_url="https://semantic-ui.com/images/avatar/small/daniel.jpg")

stevie = User(first_name="Stevie", last_name="Feliciano",
              image_url="https://semantic-ui.com/images/avatar/small/stevie.jpg")

elliot = User(first_name="Elliot", last_name="Fu",
              image_url="https://semantic-ui.com/images/avatar/small/elliot.jpg")

helen = User(first_name="Helen", last_name="Chris",
             image_url="https://semantic-ui.com/images/avatar/small/helen.jpg")

# Add them to the db session
db.session.add(daniel)
db.session.add(stevie)
db.session.add(elliot)
db.session.add(helen)

# Commit them to the db
db.session.commit()

# Add posts
post1 = Post(title="His mother had always taught him", content="His mother had always taught him not to ever think of himself as better than others. He'd tried to live by this motto. He never looked down on those who were less fortunate or who had less money than him. But the stupidity of the group of people he was talking to made him change his mind.", user_id=1)

post2 = Post(title="He was an expert but not in a discipline", content="He was an expert but not in a discipline that anyone could fully appreciate. He knew how to hold the cone just right so that the soft server ice-cream fell into it at the precise angle to form a perfect cone each and every time. It had taken years to perfect and he could now do it without even putting any thought behind it.", user_id=2)

post3 = Post(title="Dave watched as the forest burned up on the hill", content="Dave watched as the forest burned up on the hill, only a few miles from her house. The car had been hastily packed and Marta was inside trying to round up the last of the pets. Dave went through his mental list of the most important papers and documents that they couldn't leave behind. He scolded himself for not having prepared these better in advance and hoped that he had remembered everything that was needed. He continued to wait for Marta to appear with the pets, but she still was nowhere to be seen.", user_id=3)

post4 = Post(title="All he wanted was a candy bar", content="All he wanted was a candy bar. It didn't seem like a difficult request to comprehend, but the clerk remained frozen and didn't seem to want to honor the request. It might have had something to do with the gun pointed at his face.", user_id=3)

post5 = Post(title="Hopes and dreams were dashed that day",
             content="Hopes and dreams were dashed that day. It should have been expected, but it still came as a shock. The warning signs had been ignored in favor of the possibility, however remote, that it could actually happen. That possibility had grown from hope to an undeniable belief it must be destiny. That was until it wasn't and the hopes and dreams came crashing down.", user_id=4)

db.session.add(post1)
db.session.add(post2)
db.session.add(post3)
db.session.add(post4)
db.session.add(post5)

db.session.commit()

# Add Tags
history = Tag(name="history")
english = Tag(name="english")
mystery = Tag(name="mystery")
american = Tag(name="american")
crime = Tag(name="crime")

db.session.add(history)
db.session.add(english)
db.session.add(mystery)
db.session.add(american)
db.session.add(crime)

db.session.commit()

# Add Posts and Tags Relationships
detail1 = PostTag(post_id=1, tag_id=1)
detail2 = PostTag(post_id=1, tag_id=4)
detail3 = PostTag(post_id=2, tag_id=2)
detail4 = PostTag(post_id=3, tag_id=1)
detail5 = PostTag(post_id=4, tag_id=3)
detail6 = PostTag(post_id=4, tag_id=2)
detail7 = PostTag(post_id=4, tag_id=4)
detail8 = PostTag(post_id=5, tag_id=5)
detail9 = PostTag(post_id=5, tag_id=1)
detail10 = PostTag(post_id=1, tag_id=5)

db.session.add_all(
    [detail1, detail2, detail3, detail4, detail5, detail6, detail7, detail8, detail9, detail10])
db.session.commit()
