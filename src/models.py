from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Table, Column, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
import enum 

db = SQLAlchemy()

class TypeMedia(enum.Enum):
    VIDEO = "video"
    IMAGE = "image"


association_table = Table(
    "association",
    db.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("follower_id", ForeignKey("follower.id"), primary_key=True)
)

class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    firtsname: Mapped[str] = mapped_column(String(50), nullable=False)
    lastname: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)

    followers: Mapped[List["Follower"]] = relationship(
        "Follower",
        secondary=association_table, back_populates="usertwo")
    posts: Mapped[List["Post"]] = relationship(
        back_populates="user_post")
    digitalmedia: Mapped[List["Media"]] = relationship(
        back_populates="user_media")
    comments: Mapped[List["Comment"]] = relationship(
        back_populates="comment_user")

class Follower(db.Model):
    __tablename__ = "follower"

    id: Mapped[int] = mapped_column(primary_key=True)

    usertwo: Mapped[List["User"]] = relationship(
        "User",
        secondary=association_table, back_populates="followers")

class Post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user_post: Mapped["User"] = relationship(
        back_populates="posts")
    list_media: Mapped[List["Media"]] = relationship(
        back_populates="post_media")
    list_comment: Mapped[List["Comment"]] = relationship(
        back_populates="comment_post")

class Media(db.Model):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[enum] = mapped_column(Enum(TypeMedia), nullable=False)
    url: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))

    user_media: Mapped["User"] = relationship(
        back_populates="digitalmedia")
    post_media: Mapped["Post"] = relationship(
        back_populates="list_media")

class Comment(db.Model):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(2000), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))

    comment_post: Mapped["Post"] = relationship(
        back_populates="list_commment")
    comment_user: Mapped["User"] = relationship(
        back_populates="comments")
