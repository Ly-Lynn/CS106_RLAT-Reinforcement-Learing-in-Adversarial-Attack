import React, { useState } from 'react';
import { Form, Button, Alert, Image } from 'react-bootstrap';
import axios from 'axios';

const UploadForm = ({ setPrediction }) => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [error, setError] = useState('');
    const [uploadedImage, setUploadedImage] = useState(null);

    const handleFileChange = (e) => {
        setSelectedFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            const response = await axios.post('http://127.0.0.1:8000/predict/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setPrediction(response.data.prediction);
            setUploadedImage(`data:image/png;base64,${response.data.image}`);
            setError('');
        } catch (err) {
            setError('Failed to fetch prediction. Please try again.');
        }
    };

    return (
        <Form onSubmit={handleSubmit}>
            <Form.Group controlId="formFile" className="mb-3">
                <Form.Label>Upload Image</Form.Label>
                <Form.Control type="file" onChange={handleFileChange} />
            </Form.Group>
            <Button variant="primary" type="submit">
                Predict
            </Button>
            {error && <Alert variant="danger" className="mt-3">{error}</Alert>}
            {uploadedImage && <Image src={uploadedImage} alt="Uploaded" fluid className="mt-3" />}
        </Form>
    );
};

export default UploadForm;
