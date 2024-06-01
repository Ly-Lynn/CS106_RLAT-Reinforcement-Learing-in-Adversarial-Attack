import React, { useState } from 'react';
import { Form, Button, Alert } from 'react-bootstrap';
import FormSubmitted from './formSubmitted';
import axios from 'axios';

const UploadForm = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [error, setError] = useState('');
    const [image, setImage] = useState(null);
    const [resize, setResize] = useState(null);
    const [draw, setDraw] = useState(null);
    const [prediction, setPrediction] = useState('');

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
            setImage(`data:image/png;base64,${response.data.image}`);
            setResize(`data:image/png;base64,${response.data.resize_image}`);
            setDraw(`data:image/png;base64,${response.data.draw_image}`);
            setError('');
            // onFormSubmit();
        } catch (err) {
            console.error('Error fetching prediction:', err); // Log detailed error
            setError('Failed to fetch prediction. Please try again.', err);
        }
    };

    return (
        <>
            <Form onSubmit={handleSubmit}>
                <Form.Group controlId="formFile" className="mb-3">
                    <Form.Label>Upload Image</Form.Label>
                    <Form.Control type="file" onChange={handleFileChange} />
                </Form.Group>
                <Button variant="primary" type="submit">
                    Confirm
                </Button>
                {error && <Alert variant="danger" className="mt-3">{error}</Alert>}
            </Form>
            {image && <FormSubmitted image={image} resize={resize} grid={draw} prediction={prediction} />}
        </>
    );
};

export default UploadForm;
