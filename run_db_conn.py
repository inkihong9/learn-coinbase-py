from db_conn import User, SessionLocal

def main():
    session = SessionLocal()

    # Add new user
    new_user = User(name="user", email="user@example.com")
    session.add(new_user)
    session.commit()

    # Query
    users = session.query(User).all()
    for u in users:
        print(f"{u.id} - {u.name} ({u.email})")

    session.close()

if __name__ == "__main__":
    main()
