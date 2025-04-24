import streamlit_authenticator as stauth

# Définir les utilisateurs
names = ['Admin', 'Viewer']
usernames = ['admin', 'viewer']
passwords = ['adminpass', 'viewerpass']  # à hacher en prod

hashed_passwords = stauth.Hasher(passwords).generate()

credentials = {
    "usernames": {
        usernames[i]: {"name": names[i], "password": hashed_passwords[i]}
        for i in range(len(usernames))
    }
}
