import React, { useState, useRef } from 'react';
import { UploadCloud, Image as ImageIcon, Loader } from 'lucide-react';
import { uploadImage } from '../api';

export default function ImageUploader({ setIngredients, appendIngredients }) {
  const [isUploading, setIsUploading] = useState(false);
  const [preview, setPreview] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Create a preview
    const reader = new FileReader();
    reader.onload = (ev) => setPreview(ev.target.result);
    reader.readAsDataURL(file);

    setIsUploading(true);
    try {
      const data = await uploadImage(file);
      appendIngredients(data.detected_ingredients);
    } catch (err) {
      alert("Error analyzing image: " + err.message);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="image-uploader-container panel">
      <h3>Or Upload an Image</h3>
      <p className="subtitle">Let AI detect ingredients from a picture!</p>
      
      <div 
        className={`drop-area ${isUploading ? 'uploading' : ''}`}
        onClick={() => fileInputRef.current?.click()}
      >
        {isUploading ? (
          <div className="flex-center col fade-in">
            <Loader className="spinner icon-large text-primary" size={48} />
            <p>Analyzing flavors...</p>
          </div>
        ) : preview ? (
          <div className="preview-container fade-in">
            <img src={preview} alt="Upload preview" className="preview-image" />
            <div className="overlay">
              <ImageIcon size={32} />
              <p>Change Image</p>
            </div>
          </div>
        ) : (
          <div className="flex-center col fade-in">
            <UploadCloud className="icon-large text-primary mb-2" size={48} />
            <p>Click or drag to drop an image</p>
          </div>
        )}
      </div>
      <input 
        type="file" 
        accept="image/*" 
        style={{ display: 'none' }} 
        ref={fileInputRef}
        onChange={handleFileChange}
      />
    </div>
  );
}
