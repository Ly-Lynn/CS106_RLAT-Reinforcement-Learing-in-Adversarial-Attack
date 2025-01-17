import React, { useState, useRef, useEffect } from 'react';
import { Form, Button, Alert, Container, Image } from 'react-bootstrap';
import ImageDisplay from './imageDisplay';
import ProgressBar from 'react-bootstrap/ProgressBar';
import axios from 'axios';


const FormSubmitted = ({image, resize, grid}) => {
    // console.log("image", image)
    const [currentImage, setCurrentImage] = useState(null);
    const [probList, setProbList] = useState([0,0,0,0,0,0,0,0,0,0]);
    const [pred, setPred] = useState(null);
    const [l2, setL2] = useState(null);
    const [gridImage, setGridImage] = useState(null);
    const [success, setSuccess] = useState(null)
    const [step, setStep] = useState(null);
    const [smallAttacked, setSmallAttacked] = useState(null)
    const eventSource = useRef(null); // Use useRef to keep track of EventSource instance

    const nameClasses = ['airplane', 
                        'automobile',
                        'bird',
                        'cat',
                        'deer',
                        'dog',
                        'frog',
                        'horse',
                        'ship',
                        'truck']
    const handleAttack = async() => {
        try {
            const response = await axios.post('http://127.0.0.1:8000/attack', { image });
            const sessionId = response.data.session_id;
            eventSource.current = new EventSource(`http://127.0.0.1:8000/attack/${sessionId}`);
            eventSource.current.onmessage = (event) => {  
                const data = JSON.parse(event.data);
                // console.log(event.data)
                setSmallAttacked()
                setCurrentImage(`data:image/png;base64,${data.attacked}`);
                setGridImage(`data:image/png;base64,${data.grid}`);
                setProbList(data.prob);
                setPred(data.pred);
                setL2(data.l2);
                setSuccess(data.success);
                setStep(data.step)
                setSmallAttacked(`data:image/png;base64,${data.small_attacked}`)
            };
                eventSource.current.onerror = () => {
                    eventSource.current.close();
                
            }   
        } catch (error) {
            console.error('Error attack:', error);
        }
    };

    let alertVariant, alertText;
    if (success === '1') {
        alertVariant = 'success';
        alertText = 'Attack successfully'
    } else if (success === '0') {
        alertVariant = 'danger';
        alertText = 'Attack failes'
    } else {
        alertVariant = 'info'
        alertText = 'Attacking ...'
    }


    return (
        <Container className='d-flex p-4'>
            <div className=''>
                <div className='border p-2'>
                    <div className='d-flex justify-content-center align-items-center'>
                        {/* {image && <Image src={image} alt="imageUploaded" fluid className="mt-3" />}
                        {resize && <Image src={resize} alt="imageUploaded" fluid className="mt-3" />} */}
                        {image && resize && <ImageDisplay img1={image} img2={resize} />}
                        <ImageDisplay img1={smallAttacked}/>
                        <ImageDisplay img1={currentImage} img2={gridImage} />
                    </div>
                </div>
            </div>
            <div className='ml-3 p-2 flex-grow-1'>
                <div className='mb-2' style={{ fontSize: '20px' }}><strong>Step: </strong> {step} </div>
                <div className='mb-3'>
                    {probList && probList.length > 0 ? (
                        probList.map((prob, index) => (
                            <div key={index}>
                                <div className="text-base font-medium" style={{color: '#000'}}>
                                    <strong>{nameClasses[index]}</strong>: {`${(prob * 100).toFixed(2)}%`}
                                </div>
                                <ProgressBar variant={`${index}-bar`} now={prob * 100} label={`${(prob * 100).toFixed(2)}%`} />
                            </div>
                        ))
                    ) : (
                        <div>No data available</div>
                    )}
                </div>
                {pred && <Alert variant='primary' className='mt-3'>Predict: {pred}</Alert>}
                {l2 && <Alert variant='primary' className='mt-3'>L2 Norm: {l2}</Alert>}
                {success && <Alert variant={alertVariant}>{alertText}</Alert>}
                <div className='d-flex justify-content-center'>
                    <Button onClick={handleAttack} variant='danger' className='mt-3'>Attack</Button>
                </div>
            </div>
        </Container>
    )
}

export default FormSubmitted;