<script>
  let theme = '';
  let characterType = ''; // Dropdown for character type
  let characterCount = 1; // Slider for number of characters
  let characters = ''; // Textbox for character names
  let storyLocation = ''; // Textbox for story location
  let storyMoral = ''; // Textbox for story moral values
  let otherThings = '';
  let story = '';
  let imageDesc = ''; // Add a variable to capture image description
  let imagePath = '';

  let loadingStory = false; // Track story loading state
  let loadingImage = false; // Track image loading state

  async function getStory() {
    loadingStory = true;
    story = ''; // Clear previous story
    try {
      const response = await fetch('/api/story', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          theme: theme,
          characterType: characterType,
          characterCount: characterCount,
          characters: characters,
          storyLocation: storyLocation,
          storyMoral: storyMoral,
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
    } finally {
      loadingStory = false;
    }
  }

  async function fetchImage() {
    loadingImage = true;
    imagePath = ''; // Clear previous image
    try {
      const response = await fetch('/api/generate_image', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          image_desc: imageDesc
        })
      });

      const data = await response.json();

      if (data.image_url) {
        imagePath = data.image_url;
      } else {
        console.error("Error generating image:", data.error);
      }
    } catch (error) {
      console.error('Error fetching image:', error);
    } finally {
      loadingImage = false;
    }
  }

  async function generateStoryAndImage() {
    await getStory();
    await fetchImage();
  }
</script>

<style>
  main {
    font-family: 'Comic Sans MS', 'Arial', sans-serif;
    text-align: right;
    direction: rtl;
    padding: 20px;
    background: linear-gradient(135deg, #ffebcd 0%, #ffcccb 100%);
    border-radius: 15px;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
    max-width: 800px;
    margin: 0 auto;
  }

  .inner-container {
    background-color: #f5f5f5; /* Light grey background */
    padding: 20px;
    border-radius: 15px;
    width: 90%;
    max-width: 700px; /* Smaller width than main */
    margin: 0 auto; /* Center within main */
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
  }

  h1 {
    font-size: 2rem;
    color: #ff6347;
    text-shadow: 2px 2px 0px #ffe4e1;
    text-align: center;
    margin-bottom: 20px;
  }

  label {
    font-size: 1.5rem;
    color: #555;
  }

  input, textarea {
    width: 100%;
    font-size: 1.5rem;
    padding: 15px;
    margin: 10px 0;
    box-sizing: border-box;
    border-radius: 20px; /* Rounder input and textarea */
    border: 2px solid #43bccd;
    background-color: #fff;
    box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
  }

  /* Base styling for the dropdown */
select {
  appearance: none;
  -webkit-appearance: none; /* For Safari */
  -moz-appearance: none; /* For Firefox */
  background-color: #f0f0f0;
  color: #333;
  font-size: 1.2rem;
  padding: 12px 20px;
  border: 2px solid #43bccd; /* Border color */
  border-radius: 8px; /* Rounded corners */
  width: 100%;
  max-width: 400px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow */
  transition: all 0.3s ease;
  cursor: pointer;
}

/* Arrow for the dropdown */
/* Container for consistent dropdown width */
.select-container {
  position: relative;
  width: 100%; /* Adjust width to match other controls */
  max-width: 400px;
}

/* Base styling for the dropdown */
select {
  appearance: none;
  -webkit-appearance: none; /* For Safari */
  -moz-appearance: none; /* For Firefox */
  background-color: #f0f0f0;
  color: #333;
  font-size: 1.2rem;
  padding: 12px 40px;
  border: 2px solid #43bccd;
  border-radius: 20px; /* Increased border-radius for rounder shape */
  width: 100%;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
}

/* Custom arrow for the dropdown */
.select-container::after {
  content: '';
  position: absolute;
  top: 50%;
  right: 20px;
  transform: translateY(-50%) rotate(45deg);
  width: 10px;
  height: 10px;
  border-left: 2px solid #333;
  border-bottom: 2px solid #333;
  pointer-events: none; /* Prevent arrow from blocking dropdown interaction */
}

/* Hover and focus effects */
select:hover {
  border-color: #3598a9;
}

select:focus {
  outline: none;
  border-color: #43bccd;
  box-shadow: 0 0 0 3px rgba(67, 188, 205, 0.2);
}



  button {
    font-size: 1.5rem;
    padding: 10px 20px;
    background-color: #43bccd; /* Blue button color */
    color: white;
    border: none;
    border-radius: 20px; /* Rounder button */
    cursor: pointer;
    margin-top: 15px;
    box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s, background-color 0.3s;
  }

  button:hover {
    background-color: #3598a9;
    transform: scale(1.05);
  }

  .story-output {
    margin-top: 20px;
    font-size: 1.75rem;
    background-color: #fef5e7;
    padding: 25px;
    border-radius: 15px;
    border: 2px dashed #ffb6c1;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
  }

  .logo-container {
    text-align: center;
    margin: 20px 0;
  }

  .logo {
    max-width: 150px;
    height: auto;
  }

  .loading-spinner {
    border: 4px solid #f3f3f3;
    border-top: 4px solid #888;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin: 0 auto;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  .pic {
    max-width: 150px; /* Adjust to desired width */
    height: auto; /* Maintain aspect ratio */
    border-radius: 10px; /* Optional: Rounded corners */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Optional: Subtle shadow for a polished look */
    margin-top: 10px; /* Add space above the image */
  }

</style>

<main>
  <div class="logo-container">
    <img src="qissah-logo.png" class="logo" alt="Logo">
  </div>

  <div class="inner-container">
    <!-- <h1>نموذج توليد الحكايات</h1> -->

    <label for="theme">اختر موضوع القصة:</label>
    <input type="text" bind:value={theme} id="theme" placeholder="موضوع القصة..." />

    <label for="characterType">نوع الشخصيات:</label>
    <div class="select-container">
      <select>
        <option value="human">بشر</option>
        <option value="animal">حيوانات</option>
        <option value="inanimate">جمادات</option>
        <option value="other">أخرى</option>
      </select>
    </div>

    <label for="characters-slider">عدد الشخصيات:</label>
    <input 
      type="range" 
      id="characters-slider" 
      min="1" 
      max="5" 
      step="1" 
      bind:value={characterCount}
    />
    <div class="slider-value">عدد الشخصيات المختارة: {characterCount}</div>

    <label for="characters">أسماء الشخصيات:</label>
    <input type="text" bind:value={characters} id="characters" placeholder="أسماء الشخصيات..." />

    <label for="storyLocation">مكان القصة:</label>
    <input type="text" bind:value={storyLocation} id="storyLocation" placeholder="مكان القصة..." />

    <label for="storyMoral">القيم الأخلاقية للقصة:</label>
    <input type="text" bind:value={storyMoral} id="storyMoral" placeholder="القيم الأخلاقية..." />

    <label for="otherThings">اضف عناصر أخرى:</label>
    <textarea bind:value={otherThings} id="otherThings" placeholder="عناصر أخرى..."></textarea>

    <label for="imageDesc">وصف الصورة:</label>
    <input type="text" bind:value={imageDesc} id="imageDesc" placeholder="وصف الصورة..." />

    <button on:click={generateStoryAndImage}>توليد القصة والصورة</button>

    {#if loadingStory}
      <div class="loading-spinner"></div>
    {:else if story}
      <div class="story-output">
        {#if loadingImage}
          <div class="loading-spinner"></div>
        {:else if imagePath}
          <img class="pic" src={imagePath} alt="Generated image">
        {/if}
        <p>{story}</p>
      </div>
    {/if}
  </div>
</main>
