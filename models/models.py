from app import db

class Patient_telecc_state(db.Model):
    PatientID = db.Column(db.Integer)
    room = db.Column(db.Integer)
    Sta6a = db.Column(db.Integer)
    PatientName = db.Column(db.Text)
    Trial_ARM = db.Column(db.Integer)
    prediction_datetime = db.Column(db.DateTime)
    respiratory_score = db.Column(db.Float)
    respiratory_class = db.Column(db.Integer)
    respiratory_trend = db.Column(db.Integer)
    septic_shock_score = db.Column(db.Float)
    septic_shock_class = db.Column(db.Integer)
    septic_shock_trend = db.Column(db.Integer)
    septic_shock_score_expl_pos_1 = db.Column(db.Float)
    septic_shock_score_expl_pos_2 = db.Column(db.Float)
    septic_shock_score_expl_pos_3 = db.Column(db.Float)
    septic_shock_score_expl_neg_1 = db.Column(db.Float)
    septic_shock_score_expl_neg_2 = db.Column(db.Float)
    septic_shock_score_expl_neg_3 = db.Column(db.Float)
    respitory_score_expl_pos_1 = db.Column(db.Float)
    respitory_score_expl_pos_2 = db.Column(db.Float)
    respitory_score_expl_pos_3 = db.Column(db.Float)
    respitory_score_expl_neg_1 = db.Column(db.Float)
    respitory_score_expl_neg_2 = db.Column(db.Float)
    respitory_score_expl_neg_3 = db.Column(db.Float)

    def __repr__(self):
        return f'PatientID, Sta6a, prediction_datetime, respiratory_score, septic_shock\n{self.PatientID}, {self.Sta6a}, {self.prediction_datetime}, {self.respiratory_score}, {self.septic_shock_score}>'