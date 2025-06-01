from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from enum import Enum

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


association_table = Table(
    "association",
    db.metadata,
    Column("users_id", ForeignKey("users.id"), primary_key=True),
    Column("follower_id", ForeignKey("follower.id"), primary_key=True)
)


class Users(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    firtsname: Mapped[str] = mapped_column(String(50), nullable=False)
    lastname: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)

    followers: Mapped[List["Follower"]] = relationship(
        "Follower",
        secondary=association_table,
        back_populates="userstwo"
    )
    posts: Mapped[List["Post"]] = relationship(
        back_populates="users_post"
    )
    digitalmedia: Mapped[List["Media"]] = relationship(
        back_populates="users_media"
    )
    comments: Mapped[List["Comment"]] = relationship(
        back_populates="comment_users"
    )


class Follower(db.Model):
    __tablename__ = "follower"

    id: Mapped[int] = mapped_column(primary_key=True)

    userstwo: Mapped[List["Users"]] = relationship(
        "Users",
        secondary=association_table,
        back_populates="followers"
    )


class Post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    users_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    users_post: Mapped["Users"] = relationship(
        back_populates="posts"
    )
    list_media: Mapped[List["Media"]] = relationship(
        back_populates="post_media"
    )
    list_comment: Mapped[List["Comment"]] = relationship(
        back_populates="comment_post"
    )


class Media(db.Model):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))

    users_media: Mapped["Users"] = relationship(
        back_populates="digitalmedia"
    )
    post_media: Mapped["Post"] = relationship(
        back_populates="list_media"
    )


class Comment(db.Model):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(2000), nullable=False)
    users_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))

    comment_post: Mapped["Post"] = relationship(
        back_populates="list_commment"
    )
    comment_users: Mapped["Users"] = relationship(
        back_populates="comments"
    )
