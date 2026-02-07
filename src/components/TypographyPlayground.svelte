<script lang="ts">
  import { onMount, createEventDispatcher } from 'svelte';
  import Typography from '../components/Typography.svelte';
  
  const dispatch = createEventDispatcher();
  
  let text = 'Type your text here...';
  let fontFamily = 'serif';
  let fontSize = 48;
  let fontWeight = 400;
  let letterSpacing = 0;
  let lineHeight = 1.2;
  let textAlign = 'center';
  let textTransform = 'none';
  let color = '#ffffff';
  let selectedEffect = 'none';
  let playSpeed = 300; // Default speed in ms
  let repeatCount = 8; // Default repeat count
  let customMsg = false;
  
  // Animation options like original iBlipper
  const animationOptions = [
    { value: 'topbounce,fade', label: 'bounce' },
    { value: 'pulsate,fade', label: 'pulsate' },
    { value: 'slide,fade', label: 'slide' },
    { value: 'shake,fade', label: 'shake' },
    { value: 'spinaway,fade', label: 'spinaway' },
    { value: 'slowslide,fade', label: 'slowslide' },
    { value: 'vibrato,fade', label: 'vibrato' },
    { value: 'wiggle,fade', label: 'wiggle' },
    { value: 'waggle,fade', label: 'waggle' },
    { value: 'wobble,fade', label: 'wobble' },
    { value: 'zoomin,fade', label: 'zoomin' },
    { value: 'zoomout,fade', label: 'zoomout' }
  ];
  
  // Color options for light and dark palettes
  const darkPalette = [
    '#000000', // Black
    '#003300', // Dark Green
    '#000066', // Dark Blue
    '#990000', // Dark Red
    '#7D1C8D'  // Purple
  ];
  
  const lightPalette = [
    '#FFFFFF', // White
    '#FFFEAA', // Light Yellow
    '#99FF66', // Light Green
    '#C2FDFE', // Light Blue
    '#FFCCFF'  // Light Pink
  ];
  
  let useDarkPalette = false;
  
  // Predefined message categories
  const messageCategories = [
    {
      name: 'Greetings',
      messages: [
        'whazzz up? ;-)',
        'Woo hoo :-> WOO HOO',
        'Come Over Here :-)'
      ]
    },
    {
      name: 'Affection',
      messages: [
        '(V) I love You (V) (v)',
        'You are my sun shine'
      ]
    },
    {
      name: 'Pickup Lines',
      messages: [
        'Hey Good Lookin!',
        'Lets Dance',
        "I'm leaving :-) Are you coming?",
        'Do you mind if I stare at you up close instead of from across the room?',
        'Hi, Can I buy you a drink?',
        'Hi, Can I buy you several drinks?',
        'Can get your number?',
        'My number is '
      ]
    },
    {
      name: 'Out with Friends',
      messages: [
        'You ready to go?',
        'Want another drink?'
      ]
    },
    {
      name: 'Restaurants',
      messages: [
        'Another round please !!',
        'Check Please',
        'BEER please :->'
      ]
    },
    {
      name: 'Good-byes',
      messages: [
        'See ya later alligator!',
        'After while crocodile',
        'See ya soon'
      ]
    }
  ];
  
  // Track expanded categories
  let expandedCategories: Record<string, boolean> = {};
  
  // Toggle category expansion
  function toggleCategory(categoryName: string): void {
    expandedCategories[categoryName] = !expandedCategories[categoryName];
  }
  
  // Set message from predefined options
  function setMessage(msg: string): void {
    text = msg;
    customMsg = true;
    dispatch('settingsChange', settings);
  }
  
  // Set color from palette
  function setColor(newColor: string): void {
    color = newColor;
  }
  
  // Toggle between light and dark palette
  function toggleColorPalette(): void {
    useDarkPalette = !useDarkPalette;
  }
  
  const fontFamilyOptions = ['sans', 'serif', 'mono'];
  const fontWeightOptions = [300, 400, 600, 700];
  const textAlignOptions = ['left', 'center', 'right'];
  const textTransformOptions = ['none', 'uppercase', 'lowercase', 'capitalize'];
  const speedOptions = [
    { value: 1200, label: '1.2s' },
    { value: 750, label: '.75s' },
    { value: 500, label: '.5s' },
    { value: 400, label: '.4s' },
    { value: 300, label: '.3s' },
    { value: 150, label: '.15s' }
  ];
  const repeatOptions = [1, 2, 4, 8, 100, 10000];

  // Watch for changes to settings and dispatch them to parent
  $: settings = {
    text,
    fontFamily,
    fontSize,
    fontWeight,
    letterSpacing,
    lineHeight,
    textAlign,
    textTransform,
    color,
    effect: selectedEffect,
    speed: playSpeed,
    repeatCount
  };

  $: dispatch('settingsChange', settings);
  
  function handlePresentClick(): void {
    dispatch('presentClick');
  }
  
  // Select the first animation
  onMount(() => {
    selectedEffect = animationOptions[0].value;
  });
