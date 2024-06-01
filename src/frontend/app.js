import React, { useState } from 'react';
import { Container, Button } from 'react-bootstrap';
import UploadForm from './components/form';
// import ImageDisplay from './components/imageDisplay';
import Attack from './components/attack'

function App() {
    

    return (
        <Container className="mt-5">
            <h1 className="mb-4">Reinforcement Learning in Adversarial Attack with Classification Model</h1>
            <UploadForm />
            
        </Container>
    );
}

export default App;
