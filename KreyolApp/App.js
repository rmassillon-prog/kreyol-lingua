const speak = (textToSpeak) => {
    let phoneticText = textToSpeak
      .toLowerCase()
      .replace(/\bap\b/g, 'app')      // Fixes the silent 'p'
      .replace(/mache/g, 'maché')     // Fixes the silent 'e'
      .replace(/manje/g, 'man-zhay')  // Fixes the 'manj' clipping
      .replace(/mwen/g, 'mou-en');    // Improves the nasal sound

    Speech.speak(phoneticText, { 
      language: 'fr-FR', 
      pitch: 0.9, 
      rate: 0.65 
    });
  };
