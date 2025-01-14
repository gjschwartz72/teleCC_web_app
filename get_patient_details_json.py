from orm_models import Patient_telecc_state, Patient_telecc_history
from web_app import app, db
from flask import jsonify

def get_patient_details_json(patient_id):
    """
    Endpoint to fetch detailed information about a specific patient.
    """
    
    # Query the database for the patient details based on patient_id
    patient = db.session.query(Patient_telecc_state).filter(Patient_telecc_state.patientID == patient_id).first()

    patient_hist = (
        db.session.query(Patient_telecc_history).
        filter(Patient_telecc_history.patientID == patient_id).
        order_by(Patient_telecc_history.prediction_datetime.asc()).
        all()
    )

    if not patient:
        return jsonify({'error': 'Patient not found'}), 404

    # Prepare the response data
    response_data = {
        'patient_id': patient.patientID,
        'patient_name': patient.patientName,
        'room': patient.room,
        'prediction_datetime': patient.prediction_datetime.strftime('%m-%d-%Y %I:%M %p'),
        'septic_shock_class': 'Low' if patient.septic_shock_class == 1 else 'Moderate' if patient.septic_shock_class == 2 else 'Critical',
        'septic_shock_score': round(patient.septic_shock_score, 2),
        'septic_shock_protocol': 'Line 1\nLine 2\nLine 3\nLine 4',

        'septic_shock_expl': {
            f'{prefix}_{i}': (
                    getattr(patient, f'septic_shock_expl_field_{prefix}_{i}', None),  # Dynamically construct field name
                    getattr(patient, f'septic_shock_expl_val_{prefix}_{i}', None)
                )
                for prefix in ['pos', 'neg']  # Iterate over prefixes
                for i in range(1, 4)          # Iterate over indices
        },   

        'respiratory_class': 'Low' if patient.respiratory_class == 1 else 'Moderate' if patient.respiratory_class == 2 else 'Critical',
        'respiratory_score': round(patient.respiratory_score, 2),
        'respiratory_protocol': 'Line A\nLine B\nLine C\nLine D',

        'respiratory_expl': {
            f'{prefix}_{i}': (
                    getattr(patient, f'respiratory_expl_field_{prefix}_{i}', None),  # Dynamically construct field name
                    getattr(patient, f'respiratory_expl_val_{prefix}_{i}', None)
                )
                for prefix in ['pos', 'neg']  # Iterate over prefixes
                for i in range(1, 4)          # Iterate over indices
        }, 

        'septic_shock_history': [{
            "dateTime": record.prediction_datetime.isoformat(),
            "value": round(record.septic_shock_score, 2)
            }
            for record in patient_hist
        ],
        'respiratory_history': [{
            "dateTime": record.prediction_datetime.isoformat(),
            "value": round(record.respiratory_score, 2)
            }
            for record in patient_hist
        ]


    }

    return jsonify(response_data)