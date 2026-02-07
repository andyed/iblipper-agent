<script lang="ts">
  export let text = '';
  export let fontFamily = 'serif';
  export let fontSize = 48;
  export let fontWeight = 400;
  export let letterSpacing = 0;
  export let lineHeight = 1.2;
  export let textAlign = 'left';
  export let textTransform = 'none';
  export let color = '#0284c7';
  export let effect = 'none';
  
  function getEffectClass(effectName: string): string {
    switch(effectName) {
      case 'gradient': return 'text-gradient';
      case 'shadow': return 'text-shadow';
      case 'outline': return 'text-outline';
      case 'animated': return 'text-animated';
      default: return '';
    }
  }
</script>

<div
  class="typography-display {getEffectClass(effect)}"
  style="
    font-family: {fontFamily === 'sans' ? 'Inter, sans-serif' : 
               fontFamily === 'serif' ? 'Playfair Display, serif' : 
               'Space Mono, monospace'};
    font-size: {fontSize}px;
    font-weight: {fontWeight};
    letter-spacing: {letterSpacing}px;
    line-height: {lineHeight};
    text-align: {textAlign};
    text-transform: {textTransform};
    color: {effect === 'gradient' ? 'currentColor' : color};
  "
>
  {text}
</div> 