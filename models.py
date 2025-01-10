from web_app import db

class Patient_telecc_state(db.Model):
    __tablename__ = 'patient_telecc_state'

    patientID = db.Column(db.Integer, primary_key = True)
    room = db.Column(db.Integer)
    station_number = db.Column(db.Integer, primary_key = True)
    patientName = db.Column(db.Text)
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

    # def __repr__(self):
    #     return f'PatientID, Sta6a, prediction_datetime, respiratory_score, septic_shock\n{self.PatientID}, {self.Sta6a}, {self.prediction_datetime}, {self.respiratory_score}, {self.septic_shock_score}>'

class Patient_telecc_history(db.Model):

    __tablename__ = 'patient_teleCC_history'

    PatientID = db.Column(db.Integer, primary_key = True)
    Sta6a = db.Column(db.Integer)
    prediction_datetime = db.Column(db.DateTime, primary_key = True)
    septic_shock_score = db.Column(db.Float)
    respiratory_score = db.Column(db.Float)

class Station_lookup(db.Model):

    __tablename__ = 'station_lookup'

    station_number = db.Column(db.Integer, primary_key=True)
    station_name = db.Column(db.Text)
