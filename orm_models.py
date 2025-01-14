from web_app import db

class Patient_telecc_state(db.Model):

    __tablename__ = 'patient_teleCC_state'

    patientID = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.Integer)
    station_number = db.Column(db.Integer, primary_key=True)
    patientName = db.Column(db.Text)
    Trial_ARM = db.Column(db.Integer)
    prediction_datetime = db.Column(db.DateTime)
    respiratory_score = db.Column(db.Float)
    respiratory_class = db.Column(db.Integer)
    respiratory_trend = db.Column(db.Integer)
    septic_shock_score = db.Column(db.Float)
    septic_shock_class = db.Column(db.Integer)
    septic_shock_trend = db.Column(db.Integer)
    septic_shock_expl_val_pos_1 = db.Column(db.Float)
    septic_shock_expl_val_pos_2 = db.Column(db.Float)
    septic_shock_expl_val_pos_3 = db.Column(db.Float)
    septic_shock_expl_val_neg_1 = db.Column(db.Float)
    septic_shock_expl_val_neg_2 = db.Column(db.Float)
    septic_shock_expl_val_neg_3 = db.Column(db.Float)
    respiratory_expl_val_pos_1 = db.Column(db.Float)
    respiratory_expl_val_pos_2 = db.Column(db.Float)
    respiratory_expl_val_pos_3 = db.Column(db.Float)
    respiratory_expl_val_neg_1 = db.Column(db.Float)
    respiratory_expl_val_neg_2 = db.Column(db.Float)
    respiratory_expl_val_neg_3 = db.Column(db.Float)
    septic_shock_expl_field_pos_1 = db.Column(db.Text)
    septic_shock_expl_field_pos_2 = db.Column(db.Text)
    septic_shock_expl_field_pos_3 = db.Column(db.Text)
    septic_shock_expl_field_neg_1 = db.Column(db.Text)
    septic_shock_expl_field_neg_2 = db.Column(db.Text)
    septic_shock_expl_field_neg_3 = db.Column(db.Text)
    respiratory_expl_field_pos_1 = db.Column(db.Text)
    respiratory_expl_field_pos_2 = db.Column(db.Text)
    respiratory_expl_field_pos_3 = db.Column(db.Text)
    respiratory_expl_field_neg_1 = db.Column(db.Text)
    respiratory_expl_field_neg_2 = db.Column(db.Text)
    respiratory_expl_field_neg_3 = db.Column(db.Text)

class Patient_telecc_history(db.Model):

    __tablename__ = 'patient_teleCC_history'

    patientID = db.Column(db.Integer, primary_key = True)
    station_number = db.Column(db.Integer)
    prediction_datetime = db.Column(db.DateTime, primary_key = True)
    septic_shock_score = db.Column(db.Float)
    respiratory_score = db.Column(db.Float)


class Station_lookup(db.Model):

    __tablename__ = 'station_lookup'

    station_number = db.Column(db.Integer, primary_key=True)
    station_name = db.Column(db.Text)