</script>

<div class="iblipper-ui bg-gray-900 min-h-screen p-4">
  <!-- Header with Logo -->
  <div class="text-center mb-6">
    <h1 class="text-6xl font-serif font-bold mb-2 text-white">iBlipper</h1>
    <p class="text-xl text-gray-400">Expressive Typography</p>
  </div>
  
  <div class="max-w-5xl mx-auto">
    <!-- Main Interface -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Control Panel -->
      <div class="bg-gray-800 p-6 rounded-lg shadow-lg text-white">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-serif text-primary-400">Control Panel</h2>
          <button 
            class="bg-gradient-to-r from-primary-600 to-primary-400 hover:from-primary-500 hover:to-primary-300 text-white font-bold py-2 px-8 rounded-full flex items-center"
            on:click={handlePresentClick}
          >
            <span class="mr-2">Blip It!</span>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
        
        <!-- Text Input -->
        <div class="mb-6">
          <div class="flex">
            <button 
              class="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-l"
              on:click={() => { text = ''; }}
            >
              X
            </button>
            <textarea 
              bind:value={text} 
              class="w-full p-3 border bg-gray-700 text-white rounded-r focus:ring focus:ring-primary-400 focus:border-primary-500"
              rows="2"
              placeholder="Type your message here..."
              on:input={() => customMsg = true}
            ></textarea>
          </div>
        </div>
        
        <!-- Settings Fieldset -->
        <fieldset class="border border-gray-600 rounded-md p-4 mb-6">
          <legend class="px-2 text-primary-300 font-bold">Settings</legend>
          
          <div class="grid grid-cols-2 gap-4">
            <!-- Speed -->
            <div>
              <label class="block mb-1 text-gray-300">Speed:</label>
              <select 
                bind:value={playSpeed} 
                class="w-full p-2 bg-gray-700 border border-gray-600 rounded-md text-white"
              >
                {#each speedOptions as option}
                  <option value={option.value}>{option.label}</option>
                {/each}
              </select>
            </div>
            
            <!-- Effect -->
            <div>
              <label class="block mb-1 text-gray-300">Effect:</label>
              <select 
                bind:value={selectedEffect} 
                class="w-full p-2 bg-gray-700 border border-gray-600 rounded-md text-white"
              >
                {#each animationOptions as option}
                  <option value={option.value}>{option.label}</option>
                {/each}
              </select>
            </div>
            
            <!-- Repeat -->
            <div>
              <label class="block mb-1 text-gray-300">Repeat:</label>
              <select 
                bind:value={repeatCount} 
                class="w-full p-2 bg-gray-700 border border-gray-600 rounded-md text-white"
              >
                {#each repeatOptions as option}
                  <option value={option}>{option}</option>
                {/each}
              </select>
            </div>
            
            <!-- Font Family -->
            <div>
              <label class="block mb-1 text-gray-300">Font:</label>
              <select 
                bind:value={fontFamily} 
                class="w-full p-2 bg-gray-700 border border-gray-600 rounded-md text-white"
              >
                {#each fontFamilyOptions as option}
                  <option value={option}>{option}</option>
                {/each}
              </select>
            </div>
          </div>
          
          <!-- Color Palette -->
          <div class="mt-4 p-3 border border-gray-600 rounded bg-gray-700">
            <h3 class="text-sm text-gray-300 mb-2">Foreground</h3>
            
            <div class="flex flex-col gap-2">
              <!-- Dark palette -->
              <div class="flex items-center">
                <div class="flex space-x-2 mr-2">
                  {#each darkPalette as paletteColor}
                    <button 
                      class="w-8 h-8 rounded-full border-2 {color === paletteColor ? 'border-white' : 'border-transparent'}" 
                      style="background-color: {paletteColor}"
                      on:click={() => setColor(paletteColor)}
                    ></button>
                  {/each}
                </div>
                <input 
                  type="radio" 
                  bind:group={useDarkPalette} 
                  value={true} 
                  id="dark-palette"
                  class="ml-2"
                />
              </div>
              
              <!-- Light palette -->
              <div class="flex items-center">
                <div class="flex space-x-2 mr-2">
                  {#each lightPalette as paletteColor}
                    <button 
                      class="w-8 h-8 rounded-full border-2 {color === paletteColor ? 'border-white' : 'border-transparent'}" 
                      style="background-color: {paletteColor}"
                      on:click={() => setColor(paletteColor)}
                    ></button>
                  {/each}
                </div>
                <input 
                  type="radio" 
                  bind:group={useDarkPalette} 
                  value={false}
                  id="light-palette"
                  class="ml-2"
                />
              </div>
            </div>
          </div>
        </fieldset>
        
        <!-- Font Size -->
        <div class="mb-4">
          <label class="block mb-1 text-gray-300">Font Size:</label>
          <div class="flex items-center">
            <input 
              type="range" 
              bind:value={fontSize} 
              min="12" 
              max="120" 
              class="w-full mr-3 accent-primary-500"
            />
            <span class="text-sm w-12 text-right text-gray-300">{fontSize}px</span>
          </div>
        </div>
        
        <!-- Additional Typography Controls -->
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block mb-1 text-gray-300">Text Transform:</label>
            <select 
              bind:value={textTransform} 
              class="w-full p-2 bg-gray-700 border border-gray-600 rounded-md text-white"
            >
              {#each textTransformOptions as option}
                <option value={option}>{option}</option>
              {/each}
            </select>
          </div>
          
          <div>
            <label class="block mb-1 text-gray-300">Text Align:</label>
            <select 
              bind:value={textAlign} 
              class="w-full p-2 bg-gray-700 border border-gray-600 rounded-md text-white"
            >
              {#each textAlignOptions as option}
                <option value={option}>{option}</option>
              {/each}
            </select>
          </div>
        </div>
      </div>
      
      <!-- Preview and Message Categories -->
      <div class="space-y-6">
        <!-- Preview -->
        <div class="bg-black p-6 rounded-lg shadow-lg border border-gray-700">
          <h2 class="text-2xl font-serif mb-6 text-primary-400">Preview</h2>
          
          <div class="preview-container p-4 border border-gray-700 rounded-md min-h-[200px] flex items-center justify-center bg-gray-900">
            <Typography 
              {text}
              {fontFamily}
              {fontSize}
              {fontWeight}
              {letterSpacing}
              {lineHeight}
              {textAlign}
              {textTransform}
              {color}
              effect={selectedEffect}
            />
          </div>
        </div>
        
        <!-- Predefined Message Categories -->
        <div class="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h2 class="text-2xl font-serif mb-4 text-primary-400">Message Library</h2>
          
          <div class="space-y-2">
            {#each messageCategories as category}
              <div class="category border border-gray-700 rounded overflow-hidden">
                <button 
                  class="w-full py-2 px-4 bg-gray-900 text-white font-bold flex justify-between items-center"
                  on:click={() => toggleCategory(category.name)}
                >
                  <span>{category.name}</span>
                  <span>{expandedCategories[category.name] ? '▼' : '►'}</span>
                </button>
                
                {#if expandedCategories[category.name]}
                  <div class="p-2 bg-gray-800">
                    {#each category.messages as message}
                      <button 
                        class="block w-full text-left p-2 hover:bg-gray-700 text-gray-300 rounded"
                        on:click={() => setMessage(message)}
                      >
                        {message}
                      </button>
                    {/each}
                  </div>
                {/if}
              </div>
            {/each}
          </div>
        </div>
      </div>
    </div>
    
    <!-- Footer with instructions -->
    <div class="mt-8 text-center text-gray-500 text-sm">
      <p>Original iBlipper Style - Type your message or choose from the library, then click "Blip It!"</p>
      <p class="mt-2">Special formatting: @word@ = wiggle, word! = wobble, word, = bounce, word. = zoom, etc.</p>
    </div>
  </div>
</div> 