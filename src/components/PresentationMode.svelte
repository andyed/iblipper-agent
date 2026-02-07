<script lang="ts">
  import { onMount } from 'svelte';
  
  export let settings: {
    text: string;
    fontFamily: string;
    fontSize: number;
    fontWeight: number;
    letterSpacing: number;
    lineHeight: number;
    textAlign: string;
    textTransform: string;
    color: string;
    effect: string;
  };
  export let exitPresentation: () => void;
  
  // For tracking animation state
  let animationKey = 0;
  let animationClass = '';
  
  // Instead of storing just words, we'll store enhanced "blips" with animation info
  interface Blip {
    displayWord: string;
    animation: string;
    duration: number;
    lag: number;
  }
  
  let blips: Blip[] = [];
  let currentBlipIndex = 0;
  let isPlaying = false;
  let defaultSpeed = 300; // milliseconds per word
  let playInterval: number | null = null;
  
  // Animation selection
  let selectedAnimation = 'fade';
  const animationOptions = [
    'fade', 'slide', 'slowslide', 'topbounce', 'wobble', 
    'zoomout', 'zoomin', 'shake', 'spinaway', 'wiggle', 
    'waggle', 'vibrato', 'pulsate'
  ];
  
  // Window dimensions for responsive sizing
  let windowWidth: number;
  let windowHeight: number;
  
  // Interpret word and return animation specs based on original iBlipper logic
  function interpWord(word: string): Blip {
    // Default values
    const blip: Blip = {
      displayWord: word,
      animation: selectedAnimation,
      duration: defaultSpeed,
      lag: 5
    };
    
    // Special syntax handling (from original iBlipper)
    
    // @word@ - use wiggle animation
    if (word.match(/^@.*@$/)) {
      blip.displayWord = word.substring(1, word.length - 1);
      blip.animation = 'wiggle,fade';
    }
    
    // word! - use wobble animation
    if (word.match(/.*!$/)) {
      blip.animation = 'wobble,zoomout';
    }
    
    // word, - use topbounce animation
    if (word.match(/.*,$/)) {
      blip.animation = 'topbounce,fade';
      blip.lag *= 2;
    }
    
    // word. - use zoomout animation
    if (word.match(/.*\.$/)) {
      blip.animation = 'zoomout,shake';
      blip.lag *= 2;
    }
    
    // _word_ - longer duration
    if (word.match(/^_.*_$/)) {
      blip.displayWord = word.substring(1, word.length - 1);
      blip.duration += (defaultSpeed / 2);
    }
    
    // #word# - use topbounce animation
    if (word.match(/^#.*#$/)) {
      blip.displayWord = word.substring(1, word.length - 1);
      blip.animation = 'topbounce,fade';
    }
    
    // "word" - longer duration
    if (word.match(/^".*"$/)) {
      blip.displayWord = word.substring(1, word.length - 1);
      blip.duration += defaultSpeed;
    }
    
    return blip;
  }
  
  // Process text into blips with animation info
  function parseMsg(text: string): Blip[] {
    const rawWords = text.split(/\s+/).filter(word => word.length > 0);
    const processedBlips: Blip[] = [];
    
    for (let i = 0; i < rawWords.length; i++) {
      const currentWord = rawWords[i];
      const nextWord = i < rawWords.length - 1 ? rawWords[i + 1] : null;
      
      // If there's a next word and combined they're less than 10 characters, show them together
      if (nextWord && (currentWord.length + nextWord.length < 10) && 
          !hasSpecialSyntax(currentWord) && !hasSpecialSyntax(nextWord)) {
        const combinedWord = `${currentWord} ${nextWord}`;
        processedBlips.push(interpWord(combinedWord));
        i++; // Skip the next word since we've already included it
      } else {
        processedBlips.push(interpWord(currentWord));
      }
    }
    
    return processedBlips;
  }
  
  // Check if a word has special syntax characters that would trigger special animations
  function hasSpecialSyntax(word: string): boolean {
    return !!word.match(/^@.*@$/) || 
           !!word.match(/.*!$/) || 
           !!word.match(/.*,$/) || 
           !!word.match(/.*\.$/) ||
           !!word.match(/^_.*_$/) ||
           !!word.match(/^#.*#$/) ||
           !!word.match(/^".*"$/);
  }
  
  // Update blips when text changes
  $: {
    blips = parseMsg(settings.text);
    currentBlipIndex = 0;
  }
  
  // Reset animation by updating the class with a unique suffix
  function resetAnimation() {
    animationKey++;
    const currentBlip = blips[currentBlipIndex] || { animation: selectedAnimation };
    const animations = currentBlip.animation.split(',');
    
    // If the animation has two parts (like "wobble,fade"), use both
    if (animations.length > 1) {
      animationClass = `anim-${animations[0]}-${animationKey} anim-${animations[1]}-${animationKey}`;
    } else {
      animationClass = `anim-${currentBlip.animation}-${animationKey}`;
    }
  }
  
  function startRSVP() {
    if (!isPlaying && blips.length > 0) {
      isPlaying = true;
      advanceWord();
    }
  }
  
  function advanceWord() {
    if (!isPlaying) return;
    
    resetAnimation();
    
    // Schedule the next word with the current blip's duration + lag
    const currentBlip = blips[currentBlipIndex];
    playInterval = window.setTimeout(() => {
      // Move to next word
      currentBlipIndex = (currentBlipIndex + 1) % blips.length;
      advanceWord();
    }, currentBlip.duration + currentBlip.lag);
  }
  
  function stopRSVP() {
    if (isPlaying) {
      isPlaying = false;
      if (playInterval) {
        clearTimeout(playInterval);
        playInterval = null;
      }
    }
  }
  
  function togglePlay() {
    if (isPlaying) {
      stopRSVP();
    } else {
      startRSVP();
    }
  }
  
  function adjustSpeed(increment: boolean) {
    // Adjust the playback speed
    if (increment && defaultSpeed > 100) {
      defaultSpeed -= 50;
    } else if (!increment && defaultSpeed < 1000) {
      defaultSpeed += 50;
    }
    
    // Update all blips with the new base speed
    blips = parseMsg(settings.text);
    
    // Restart if playing
    if (isPlaying) {
      stopRSVP();
      startRSVP();
    }
  }
  
  function changeAnimation(direction: 'next' | 'prev') {
    const currentIndex = animationOptions.indexOf(selectedAnimation);
    let newIndex;
    
    if (direction === 'next') {
      newIndex = (currentIndex + 1) % animationOptions.length;
    } else {
      newIndex = (currentIndex - 1 + animationOptions.length) % animationOptions.length;
    }
    
    selectedAnimation = animationOptions[newIndex];
    
    // Update blips that use the default animation
    blips = parseMsg(settings.text);
    resetAnimation();
  }
  
  // Calculate a base font size that fills the screen nicely
  function calculateBaseFontSize(): number {
    // Base size calculation based on viewport dimensions
    return Math.min(windowWidth, windowHeight) * 0.18;
  }
  
  // More sophisticated font size calculation that considers word characteristics
  function calculateOptimalFontSize(word: string): number {
    // Start with base size
    let base = calculateBaseFontSize();
    
    // Get word length
    const length = word.length;
    
    // Character width approximation
    // Characters like 'i', 'l', 'j', 't' are narrow
    // Characters like 'w', 'm' are wide
    const narrowChars = (word.match(/[iljft1'\.\,]/g) || []).length;
    const wideChars = (word.match(/[wm@]/g) || []).length;
    
    // Calculate effective length considering character width variations
    const effectiveLength = length - (narrowChars * 0.5) + (wideChars * 0.5);
    
    // Scaling factors based on word characteristics
    let scaleFactor = 1.0;
    
    // More aggressive scaling for longer words
    if (effectiveLength <= 3) {
      scaleFactor = 1.2; // Very short words can be bigger
    } else if (effectiveLength <= 6) {
      scaleFactor = 1.0; // Normal scaling for average words
    } else if (effectiveLength <= 10) {
      scaleFactor = 0.85; // Slightly reduced for longer words
    } else if (effectiveLength <= 15) {
      scaleFactor = 0.75; // More reduction for even longer words
    } else {
      // For very long words, scale down more aggressively
      // But ensure a minimum size
      scaleFactor = Math.max(0.4, 1.0 - (effectiveLength * 0.03));
    }
    
    // Adjust scale factor based on all uppercase vs mixed case
    if (word === word.toUpperCase() && word.length > 2) {
      scaleFactor *= 0.9; // All caps is harder to read, so slightly smaller
    }
    
    return base * scaleFactor;
  }
  
  onMount(() => {
    // Set initial window dimensions
    windowWidth = window.innerWidth;
    windowHeight = window.innerHeight;
    
    // Update dimensions on resize
    const handleResize = () => {
      windowWidth = window.innerWidth;
      windowHeight = window.innerHeight;
    };
    
    window.addEventListener('resize', handleResize);
    
    // Start RSVP automatically in presentation mode
    if (blips.length > 0) {
      startRSVP();
    }
    
    return () => {
      // Clean up interval and event listeners on component destruction
      if (playInterval) {
        clearTimeout(playInterval);
      }
      window.removeEventListener('resize', handleResize);
    };
  });
  
  // Current word to display
  $: currentBlip = blips[currentBlipIndex] || { displayWord: '', animation: selectedAnimation, duration: defaultSpeed, lag: 5 };
  
  // Calculate font size based on improved algorithm
  $: fontSize = calculateOptimalFontSize(currentBlip.displayWord);
  
  // Update the animation class when the animation changes
  $: {
    if (currentBlip) {
      resetAnimation();
    }
  }
</script>

<div class="presentation-mode fixed inset-0 bg-black flex flex-col justify-center items-center z-50">
  <!-- Exit button -->
  <button 
    class="absolute top-4 right-4 text-white bg-gray-800 hover:bg-gray-700 rounded-full p-2"
    on:click={exitPresentation}
    aria-label="Exit presentation mode"
  >
    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
    </svg>
  </button>
  
  <!-- Animation selection -->
  <div class="absolute top-4 left-4 text-white text-sm flex items-center gap-2">
    <button 
      class="bg-gray-800 hover:bg-gray-700 rounded-full p-2"
      on:click={() => changeAnimation('prev')}
      aria-label="Previous animation"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
    </button>
    
    <span class="font-medium capitalize">{selectedAnimation}</span>
    
    <button 
      class="bg-gray-800 hover:bg-gray-700 rounded-full p-2"
      on:click={() => changeAnimation('next')}
      aria-label="Next animation"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
      </svg>
    </button>
  </div>
  
  <!-- Text display -->
  <div class="word-display flex-1 flex justify-center items-center w-full overflow-hidden">
    {#if blips.length > 0}
      <p
        class="{settings.effect !== 'none' ? `text-${settings.effect}` : ''} {animationClass}"
        style="
          font-family: {settings.fontFamily === 'sans' ? 'Inter, sans-serif' : 
                     settings.fontFamily === 'serif' ? 'Playfair Display, serif' : 
                     'Space Mono, monospace'};
          font-size: {fontSize}px;
          font-weight: {settings.fontWeight};
          letter-spacing: {settings.letterSpacing}px;
          line-height: {settings.lineHeight};
          text-align: center;
          text-transform: {settings.textTransform};
          color: {settings.color};
          max-width: 90vw;
          display: inline-block;
          overflow: visible;
          animation-fill-mode: both;
          animation-duration: {currentBlip.duration/1000}s;
        "
      >
        {currentBlip.displayWord}
      </p>
    {:else}
      <p class="text-white text-4xl">No text to display</p>
    {/if}
  </div>
  
  <!-- Display progress -->
  <div class="progress-indicator w-full h-1 bg-gray-800 mb-8">
    <div 
      class="h-full bg-primary-500 transition-all duration-200"
      style="width: {blips.length > 0 ? (currentBlipIndex / blips.length * 100) : 0}%"
    ></div>
  </div>
  
  <!-- Syntax help -->
  <div class="absolute top-4 text-gray-500 text-xs">
    <button class="text-gray-400 hover:text-white underline" on:click={() => alert("Special formatting:\n@word@ = wiggle\nword! = wobble\nword, = bounce\nword. = zoom\n_word_ = slow\n#word# = bounce\n\"word\" = very slow")}>
      Syntax Help
    </button>
  </div>
  
  <!-- Controls -->
  <div class="controls absolute bottom-8 flex gap-4">
    <button 
      class="bg-white p-3 rounded-full"
      on:click={() => adjustSpeed(false)}
      aria-label="Slow down"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
    </button>
    
    <button 
      class="bg-white p-3 rounded-full"
      on:click={togglePlay}
      aria-label={isPlaying ? "Pause" : "Play"}
    >
      {#if isPlaying}
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 9v6m4-6v6m7-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      {:else}
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      {/if}
    </button>
    
    <button 
      class="bg-white p-3 rounded-full"
      on:click={() => adjustSpeed(true)}
      aria-label="Speed up"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
      </svg>
    </button>
  </div>
  
  <!-- Current word info -->
  <div class="absolute bottom-2 text-gray-500 text-xs">
    {currentBlipIndex + 1} / {blips.length} · {defaultSpeed}ms
  </div>
</div>

<style>
  .presentation-mode {
    touch-action: manipulation;
  }
  
  .word-display {
    padding: 2rem;
  }
</style> 