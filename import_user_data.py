import csv
import os

from dotenv import load_dotenv

from app import User

load_dotenv()


def get_users_from_csv(csv_file_path):
    try:
        with open(csv_file_path, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  # Ignoring first row from csv file

            users_to_import = []
            for row in csv_reader:
                first_name, last_name, email = row

                users_to_import.append(
                    dict(
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                    )
                )

            return users_to_import

    except FileNotFoundError:
        print(f"CSV file '{csv_file_path}' not found.")


def insert_users_to_db(users: list):
    from flask import Flask
    from app import db

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")

    db.init_app(app)

    with app.app_context():

        try:
            for user in users:
                # Check if the email already exists in the database
                if User.query.filter_by(email=user.get("email")).first():
                    print(f"User with email '{user.get('email')}' already exists. Skipping...")
                    continue

                new_user = User(
                    firstname=user.get("first_name"),
                    lastname=user.get("last_name"),
                    email=user.get("email")
                )
                db.session.add(new_user)

            db.session.commit()
            print("Data imported successfully!")

        except Exception as e:
            db.session.rollback()
            print("Error occurred while importing data:", str(e))


if __name__ == "__main__":
    file_path = input("Please enter peth to file: ")
    users = get_users_from_csv(file_path)
    insert_users_to_db(users)
