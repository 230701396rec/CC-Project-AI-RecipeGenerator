import React from 'react';
import { Clock, ChefHat, Info } from 'lucide-react';

export default function RecipeView({ recipe }) {
  if (!recipe) return null;

  return (
    <div className="recipe-view slide-up">
      <div className="recipe-header glowing-bg">
        <h2>{recipe.name}</h2>
        <div className="recipe-meta flex-center gap-4">
          <span className="badge flex-center gap-2"><Clock size={16}/> {recipe.cook_time}</span>
          <span className="badge flex-center gap-2"><ChefHat size={16}/> Gen-AI Recipe</span>
        </div>
      </div>

      <div className="recipe-grid">
        <div className="recipe-card panel">
          <h3>Ingredients</h3>
          <ul className="ingredients-list">
            {recipe.ingredients_list.map((ing, i) => (
              <li key={i}>{ing}</li>
            ))}
          </ul>
        </div>
        
        {recipe.nutrition && (
          <div className="recipe-card panel">
            <h3><Info size={18} style={{display:'inline', verticalAlign:'middle'}}/> Nutrition facts (Est.)</h3>
            <div className="nutrition-grid">
              <div className="nutri-item"><span>Calories</span><strong>{recipe.nutrition.calories}</strong></div>
              <div className="nutri-item"><span>Protein</span><strong>{recipe.nutrition.protein}</strong></div>
              <div className="nutri-item"><span>Carbs</span><strong>{recipe.nutrition.carbs}</strong></div>
              <div className="nutri-item"><span>Fat</span><strong>{recipe.nutrition.fat}</strong></div>
            </div>
          </div>
        )}
      </div>

      <div className="recipe-card panel step-card">
        <h3>Instructions</h3>
        <ol className="instructions-list">
          {recipe.instructions.map((step, i) => (
            <li key={i}>
              <span className="step-number">{i + 1}</span>
              <p>{step}</p>
            </li>
          ))}
        </ol>
      </div>
    </div>
  );
}
