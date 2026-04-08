import React, { useState } from 'react';
import { Plus, X } from 'lucide-react';

export default function IngredientInput({ ingredients, setIngredients }) {
  const [inputValue, setInputValue] = useState('');

  const handleAdd = (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;
    
    // Split by commas to allow pasting a list
    const newItems = inputValue.split(',').map(i => i.trim()).filter(i => i);
    
    const uniqueItems = new Set([...ingredients, ...newItems]);
    setIngredients(Array.from(uniqueItems));
    setInputValue('');
  };

  const removeIngredient = (index) => {
    setIngredients(ingredients.filter((_, i) => i !== index));
  };

  return (
    <div className="ingredient-input-container panel">
      <h3>Add Ingredients</h3>
      <p className="subtitle">Type an ingredient and press Enter, or separate by commas</p>
      
      <form onSubmit={handleAdd} className="input-row">
        <input 
          type="text" 
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="e.g. Tomato, Chicken, Rice..."
          className="styled-input"
        />
        <button type="submit" className="btn btn-primary"><Plus size={18} /> Add</button>
      </form>

      <div className="tags-container">
        {ingredients.map((ing, i) => (
          <div key={i} className="tag animate-pop">
            <span>{ing}</span>
            <button type="button" onClick={() => removeIngredient(i)} className="remove-btn">
              <X size={14} />
            </button>
          </div>
        ))}
        {ingredients.length === 0 && (
          <div className="empty-tags">No ingredients added yet...</div>
        )}
      </div>
    </div>
  );
}
