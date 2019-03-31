from app import db

class Device(db.Model):
    __tablename__ = 'Device'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    text = db.Column(db.PickleType())
    current = db.Column(db.Integer, default=0) # current page of device

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, text):
        self.text = text
        self.current = 0
        db.session.commit()

    def page(self): # get current page
        data = str(self.text[self.current])
        return data.replace(', ', '')[1:-1]

    def next_page(self): # 다음 페이지
        try: 
            self.text[self.current + 1]
            self.current += 1
            db.session.commit()
            return True
        except IndexError:
            return False

    def prev_page(self): # 이전 페이지 
        try: 
            self.text[self.current - 1]
            self.current -= 1
            db.session.commit()
            return True
        except IndexError:
            return False
