import React, { useState } from 'react';
import IngredientInput from './components/IngredientInput';
import ImageUploader from './components/ImageUploader';
import RecipeView from './components/RecipeView';
import HistorySidebar from './components/HistorySidebar';
import { generateRecipe } from './api';
import { ChefHat, Sparkles, Loader } from 'lucide-react';

function App() {
  const [ingredients, setIngredients] = useState([]);
  const [recipe, setRecipe] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);

  const appendCustomIngredients = (newItems) => {
    const unique = Array.from(new Set([...ingredients, ...newItems]));
    setIngredients(unique);
  };

  const handleGenerate = async () => {
    if (ingredients.length === 0) return;
    setIsGenerating(true);
    setRecipe(null);
    try {
      const data = await generateRecipe(ingredients);
      setRecipe(data);
    } catch (err) {
      alert("Failed to generate recipe.");
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="layout">
      <HistorySidebar onSelectRecipe={setRecipe} />
      
      <main className="main-content">
        <header className="app-header fade-in-down">
          <div className="logo flex-center gap-2">
            <div className="icon-wrap"><ChefHat size={32} className="text-primary"/></div>
            <h1>AI <span className="text-gradient">Recipe Genius</span></h1>
          </div>
          <p>Transform your ingredients or food images into delicious meals!</p>
        </header>

        {!recipe && !isGenerating && (
          <div className="input-section fade-in">
            <div className="grid-2">
              <IngredientInput ingredients={ingredients} setIngredients={setIngredients} />
              <ImageUploader setIngredients={setIngredients} appendIngredients={appendCustomIngredients} />
            </div>

            <div className="action-row">
              <button 
                className={`btn btn-generate pulse ${ingredients.length === 0 ? 'disabled' : ''}`}
                onClick={handleGenerate}
                disabled={ingredients.length === 0}
              >
                <Sparkles size={20} /> Generate Recipe
              </button>
            </div>
          </div>
        )}

        {isGenerating && (
          <div className="loading-state fade-in flex-center col">
            <Loader className="spinner icon-huge text-primary" size={64}/>
            <h2 className="mt-4 text-gradient">Cooking up some magic...</h2>
            <p>Our AI chef is crafting the perfect recipe.</p>
          </div>
        )}

        {recipe && !isGenerating && (
          <div className="recipe-container fade-in-up">
            <button className="btn btn-secondary mb-4" onClick={() => setRecipe(null)}>
              &larr; Create another recipe
            </button>
            <RecipeView recipe={recipe} />
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
