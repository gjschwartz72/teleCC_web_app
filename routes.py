from web_app import app, db
from flask import render_template, request, jsonify, url_for, redirect
from orm_models import Patient_telecc_state, Patient_telecc_history, Station_lookup
from forms import StationSelectionForm
from get_patient_details_json import get_patient_details_json


# Cache for storing loaded data
cache = {}

@app.route("/index", methods = ["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def splash():
    """Render the splash screen and handle station selection."""
    form = StationSelectionForm()
    
    # Dynamically populate the SelectField with station data
    #form.station_id.choices = [(station.station_number, station.station_name) for station in Station_lookup.query.all()]
    form.stations = Station_lookup.query.all()
    cache['stations'] = form.stations

    if form.validate_on_submit():
        # Redirect to load_data route with the selected station ID
        station_id = form.station_id.data
        return redirect(url_for("load_data", station_id=station_id))

    return render_template("splash.html", form=form)

@app.route("/teleCC_patients/<int:station_id>", methods = ["GET", "POST"])
def teleCC_patients(station_id):
    return render_template("teleCC_patients.html", initial_station_id = station_id, stations = Station_lookup.query.all())

@app.route('/load_data_v1/<int:station_id>')
def load_data_v1(station_id):
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
        stations = cache['stations'],
        prediction_datetime = prediction_datetime
    )

@app.route('/test_patient_list/<int:station_id>')
def test_patient_list(station_id):
    return render_template("patient_list.html", stations = Station_lookup.query.all(), initial_station_id = station_id)

@app.route("/testing", methods = ['GET', 'POST'])
def test():
    return render_template("teleCC_patients.html", initial_station_id = 123, stations = Station_lookup.query.all())



@app.route('/load_data/<int:station_id>')
def load_data(station_id):
    '''
    Returns JSON of:
     station_name: The station Name
     last_update: The last model update per database state table.
     patients: The list of patients in the station ICU.

    Returned data is per the ORM model queries.
    '''
    # Query the station name
    station = Station_lookup.query.filter_by(station_number=station_id).first()
    if not station:
        return jsonify({"error": "Station not found"}), 404
    station_name = station.station_name

    # Query the list of patients
    station_list = Patient_telecc_state.query.filter_by(station_number=station_id).all()
    if station_list:
        prediction_datetime = station_list[0].prediction_datetime.strftime('%m-%d-%Y %I:%M %p')
        station_list_sorted = sorted(station_list, key=lambda p: p.patientName.split()[-1])
    else:
        prediction_datetime = None
        station_list_sorted = []

    # Convert patient data to JSON-serializable format
    patients_json = [
        {
            "patientID": patient.patientID,
            "patientName": patient.patientName,
            "room": patient.room,
            "septic_shock_class": patient.septic_shock_class,
            "septic_shock_trend": patient.septic_shock_trend,
            "respiratory_class": patient.respiratory_class,
            "respiratory_trend": patient.respiratory_trend,
        }
        for patient in station_list_sorted
    ]

    # Return JSON response
    return jsonify({
        "station_name": station_name,
        "last_updated": prediction_datetime,
        "patients": patients_json
    })




@app.route('/get_patient_details/<int:patient_id>', methods=['GET'])
def get_patient_details(patient_id):
    """
    Endpoint to fetch detailed information about a specific patient.


    """
    response_data = get_patient_details_json(patient_id)
    return (response_data.json)