import { plotScoreHistory } from './plotScoreHistory.js';

let activePatientID = null; // Global variable to track the active patient

export function loadPatientDetails(patientID, disease = 'septic_shock') {
    $.ajax({
        url: `/get_patient_details/${patientID}`,
        method: 'GET',
        success: function(response){
            handlePatientDetailsSuccess(response, disease)
        },
        error: function(xhr, status, error) {
            console.error(`Error fetching patient details for ID ${patientID}:`, error);
        }
    });
}

function handlePatientDetailsSuccess(data, disease = 'septic_shock') {

    // Update the activePatientID 
    activePatientID = data.patient_id
    // Attach activePatientID to the global window object
    window.activePatientID = activePatientID;

    console.log("PatientID (handlePatientDetailsSuccess): " + activePatientID)
    console.log("Disease (handlePatientDetailsSuccess): " + disease)


    // Get the data from the data object coinsiding with the disease type.
    const scoreClass = data[`${disease}_class`];
    const scoreValue = data[`${disease}_score`];
    const protocol = data[`${disease}_protocol`];
    const scoreHistoryData = data[`${disease}_history`];
    const explainabilityData = data[`${disease}_expl`];

    // ***************************************
    // Update Septic Shock Information Box
    // ***************************************
    
    // Dynamically set the title based on the disease
    const titleElement = document.getElementById('modelTitle');
    if (titleElement) {
        titleElement.textContent = disease === 'septic_shock' ? 'Septic Shock' : 'Respiratory Failure';
    }

    const scoreBox = document.getElementById('modelScore');
    scoreBox.className = 'score-box';
    switch (scoreClass.toLowerCase()) {
        case 'low':
            scoreBox.style.backgroundColor = 'white';
            scoreBox.style.color = 'black';
            break;
        case 'moderate':
            scoreBox.style.backgroundColor = '#30547C';
            scoreBox.style.color = 'white';
            break;
        case 'critical':
            scoreBox.style.backgroundColor = '#b33329';
            scoreBox.style.color = 'white';
            break;
        default:
            scoreBox.style.backgroundColor = '#d9534f';
            scoreBox.style.color = 'white';
    }
    document.getElementById('modelScore').textContent = `${scoreValue}`;
    document.getElementById('modelClass').textContent = `${scoreClass}`;
    document.getElementById('modelDate').textContent = `${data.prediction_datetime}`;
    document.getElementById('patientInfo').textContent = `Patient: ${data.patient_name}, Room ${data.room}`;

    const protocolContent = protocol.split('\n').map(line => `<p>• ${line}</p>`).join('');
    document.querySelector('.protocol').innerHTML = `<p><strong>Protocol:</strong></p>${protocolContent}`;

    // Update Explainability Table
    const tableBody = document.getElementById('explainabilityTableBody');
    tableBody.innerHTML = '';

    // Add positive contributions
    ['pos_1', 'pos_2', 'pos_3'].forEach(key => {
        if (explainabilityData[key]) {
            const row = `<tr><td>${explainabilityData[key][0]}</td><td>${explainabilityData[key][1]}</td></tr>`;
            tableBody.innerHTML += row;
        }
    });

    // Add negative contributions
    ['neg_1', 'neg_2', 'neg_3'].forEach(key => {
        if (explainabilityData[key]) {
            const row = `<tr><td>${explainabilityData[key][0]}</td><td>${explainabilityData[key][1]}</td></tr>`;
            tableBody.innerHTML += row;
        }
    });

    // Add the Score plot
    const ctx = document.getElementById('scoreHistoryChart').getContext('2d');
    plotScoreHistory(ctx, scoreHistoryData, data.prediction_datetime);
}