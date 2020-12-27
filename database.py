import sqlite3

def init():

    conn = sqlite3.connect('audio.db')

    db = conn.cursor()

    # db.execute('CREATE TABLE Student (id integer PRIMARY KEY autoincrement, Name varchar(30), Age integer)')
    try: 
        db.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER NOT NULL,
            name CHAR(128),
            gender CHAR,
            city CHAR(128),
            wechat_id CHAR(128),
            PRIMARY KEY (user_id AUTOINCREMENT)
        )
        """
        )

        conn.commit()

    except:
        conn.rollback()

    try: 
        db.execute(
        """
        CREATE TABLE IF NOT EXISTS audio (
            audio_id INT AUTO_INCREMENT PRIMARY KEY,
            audio_filename CHAR(128),
            accuracy FLOAT,
            user_id FOREIGN KEY REFERENCES users(user_id) 
        """
        )

        conn.commit()

    except:
        conn.rollback()

    conn.close()


def add_user(name, gender, city, wechat_id):

    conn = sqlite3.connect('audio.db')

    db = conn.cursor()

    db.execute("INSERT INTO users (name, gender, city, wechat_id) VALUES (?, ?, ?, ?)", (name, gender, city, wechat_id))

    conn.commit()
    conn.close()


def add_audio(audio_filename, accuracy):

    conn = sqlite3.connect('audio.db')

    db = conn.cursor()

    db.execute("INSERT INTO audio (audio_filename, accuracy) VALUES (?, ?)", (audio_filename, accuracy))

    conn.commit()
    conn.close()

init()
add_user("Robert", 'M', "Shanghai", "robert20040506")