<script lang="ts">
  import TypographyPlayground from './components/TypographyPlayground.svelte';
  import PresentationMode from './components/PresentationMode.svelte';
  import { onMount } from 'svelte';
  
  interface TypographySettings {
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
  }
  
  let title = "iBlipper";
  let subtitle = "Expressive Typography Playground";
  let isPresenting = false;
  let presentationSettings: TypographySettings = {
    text: 'Type your text here...',
    fontFamily: 'serif',
    fontSize: 48,
    fontWeight: 400,
    letterSpacing: 0,
    lineHeight: 1.2,
    textAlign: 'center',
    textTransform: 'none',
    color: '#0284c7',
    effect: 'none'
  };
  
  // Handle window orientation changes for mobile
  let isLandscape = false;
  
  function checkOrientation() {
    isLandscape = window.innerWidth > window.innerHeight;
    if (window.innerWidth < 768) { // Mobile device
      isPresenting = isLandscape;
    }
  }
  
  onMount(() => {
    checkOrientation();
    window.addEventListener('resize', checkOrientation);
    
    // Handle ESC key to exit presentation mode
    const keyHandler = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isPresenting) {
        isPresenting = false;
      }
    };
    
    window.addEventListener('keydown', keyHandler);
    
    return () => {
      window.removeEventListener('resize', checkOrientation);
      window.removeEventListener('keydown', keyHandler);
    };
  });
  
  function updatePresentationSettings(event: CustomEvent<TypographySettings>) {
    presentationSettings = event.detail;
  }
  
  function togglePresentation() {
    isPresenting = !isPresenting;
  }
</script>

{#if isPresenting}
  <PresentationMode settings={presentationSettings} exitPresentation={togglePresentation} />
{:else}
  <main class="min-h-screen p-6 md:p-12">
    <header class="mb-12 text-center">
      <h1 class="text-6xl md:text-8xl font-serif font-bold mb-4 text-gradient">
        {title}
      </h1>
      <p class="text-xl md:text-2xl font-sans text-gray-600">
        {subtitle}
      </p>
    </header>
    
    <TypographyPlayground 
      on:settingsChange={updatePresentationSettings} 
      on:presentClick={togglePresentation} 
    />
    
    <footer class="mt-16 text-center text-sm text-gray-500">
      <p>Created with Svelte & Tailwind CSS</p>
    </footer>
  </main>
{/if}

<style>
  :global(html) {
    scroll-behavior: smooth;
  }
</style>
