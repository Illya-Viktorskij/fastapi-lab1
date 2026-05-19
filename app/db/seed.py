import asyncio
import sys
sys.path.append("/app")

from app.database import AsyncSessionLocal
from app.models.models import User, Profile, Category, Post, Comment


async def seed():
    async with AsyncSessionLocal() as db:
        # Users
        user1 = User(name="Alice", email="alice@example.com", age=25)
        user2 = User(name="Bob", email="bob@example.com", age=30)
        user3 = User(name="Charlie", email="charlie@example.com", age=22)
        db.add_all([user1, user2, user3])
        await db.flush()

        # Profiles
        p1 = Profile(user_id=user1.id, bio="Python developer", avatar_url="https://i.pravatar.cc/150?u=alice")
        p2 = Profile(user_id=user2.id, bio="DevOps engineer", avatar_url="https://i.pravatar.cc/150?u=bob")
        p3 = Profile(user_id=user3.id, bio="Student", avatar_url="https://i.pravatar.cc/150?u=charlie")
        db.add_all([p1, p2, p3])
        await db.flush()

        # Categories
        cat1 = Category(name="Technology", description="Tech news and tutorials")
        cat2 = Category(name="Science", description="Science articles")
        cat3 = Category(name="Gaming", description="Games and reviews")
        db.add_all([cat1, cat2, cat3])
        await db.flush()

        # Posts
        post1 = Post(title="FastAPI Tutorial", content="FastAPI is awesome...", user_id=user1.id, category_id=cat1.id)
        post2 = Post(title="Docker basics", content="Docker simplifies deployment...", user_id=user1.id, category_id=cat1.id)
        post3 = Post(title="Black holes explained", content="A black hole is...", user_id=user2.id, category_id=cat2.id)
        post4 = Post(title="Top games 2024", content="Here are the best games...", user_id=user3.id, category_id=cat3.id)
        post5 = Post(title="Python tips", content="Some useful Python tricks...", user_id=user2.id, category_id=cat1.id)
        db.add_all([post1, post2, post3, post4, post5])
        await db.flush()

        # Comments
        c1 = Comment(content="Great article!", user_id=user2.id, post_id=post1.id)
        c2 = Comment(content="Very helpful, thanks!", user_id=user3.id, post_id=post1.id)
        c3 = Comment(content="Interesting read", user_id=user1.id, post_id=post3.id)
        c4 = Comment(content="I love this game!", user_id=user2.id, post_id=post4.id)
        c5 = Comment(content="Nice tips!", user_id=user3.id, post_id=post5.id)
        db.add_all([c1, c2, c3, c4, c5])

        await db.commit()
        print("✅ Seed completed successfully!")


if __name__ == "__main__":
    asyncio.run(seed())