import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

const ImageDisplay = ({img1, img2 }) => {
    return (
        <div className="container p-2 ps-3">
            {img1 && (
                <div className="col-12 mt-3">
                    <img src={img1} alt="img1Uploaded" style={{ width: 'auto', height: 'auto' }} />
                </div>
            )}
            {img2 && (
                <div className="col-12 mt-3">
                    <img src={img2} alt="img2Uploaded" style={{ width: 'auto', height: 'auto' }} />
                </div>
            )}
        </div>
    );
};

export default ImageDisplay;
