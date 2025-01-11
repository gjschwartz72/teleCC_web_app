from web_app import app, db
from flask import render_template, request, jsonify, url_for, redirect
from models import Patient_telecc_state, Patient_telecc_history, Station_lookup
from forms import StationSelectionForm

# Cache for storing loaded data
cache = {}

@app.route("/", methods=["GET", "POST"])
def splash():
    """Render the splash screen and handle station selection."""
    form = StationSelectionForm()
    
    # Dynamically populate the SelectField with station data
    #form.station_id.choices = [(station.station_number, station.station_name) for station in Station_lookup.query.all()]
    form.stations = Station_lookup.query.all()

    if form.validate_on_submit():
        # Redirect to load_data route with the selected station ID
        station_id = form.station_id.data
        return redirect(url_for("load_data", station_id=station_id))

    return render_template("splash.html", form=form)

@app.route('/load_data/<int:station_id>')
def load_data(station_id):
    #station_id = request.args.get('station_id')
    # Handle the station_id as needed

    # Use the station name from the first patient (replace with actual logic)
    station = Station_lookup.query.filter_by(station_number = station_id).all()
    station_name = station[0].station_name
 
    # Render the table template
    station_list = Patient_telecc_state.query.filter_by(station_number = station_id).all()
    if station_list:
        prediction_datetime = station_list[0].prediction_datetime
        station_list_sorted = sorted(station_list, key=lambda p: p.patientName.split()[-1])
    else:
        prediction_datetime = None

    return render_template(
        'patient_list.html',
        station_name=station_name,
        patients=station_list_sorted,
        prediction_datetime = prediction_datetime
    )

    
    return f"Loading data for station: {station_id}, {len(station_list)}"

# @app.route("/load_data", methods=["GET", "POST"])
# def load_data():
#     """Handle station selection and initialize the main page."""
#     # Ensure station exists
#     station_id = request.args.get('station_id')
#     station = Station_lookup.query.get(station_id)
#     if not station:
#         return jsonify({"error": "Station not found"}), 404

#     print("Select Station:", station)
#     return ("Selection:", station)
#     # Redirect to the main page with the selected station
#     #return render_template("main.html", station=station)


# @app.route('/main', methods=['GET', 'POST'])
# def main():
#     stations = Station_lookup.query.all()
#     return render_template('main.html', stations=stations)

# @app.route('/load_data', methods=['POST'])
# def load_data():
#     station_id = request.json.get('station_id')

#     if station_id in cache:
#         data = cache[station_id]
#     else:
#         state_data = PatientTeleCCState.query.filter_by(station_id=station_id).all()
#         history_data = PatientTeleCCHistory.query.filter_by(station_id=station_id).all()

#         data = {
#             'state': [state.to_dict() for state in state_data],
#             'history': [history.to_dict() for history in history_data]
#         }
#         cache[station_id] = data

#     return jsonify(data)

# @app.route('/patient_details/<int:patient_id>', methods=['GET'])
# def patient_details(patient_id):
#     patient_state = PatientTeleCCState.query.get(patient_id)
#     patient_history = PatientTeleCCHistory.query.filter_by(patient_id=patient_id).all()

#     if patient_state:
#         response = {
#             'state': patient_state.to_dict(),
#             'history': [entry.to_dict() for entry in patient_history]
#         }
#         return jsonify(response)
#     return jsonify({'error': 'Patient not found'}), 404