import { plotScoreHistory } from './plotScoreHistory.js';

export function loadPatientDetails(patientID) {
    $.ajax({
        url: `/get_patient_details/${patientID}`,
        method: 'GET',
        success: function(data) {
            // Update Septic Shock Information Box
            const scoreBox = document.getElementById('septicShockScore');
            scoreBox.className = 'score-box';
            switch (data.septic_shock_class.toLowerCase()) {
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
                    scoreBox.style.backgroundColor = '#d9534f'; // Default color
                    scoreBox.style.color = 'white';
            }
            document.getElementById('septicShockScore').textContent = `${data.septic_shock_score}`;
            document.getElementById('septicShockClass').textContent = data.septic_shock_class;
            document.getElementById('septicShockDate').textContent = data.prediction_datetime;
            document.getElementById('septicShockPatientInfo').textContent = `Patient: ${data.patient_name}, Room ${data.room}`;

            const protocolContent = data.septic_shock_protocol.split('\n').map(line => `<p>• ${line}</p>`).join('');
            document.querySelector('.protocol').innerHTML = `<p><strong>Protocol:</strong></p>${protocolContent}`;

            // Update Explainability Table
            const explainabilityData = data.septic_shock_expl;
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
            plotScoreHistory(ctx, data.septic_shock_history, data.prediction_datetime);
        }
    });
}