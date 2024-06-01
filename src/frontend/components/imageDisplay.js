import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

const ImageDisplay = ({ image, resize, draw }) => {
    return (
        <div className="container p-2 ps-3">
            {resize && (
                <div className="col-12 mt-3">
                    <img src={resize} alt="resizeUploaded" style={{ width: 'auto', height: 'auto' }} />
                </div>
            )}
            {draw && (
                <div className="col-12 mt-3">
                    <img src={draw} alt="drawUploaded" style={{ width: 'auto', height: 'auto' }} />
                </div>
            )}
        </div>
    );
};

export default ImageDisplay;
