import React, { useState } from 'react';
import { Container, Alert } from 'react-bootstrap';
import UploadForm from './components/form';

function App() {
    const [prediction, setPrediction] = useState('');

    return (
        <Container className="mt-5">
            <h1 className="mb-4">Reinforcement Learning in Adversarial Attack with Classification Model</h1>
            <UploadForm setPrediction={setPrediction} />
            {prediction && <Alert variant="success" className="mt-3">Prediction: {prediction}</Alert>}
        </Container>
    );
}

export default App;
