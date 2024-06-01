import React, { useState } from 'react';
import { Form, Button, Alert, Container, Image } from 'react-bootstrap';
import ImageDisplay from './imageDisplay';
import ProgressBar from 'react-bootstrap/ProgressBar';
import axios from 'axios';


const FormSubmitted = ({image, resize, grid, prediction}) => {
    return (
        <Container className='d-flex p-4'>
            <div className=''>
                <div className='border p-2'>
                    <div className='d-flex justify-content-center align-items-center'>
                        {image && <Image src={image} alt="imageUploaded" fluid className="mt-3" />}
                        {resize && <Image src={resize} alt="imageUploaded" fluid className="mt-3" />}
                        <ImageDisplay image={image} resize={resize} draw={grid} />
                    </div>
                </div>
            </div>
            <div className='ml-3 p-2 flex-grow-1'>
                <div className='mb-3'>
                    <div className="text-base font-medium">Class 1</div>
                    <ProgressBar variant='red-bar' now={45} label={`${45}%`} />
                    <div className="text-base font-medium">Class 2</div>
                    <ProgressBar variant='orange-bar' now={45} label={`${45}%`} />
                    <div className="text-base font-medium">Class 3</div>
                    <ProgressBar variant='yellow-bar' now={45} label={`${45}%`} />
                    <div className="text-base font-medium">Class 4</div>
                    <ProgressBar variant='green-bar' now={45} label={`${45}%`} />
                    <div className="text-base font-medium">Class 5</div>
                    <ProgressBar variant='blue-bar' now={45} label={`${45}%`} />
                    <div className="text-base font-medium">Class 6</div>
                    <ProgressBar variant='darkblue-bar' now={45} label={`${45}%`} />
                    <div className="text-base font-medium">Class 7</div>
                    <ProgressBar variant='purple-bar' now={45} label={`${45}%`} />
                    <div className="text-base font-medium">Class 8</div>
                    <ProgressBar variant='pink-bar' now={45} label={`${45}%`} />
                    <div className="text-base font-medium">Class 9</div>
                    <ProgressBar variant='cyan-bar' now={45} label={`${45}%`} />
                    <div className="text-base font-medium">Class 10</div>
                    <ProgressBar variant='choco-bar' now={45} label={`${45}%`} />
                </div>
                <Alert variant='success' className='mt-3'>Predict: {prediction}</Alert>
                <div className='d-flex justify-content-center'>
                    <Button variant='danger' className='mt-3'>Attack</Button>
                </div>
            </div>
        </Container>
    )
}

export default FormSubmitted;