<script>
  let theme = '';
  let characters = ''; // Textbox for character names or details
  let characterCount = 1; // Slider to select the number of characters, initialized to 1
  let otherThings = '';
  let story = '';

  async function getStory() {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/story', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          theme: theme,
          characters: characters,
          characterCount: characterCount, // Include character count in the request
          otherThings: otherThings
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      story = data.story;
    } catch (error) {
      console.error('Error fetching story:', error);
    }
  }
</script>

<style>
  main {
    font-family: 'Comic Sans MS', 'Arial', sans-serif;
    text-align: right; /* Right-to-left layout for Arabic */
    direction: rtl;
    padding: 20px;
    background: linear-gradient(135deg, #ffebcd 0%, #ffcccb 100%);
    border-radius: 15px;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
    max-width: 800px;
    margin: 0 auto;
  }

  h1 {
    font-size: 2rem; /* Larger and more playful heading */
    color: #ff6347; /* Bright and engaging color */
    text-shadow: 2px 2px 0px #ffe4e1;
    text-align: center;
    margin-bottom: 20px;
  }

  label {
    font-size: 1.75rem; /* Large label font */
    color: #555;
  }

  input, textarea {
    width: 100%;
    font-size: 1.5rem; /* Large input font */
    padding: 15px;
    margin: 10px 0;
    box-sizing: border-box;
    border-radius: 15px;
    border: 3px solid #ffa07a;
    background-color: #fffaf0;
    box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
  }

  input:focus, textarea:focus {
    outline: none;
    border-color: #ff4500;
  }

  button {
    font-size: 2rem; /* Large and playful button text */
    padding: 15px 30px;
    background-color: #ffa07a;
    color: white;
    border: none;
    border-radius: 20px;
    cursor: pointer;
    margin-top: 15px;
    box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s, background-color 0.3s;
  }

  button:hover {
    background-color: #ff6347;
    transform: scale(1.1);
  }

  .story-output {
    margin-top: 20px;
    font-size: 1.75rem; /* Large story output font */
    background-color: #fef5e7;
    padding: 25px;
    border-radius: 15px;
    border: 2px dashed #ffb6c1;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
  }

  .logo-container {
    text-align: center; /* Center the logo */
    margin: 20px 0;
  }

  .logo {
    max-width: 200px; /* Adjust the size of the logo */
    height: auto;
    border-radius: 0px;
  }

  .pic {
    max-width: 200px; /* Adjust the size of the generated image */
    height: auto;
    border-radius: 0px;
  }

  .slider-container {
    margin: 20px 0; /* Add some margin for the slider */
  }

  .slider-value {
    font-size: 1.25rem; /* Slider value display */
    text-align: center;
    margin-bottom: 10px;
    color: #555;
  }
</style>

<main>
  <div class="logo-container">
    <img src="qissah-logo.png" class="logo" alt="Logo">
  </div>
  <h1>نموذج توليد الحكايات</h1>

  <label for="theme">اختر موضوع القصة:</label>
  <input type="text" bind:value={theme} id="theme" placeholder="موضوع القصة..." />

  <label for="characters">اختر الشخصيات:</label>
  <input type="text" bind:value={characters} id="characters" placeholder="الشخصيات..." />

  <!-- Slider for selecting number of characters -->
  <div class="slider-container">
    <label for="characters-slider">عدد الشخصيات:</label>
    <div class="slider-value">عدد الشخصيات المختارة: {characterCount}</div>
    <input 
      type="range" 
      id="characters-slider" 
      min="1" 
      max="5" 
      step="1" 
      bind:value={characterCount}
    />
  </div>

  <label for="otherThings">اضف عناصر أخرى:</label>
  <textarea bind:value={otherThings} id="otherThings" placeholder="عناصر أخرى..."></textarea>

  <button on:click={getStory}>توليد القصة</button>

  {#if story}
    <div class="story-output">
      <img class="pic" src="generated-img.webp" alt="Generated image">
      <p>{story}</p>
    </div>
  {/if}
</main>
